# Fetches RIDGES Herbology v9.0 and the Zenodo HTR ground-truth sets (all CC BY 4.0).
# Run from the repository's work folder :
#   powershell -ExecutionPolicy Bypass -File fetch\fetch_ridges_zenodo.ps1
# Output: regional\incoming\bundle8\...  plus  regional\incoming\bundle8_upload.zip
#         and bundle8\RESULTS_SUMMARY.md
param(
  [int]$MaxFileMB = 1500   # Zenodo files larger than this are listed but not downloaded
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Add-Type -AssemblyName System.IO.Compression.FileSystem

$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root 'data'))) { $Root = (Get-Location).Path }
$Out  = Join-Path $Root 'regional\incoming\bundle8'
$UA   = @{ 'User-Agent' = 'VoynichResearchBundle/1.0 (personal research script)' }
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$rows = New-Object System.Collections.ArrayList

function Log($src, $file, $bytes, $status) {
  [void]$rows.Add([pscustomobject]@{src=$src; file=$file; bytes=$bytes; status=$status})
  Write-Host ("[{0}] {1}  {2} bytes  {3}" -f $src, $file, $bytes, $status)
}
function Get-Json($url) {
  for ($i=1; $i -le 4; $i++) {
    try { return Invoke-RestMethod -Uri $url -Headers $UA -UseBasicParsing -TimeoutSec 120 }
    catch { Write-Host "  retry $i : $url ($($_.Exception.Message))"; Start-Sleep -Seconds (5*$i) }
  }
  return $null
}
function Get-File($url, $dest, $md5) {
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
  if ((Test-Path $dest) -and $md5 -and ((Get-FileHash $dest -Algorithm MD5).Hash -ieq $md5)) { return 'ok (cached)' }
  for ($i=1; $i -le 4; $i++) {
    try {
      Invoke-WebRequest -Uri $url -OutFile $dest -Headers $UA -UseBasicParsing -TimeoutSec 1800
      $len = (Get-Item $dest).Length
      if ($len -le 0) { throw 'empty file' }
      if ($md5) {
        $h = (Get-FileHash $dest -Algorithm MD5).Hash
        if ($h -ine $md5) { throw "md5 mismatch ($h)" }
        return 'ok (md5 checked)'
      }
      return 'ok'
    } catch { Write-Host "  retry $i : $url ($($_.Exception.Message))"; Start-Sleep -Seconds (5*$i) }
  }
  return 'FAILED'
}
function Size($p) { if (Test-Path $p) { (Get-Item $p).Length } else { 0 } }

# ---------- 1. RIDGES Herbology v9.0 (archive.org) ----------
Write-Host "`n== 1. RIDGES Herbology (archive.org the-ridges-herbology)"
$ridgesDir = Join-Path $Out 'ridges'
$meta = Get-Json 'https://archive.org/metadata/the-ridges-herbology'
if ($null -eq $meta) { Log 'ridges' '(metadata)' 0 'FAILED' }
else {
  foreach ($f in $meta.files) {
    if ($f.name -notmatch '\.(xlsx|meta)$') { continue }
    $dest = Join-Path $ridgesDir $f.name
    $url  = 'https://archive.org/download/the-ridges-herbology/' + [uri]::EscapeDataString($f.name)
    $st = Get-File $url $dest $f.md5
    Log 'ridges' $f.name (Size $dest) $st
  }
}

# ---------- 2. Zenodo HTR ground truth ----------
Write-Host "`n== 2. Zenodo HTR ground truth"
$zen = @(
  @{key='klosterneuburg_cod48'; id='7466927'},
  @{key='inzigkofen';           id='17978574'},
  @{key='enhg_1480_85';         id='21257167'}
)
foreach ($z in $zen) {
  $dir = Join-Path $Out ('zenodo_' + $z.key)
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $rec = Get-Json ('https://zenodo.org/api/records/' + $z.id)
  if ($null -eq $rec) {
    # the id may be a concept DOI: resolve through doi.org and retry with the final record id
    try {
      $r = Invoke-WebRequest -Uri ('https://doi.org/10.5281/zenodo.' + $z.id) -Headers $UA -UseBasicParsing -MaximumRedirection 10
      $final = $r.BaseResponse.ResponseUri.AbsoluteUri
      if ($final -match '/records/(\d+)') { $rec = Get-Json ('https://zenodo.org/api/records/' + $Matches[1]) }
    } catch {}
  }
  if ($null -eq $rec) { Log $z.key '(record)' 0 'FAILED'; continue }
  $rec | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $dir 'record.json')
  Log $z.key ("record.json: " + $rec.metadata.title) (Size (Join-Path $dir 'record.json')) 'ok'
  foreach ($f in $rec.files) {
    $name = $f.key; $bytes = [int64]$f.size
    $md5 = $null; if ($f.checksum -match '^md5:(.+)$') { $md5 = $Matches[1] }
    if ($bytes -gt $MaxFileMB*1MB) { Log $z.key $name $bytes ("SKIPPED (> $MaxFileMB MB; rerun with -MaxFileMB " + [math]::Ceiling($bytes/1MB+1) + ")"); continue }
    $url = $f.links.self
    if (-not $url) { $url = 'https://zenodo.org/records/' + $rec.id + '/files/' + [uri]::EscapeDataString($name) + '?download=1' }
    $dest = Join-Path $dir $name
    $st = Get-File $url $dest $md5
    Log $z.key $name (Size $dest) $st
    # keep only the text layer of zips (PAGE/ALTO XML, txt, json, csv) for upload; images stay on the PC
    if ($st -like 'ok*' -and $name -match '\.zip$') {
      $xdir = Join-Path $dir ('text_' + [IO.Path]::GetFileNameWithoutExtension($name))
      New-Item -ItemType Directory -Force -Path $xdir | Out-Null
      $zip = [IO.Compression.ZipFile]::OpenRead($dest); $n = 0
      try {
        foreach ($e in $zip.Entries) {
          if ($e.FullName -match '\.(xml|txt|json|csv|tsv|md)$' -and $e.Length -gt 0) {
            $safe = ($e.FullName -replace '[\\/:*?"<>|]', '__')
            [IO.Compression.ZipFileExtensions]::ExtractToFile($e, (Join-Path $xdir $safe), $true); $n++
          }
        }
      } finally { $zip.Dispose() }
      Log $z.key ("  text entries from " + $name) $n ($(if ($n -gt 0) {'ok'} else {'no text entries'}))
    }
  }
}

