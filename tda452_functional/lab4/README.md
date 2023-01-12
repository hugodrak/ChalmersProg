

## Haskell Chess Engine

A simple haskell chess engine


Uses https://github.com/maksimKorzh/uci-gui for the gui. 

#### Run
`fish compile.fish` compiles the code and launches the web-server on localhost:5000 to play against it

### Bugs / Missing featurs
 * Crashes if the board has too few pieces
 * Don't respect Check properly. Sometimes when placed in check it will try to trade kings. Which of course is invalid
 * Don't support Castling, Promoting, en passant
