#! /usr/bin/env fish


set outputPath uci-gui/src/HaskellChessEngine || echo no engine exists, cannot remove

rm $outputPath
stack ghc Main.hs

cp Main $outputPath

chmod +x $outputPath

source uci-gui/venv/bin/activate.fish

cd uci-gui/src

python app.py
