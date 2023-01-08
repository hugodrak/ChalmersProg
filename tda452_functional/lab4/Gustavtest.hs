


import Test.QuickCheck
import ChessBase
import FEN


-- Generate a random color
instance Arbitrary Color where
    arbitrary = elements [White, Black]

-- Generate a random position on the board
genPosition :: Gen (Int,Int)
genPosition = do
    col <- choose (0,7)
    row <- choose (0,7)
    return (col,row)
    

    
genPieceNotKing :: Gen Piece
genPieceNotKing = do
    
    typ <- frequency [(8,return Pawn), (2,return Bishop), (2,return Knight), (2,return Rook), (1,return Queen)]
    color <- arbitrary
    (col,row) <- genPosition
    return $ Piece typ color col row
 
-- Generate a king of the given color on a random position
genKing :: Color -> Gen Piece
genKing color = do
    (col,row) <- genPosition
    return $ Piece King color col row 

-- Generate a board containing a bunch of random pieces. It's guaranteed to have at least one king of each color.
-- The generated board could break some of our invariants however:
--      * Pieces may be outside the board ([0..7])
--      * Multiple pieces may occupy the same square
genPerhapsInvalidBoard :: Gen (Board)
genPerhapsInvalidBoard = do
    
    amountPieces <- choose (0,30) 
    pieces <- vectorOf amountPieces genPieceNotKing
    whiteKing <- genKing White
    blackKing <- genKing Black
    
    let allPieces = whiteKing:blackKing:pieces
    toMove <- arbitrary
    
    return $ Board allPieces toMove

-- Invariant all pieces should fullfill. Row and column must be in range [0..7]
isPieceAtValidPosition :: Piece -> Bool
isPieceAtValidPosition piece = (x>=0) && (x<=7) && (y>=0) && (y<=7)
    where (x,y) = piecePosition piece

-- No pieces may be at the same square. An invariant all board should fullfill
-- We implments this by asserting that the number of pieces on each square is either 0 or 1. E.i less than 2
prop_noPiecesOverlapping :: Board -> Bool
prop_noPiecesOverlapping (Board pieces _) = all ((<2) . amountPiecesAtPosition) [(x,y) | x<-[0..7], y<-[0..7]]

    where amountPiecesAtPosition (x,y) = length $ filter (isThisPieceAt x y) pieces

prop_pieceValid :: Piece -> Bool
prop_pieceValid = isPieceAtValidPosition
    
-- Check that a board fullfill all invariants
prop_boardValid :: Board -> Bool
prop_boardValid board = all prop_pieceValid (pieces board) && prop_noPiecesOverlapping board

-- Define a generator which only generate valid board
genValidBoard :: Gen Board
genValidBoard = genPerhapsInvalidBoard `suchThat` prop_boardValid

instance Arbitrary Board where
    arbitrary = genValidBoard

printRandomBoard :: IO ()
printRandomBoard = do
                    board <- generate arbitrary
                    let s = formatBoard board
                    putStr s
                    

prop_FENisValid = prop_boardValid board
    where board = parseFEN "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

