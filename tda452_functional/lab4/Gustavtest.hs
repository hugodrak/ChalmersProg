


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

prop_containsKings :: Board -> Bool 
prop_containsKings (Board ps _) = lw <= 1 && lb <= 1  
    where 
        allKings = [p | p <- ps, pieceType p == King]
        allColor = map pieceColor allKings
        white = filter (==White) allColor 
        black = filter (==Black) allColor
        lw = length white
        lb = length black
    



prop_piecesPerColor :: Board -> Bool 
prop_piecesPerColor (Board ps _) = numbers l1 && numbers l2 
    where 
        allColor = map pieceColor ps 
        allWhite = filter (== White) allColor
        allBlack = filter (== Black) allColor
        l1 = length allWhite
        l2 = length allBlack
        numbers l = l >= 1 && l <= 16 

-- Check that a board fullfill all invariants
prop_boardValid :: Board -> Bool
prop_boardValid board = all prop_pieceValid (pieces board) && prop_noPiecesOverlapping board && prop_containsKings board && prop_piecesPerColor board



-- Define a generator which only generate valid board
genValidBoard :: Gen Board
genValidBoard = genPerhapsInvalidBoard `suchThat` prop_boardValid


prop_findAllValidMoves b = prop_boardValid b ==> all prop_boardValid (findAllValidMoves b)

instance Arbitrary Board where
    arbitrary = genValidBoard

printRandomBoard :: IO ()
printRandomBoard = do
                    board <- generate arbitrary
                    let s = formatBoard board
                    putStr s
                    

prop_FENisValid = prop_boardValid board
    where board = parseFEN "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

