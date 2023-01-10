{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Use <$>" #-}
import Test.QuickCheck
import Data.Maybe
import System.Random

import ChessBase
import FEN
import MovePredictor


------------------------------------------------------------------------------------------- [Arbitraries] ---------------------------------------------------------------------------------------------------
-- Generate a random color
instance Arbitrary Color where
    arbitrary = elements [White, Black]

instance Arbitrary PieceType where
    arbitrary = frequency [(8,(return Pawn)), (2,(return Bishop)), (2,(return Knight)), (2,(return Rook)), (1,(return King)), (1,(return Queen))]

genPiece :: Gen (Piece)
genPiece = do
           (r1,r2) <- genPosition
           p <- arbitrary
           c <- arbitrary
           return (Piece p c r1 r2)

instance Arbitrary Piece where
    arbitrary = genPiece

-- Generate a random position on the board
genPosition :: Gen (Int,Int)
genPosition = do
    col <- choose (0,7)
    row <- choose (0,7)
    return (col,row)
    
    
genPieceNotKing :: Gen Piece
genPieceNotKing = genPiece `suchThat` ((/= King) . pieceType)


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

instance Arbitrary FenParser where
    arbitrary = do 
                x <- choose (0,7)
                y <- choose (0,7)
                n <- choose (10,20)
                ps <- vectorOf n genPiece
                return (FenParser ps x y)


instance Arbitrary RatedBoard where
    arbitrary = do
                b <- arbitrary
                d <- arbitrary
                return $ RatedBoard b (abs d)
                

                
instance Arbitrary StdGen where
    arbitrary = do 
                seed <- chooseInt (0,1000000)
                return $ mkStdGen seed
------------------------------------------------------------------------------------------- [ChessBase Properties] ---------------------------------------------------------------------------------------------------
{-
    The purpose of writing properties is three-fold:

    * They serve as a specification before you write your functions.
    * During the implementation phase they help you with debugging.
    * When you are finished they serve as mathematically precise documentation for your program.

-}

-- Checks that all found valid boards fulfills the property of prop_boardValid 
prop_findAllValidMoves :: Board -> Bool
prop_findAllValidMoves b = all prop_boardValid (findAllValidMoves b)


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
        numbers l = l <= 16 

-- Check that a board fullfill all invariants
prop_boardValid :: Board -> Bool
prop_boardValid board = all prop_pieceValid (pieces board) && prop_noPiecesOverlapping board && prop_containsKings board && prop_piecesPerColor board



-- Function (pieceType) should satisfy this property i.e.
-- The return type should be one of the piece types 
prop_pieceType :: Piece -> Bool
prop_pieceType p = or[sort == t | t <- [Pawn,King,Queen,Knight,Bishop,Rook]]
            where
                sort = pieceType p


-- Function (pieceColor) should satisfy this property i.e
-- The return color should be one of the two colors
prop_pieceColor :: Piece -> Bool
prop_pieceColor p = or[col == t | t <- [White,Black]]
            where
                col = pieceColor p
           

-- Function (pieces) should satisfy this property
-- The return value should be in these range
prop_pieces :: Board -> Bool
prop_pieces b = l > 2 && l <= 32
    where 
        l = length $ pieces b 


-- Function (otherColor) should satisfy this property
-- The return of the return value should be the same as the arbitrary color 
prop_otherColor :: Color -> Bool
prop_otherColor c = c == otherColor (otherColor c) 


-- Function (nextTurn) should satisfy this property
-- The return board should contain the same pieces but the opposite color to the original board
prop_nextTurn :: Board -> Bool
prop_nextTurn (Board ps c) = (pieces newBoard == ps) && (notToMove newBoard == c)
        where  
            newBoard = nextTurn (Board ps c)


-- Function (piecePosition) should satisfy this property
-- The return position should be in these valid ranges
prop_piecePosition :: Piece -> Bool
prop_piecePosition p = (x >= 0 && x <= 7) && (y >= 0 && y <= 7)
            where
                (x,y) = piecePosition p


-- Function (piecesOfColor) should satisfy this property
-- The return pieces all should have the same color as the arbitrary color  
prop_piecesOfColor :: Board -> Color -> Bool
prop_piecesOfColor b c = and $ map (== c) list
                where
                    ps   = piecesOfColor b c 
                    list = map (pieceColor) ps 


-- Function (myPieces) should satisfy this property
-- The return pieces all should have the same color as the board and the number of the return pieces should be in these range 
prop_myPieces :: Board -> Bool
prop_myPieces b = sameColor && (l > 0) && (l <= 16)
        where
            ps = myPieces b
            sameColor = and[isPieceOfColor (toMove b) p | p <- ps]
            l = length ps


-- Function (piecesContains) should satisfy this property
-- If having a list of pieces and adding a piece to the list then, the return value of the function should always be True 
-- There will be some cases that are discarded due to the precondition
prop_piecesContains :: [Piece] -> Piece -> Property
prop_piecesContains ps p = (length ps) > 0 ==> found 
        where 
            insert = ps ++ [p]
            found = piecesContains insert p 


-- Function (boardContains) should satisfy this property
-- If the arbitrary board is valid and the return value of function (boardContains) is True then there should be at least one piece among the board's pieces (since there could be more) 
-- There will be some tests that pass and many that are discarded due to the preconditions 
-- General prop  
prop_boardContains :: Board -> Piece -> Property
prop_boardContains b p = boardContains b p ==> (length $ filter (== p) (pieces b)) > 0 
        where
            found = boardContains b p


-- Function (movePieceTo) should satisfy this property
-- Given an arbitrary board, a position (x,y) and an index, taken a pieces from the board's pieces at index 
-- Moving the piece and producing a newBoard through function (movePieceTo)
-- Then the newBoard should contain the newPiece with positions (x,y) i.e. being True 
-- There will be many discarded cases and few passed due to the preconditions 
prop_movePieceTo :: Board -> Int -> Int -> Int -> Property    
prop_movePieceTo b x y index = (isPosValid x y) && (index > 2 && index < (length (pieces b))) ==> moved
            where
                p = (pieces b) !! index
                newB = movePieceTo b p x y
                newPiece = Piece (pieceType p) (pieceColor p) x y
                moved = boardContains newB newPiece


-- Function (isThisPieceAt) should satisfy this property
-- Given an arbitrary board and piece, if the board contains the piece, taken the position (x,y) of the piece on the board the return value of function (isThisPieceAt) should always be True 
-- There will be many discarded cases and few passed due to the preconditions
-- General prop
prop_thisPieceAt :: Board -> Piece -> Property
prop_thisPieceAt b p = boardContains b p ==> (isThisPieceAt x y p)
        where
            (x,y) = piecePosition p



-- Function (isSpaceOccupied) should satisfy this property
-- The return value should always be True
-- Not a general property
prop_spaceOccupied :: Board -> Bool
prop_spaceOccupied b = isSpaceOccupied b x y
        where
            p = head (pieces b)
            (x,y) = piecePosition p


-- Function (tryMoveTo) should satisfy this property
-- Given an arbitrary board, a valid position (x,y), a valid index and taken a piece p from the board at index 
-- Function (tryMoveTo) should produce a new board that still contains the same piece p but at the new position (x,y) 
-- There will be many discarded cases and few tests that pass due to preconditions 
prop_tryMoveTo :: Board -> Int -> Int -> Int -> Property
prop_tryMoveTo b x y index = (isPosValid x y) && (index > 2 && index <= (length (pieces b))) ==> if (newB == Nothing) then True else moved
            where 
                p = (pieces b) !! index
                newB = tryMoveTo b p x y
                newPiece = Piece (pieceType p) (pieceColor p) x y
                moved = boardContains (fromJust newB) newPiece


-- Function (isSpaceOccupiedByColor) should satisfy this property
-- Considering the precondition being True then that means that the piece p at that position (x,y) have the same color c
-- There will be many discarded cases and few tests that pass due to precondition 
prop_occupiedByColor :: Board -> Color -> Int -> Int -> Property
prop_occupiedByColor b c x y = isSpaceOccupiedByColor b c x y ==> pieceColor p == c
                    where
                        p = head $ filter (isThisPieceAt x y) (pieces b)


-- Function (isSpaceOccupiedByColor) should satisfy this property
-- Given an arbitrary board and valid position (x,y) 
-- If there exist a piece p at the position (x,y) then the board must contain that peice as well
-- There will be many discarded cases and few tests that pass due to precondition
prop_getPieceAt :: Board -> Int -> Int -> Property
prop_getPieceAt b x y = isPosValid x y ==> if (p == Nothing) then True else (boardContains b (fromJust p))
            where 
                p = getPieceAt b x y 


-- Function (tryCaptureAt) should satisfy this property
-- Given an arbitrary board, a piece of same color as the board and a position (x,y)
-- If the p is able to capture the piece at position (x,y) then the newB should contain the new piece newP and exactly one 
-- There will be som discarded cases due to precondition 
prop_tryCaptureAt :: Board -> Piece -> Int -> Int -> Property
prop_tryCaptureAt b p x y = (pieceColor p == (toMove b)) ==> if (newB == Nothing) then True else (length (filter (== newP) (myPieces (fromJust newB))) == 1) 
            where
                newB = tryCaptureAt b p x y 
                newP = Piece (pieceType p) (pieceColor p) x y
                lBefore = length $ pieces b
                lAfter = length $ pieces (fromJust newB)


-- Function (findValidMovesForPawn) should satisfy this property
-- Given an arbitrary board and taken a piece p of type Pawn from the board 
-- Then if function (findValidMovesForPawn) finds a valid move, then the new board newB1 should contain that peice in one of these positions
-- Not general as it only tests the first board produced by function (findValidMovesForPawn), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForPawn :: Board -> Property 
prop_movesForPawn b = pawnExist ==> if (l == 0) then True else contain
    where 
        pawnExist = any ((== Pawn) . pieceType) (pieces b)
        p = head[p | p <- (pieces b), pieceType p == Pawn]
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForPawn b p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Pawn col (x+nX) (y+nY)) | nX <- [-1,0,1], nY <- [-1,1]]