# ---------- 3. de.wikisource cookbooks ----------
Write-Host "`n== 3. de.wikisource"
$wsDir = Join-Path $Out 'wikisource'
New-Item -ItemType Directory -Force -Path $wsDir | Out-Null
$api = 'https://de.wikisource.org/w/api.php'
$queries = @('Buch von guter Speise', 'buoch von guoter spise', 'Meister Eberhard Kochbuch',
             'Kochbuch Meister Eberhards', 'Mondseer Kochbuch', 'Mondsee Rezepte Kochbuch')
$titles = New-Object System.Collections.Generic.List[string]
$searchLog = @()
foreach ($q in $queries) {
  $r = Get-Json ($api + '?action=query&list=search&format=json&srlimit=8&srnamespace=0&srsearch=' + [uri]::EscapeDataString($q))
  if ($null -eq $r) { Log 'wikisource' "search: $q" 0 'FAILED'; continue }
  foreach ($h in $r.query.search) { $searchLog += [pscustomobject]@{query=$q; title=$h.title; size=$h.size} }
  foreach ($h in ($r.query.search | Select-Object -First 3)) { if (-not $titles.Contains($h.title)) { $titles.Add($h.title) } }
}
$searchLog | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $wsDir 'search_results.json')
# add subpages (Title/...) of every hit
$all = New-Object System.Collections.Generic.List[string]
foreach ($t in $titles) {
  if (-not $all.Contains($t)) { $all.Add($t) }
  $r = Get-Json ($api + '?action=query&list=allpages&format=json&aplimit=500&apnamespace=0&apprefix=' + [uri]::EscapeDataString($t + '/'))
  if ($r) { foreach ($p in $r.query.allpages) { if (-not $all.Contains($p.title)) { $all.Add($p.title) } } }
}
$i = 0
foreach ($t in ($all | Select-Object -First 400)) {
  $i++
  $safe = ($t -replace '[\\/:*?"<>|]', '__')
  $dest = Join-Path $wsDir ($safe + '.wiki.txt')
  $url = 'https://de.wikisource.org/w/index.php?action=raw&title=' + [uri]::EscapeDataString($t)
  $st = Get-File $url $dest $null
  Log 'wikisource' $t (Size $dest) $st
  # also the rendered text, which resolves transcluded Page: scans
  $r = Get-Json ($api + '?action=parse&format=json&prop=text&disablelimitreport=1&page=' + [uri]::EscapeDataString($t))
  if ($r -and $r.parse.text.'*') {
    $h = Join-Path $wsDir ($safe + '.html'); $r.parse.text.'*' | Set-Content -Encoding UTF8 $h
    Log 'wikisource' ("  rendered " + $t) (Size $h) 'ok'
  }
  Start-Sleep -Milliseconds 300
}

# ---------- summary + upload zip ----------
$ok   = @($rows | Where-Object { $_.status -like 'ok*' }).Count
$bad  = @($rows | Where-Object { $_.status -like 'FAILED*' -or ($_.status -like 'ok*' -and $_.bytes -le 0) })
$skip = @($rows | Where-Object { $_.status -like 'SKIPPED*' })
$zipPath = Join-Path $Root 'regional\incoming\bundle8_upload.zip'
if (Test-Path $zipPath) { Remove-Item $zipPath }
$stage = Join-Path $env:TEMP 'voynich_bundle8_stage'
if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
New-Item -ItemType Directory -Force -Path $stage | Out-Null
Get-ChildItem -Recurse -File $Out | Where-Object { $_.Extension -notmatch '^\.(zip|jpg|jpeg|png|tif|tiff)$' } | ForEach-Object {
  $rel = $_.FullName.Substring($Out.Length).TrimStart('\')
  $d = Join-Path $stage $rel
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $d) | Out-Null
  Copy-Item $_.FullName $d
}
[IO.Compression.ZipFile]::CreateFromDirectory($stage, $zipPath)
Remove-Item -Recurse -Force $stage
$zipMB = [math]::Round((Get-Item $zipPath).Length/1MB, 1)

$md = @("# Bundle 8 results ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))", '',
  "ok: $ok   failed or empty: $($bad.Count)   skipped (too big): $($skip.Count)   upload zip: $zipMB MB", '',
  '| source | file | bytes | status |', '|---|---|---|---|')
foreach ($r in $rows) { $md += "| $($r.src) | $($r.file) | $($r.bytes) | $($r.status) |" }
$sumPath = Join-Path $PSScriptRoot 'RESULTS_SUMMARY.md'
$md | Set-Content -Encoding UTF8 $sumPath
Write-Host "`nDone. ok=$ok failed/empty=$($bad.Count) skipped=$($skip.Count)"
Write-Host "Archive written: $zipPath ($zipMB MB)"
Write-Host "Summary: $sumPath"
