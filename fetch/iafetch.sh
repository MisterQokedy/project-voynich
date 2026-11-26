#!/bin/bash
# usage: iafetch.sh identifier  -> writes identifier.txt (djvu text via /stream/, since /download/ is blocked from the cloud)
id=$1
f=$(curl -s -m 30 "https://archive.org/metadata/$id" | python3 -c "import json,sys; d=json.load(sys.stdin); print(next((x['name'] for x in d.get('files',[]) if x['name'].endswith('_djvu.txt')),''))")
[ -z "$f" ] && { echo "no djvu for $id"; exit 1; }
curl -s -m 120 "https://archive.org/stream/$id/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")" | python3 -c "
import sys,html,re; t=sys.stdin.read(); m=re.search(r'<pre[^>]*>(.*?)</pre>',t,re.S); print(html.unescape(m.group(1)) if m else t)" > $id.txt
echo "$id $f $(wc -c < $id.txt)"