------------------------------------------------------------------------------------------- [FEN Properties] ---------------------------------------------------------------------------------------------------

pos :: FenParser -> (Int,Int)
pos (FenParser _ x y) = (x,y)

prop_FENisValid :: Bool
prop_FENisValid = prop_boardValid board
    where board = parseFEN "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

-- Function (parseFenLetter) should satisfy this property
-- There will be many discarded cases and few tests that pass due to precondition
prop_parseFenLetter :: FenParser -> Char -> Property
prop_parseFenLetter f c = validChar ==> (nX == x+1 && nY == y) && (px == x && py == y)
            where
                validChar = or[v == c | v <- ['p','q','r','b','n','k']]
                fp = parseFenLetter f c
                (x,y) = pos f
                (nX,nY) = pos fp
                p = head $ result fp
                (px,py) = piecePosition p



------------------------------------------------------------------------------------------- [MovePredictor Properties] ---------------------------------------------------------------------------------------------------

-- Function (addScore) should satisfy this property
prop_addScore :: RatedBoard -> Double -> Bool
prop_addScore rb d = sum == originald + d
    where
        ratedB = addScore rb d 
        sum = rating ratedB
        originald = rating rb


-- Function (bestBoard) should satisfy this property
prop_bestBoard :: [RatedBoard] -> Property
prop_bestBoard rBoards = (length rBoards) /= 0 ==> (b == newRB)
        where
            allD = map (rating) rBoards
            maxD = maximum allD
            b = head [b | b <- rBoards, (rating b) == maxD]
            bestB = bestBoard rBoards
            newRB = RatedBoard bestB maxD
            
prop_selectRandomMoveValid :: Board -> StdGen -> Bool
prop_selectRandomMoveValid board g = prop_boardValid $ selectRandomMove board g



prop_recursionMoveValid :: Board -> StdGen -> Property
prop_recursionMoveValid board g = ( length ( pieces board) > 6) ==>  prop_boardValid $ recursionRating board g


