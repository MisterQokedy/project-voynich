# Model weights

All files are under 20 MB and stored in git. `MANIFEST.txt` lists each file with its size and SHA-256.

- `kraken_line_reader_s1/s2/s3.safetensors`: Kraken TorchVGSL line readers (about 4.0 M parameters, 1×120×400 line image in, CTC out), trained from scratch on line images with EVA labels. Three seeds, best validation checkpoint of each, run as an ensemble (mean frame posteriors, greedy decoding). Kraken `best_*.safetensors` format, not an `.mlmodel` export.
- `glyphseg_fold0.pt`, `glyphseg_fold1.pt`: glyph-segmenter U-Net state dicts (four-level encoder, 32/64/128/256 channels, 3-channel input, 1-channel mask logit, BCE + Dice loss). Fold 0 was trained on sheet fold 0 and applied to fold 1, and fold 1 the other way round. The model class is in `tools/segmenter/train.py`.
