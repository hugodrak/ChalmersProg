import Test.QuickCheck
import Data.Maybe
import System.Random

import ChessBase
import FEN
import MovePredictor


------------------------------------------------------------------------------------------- [Arbitraries] ---------------------------------------------------------------------------------------------------

instance Arbitrary Color where
    arbitrary = elements [White, Black]

instance Arbitrary PieceType where
    arbitrary = frequency [(8,(return Pawn)), (2,(return Bishop)), (2,(return Knight)), (2,(return Rook)), (1,(return King)), (1,(return Queen))]

genPiece :: Gen (Piece)
genPiece = do
           r1 <- choose (0,7)
           r2 <- choose (0,7)
           p <- arbitrary
           c <- arbitrary
           return (Piece p c r1 r2)

instance Arbitrary Piece where
    arbitrary = genPiece

genTypeBlack :: Gen (Piece)
genTypeBlack = do
               r1 <- choose (0,7)
               r2 <- choose (0,7)
               frequency [(8,(return (Piece Pawn Black r1 r2))), (2, (return (Piece Bishop Black r1 r2))), (2, (return (Piece Knight Black r1 r2))), (2, (return (Piece Rook Black r1 r2))), (1, (return (Piece Queen Black r1 r2)))]

genTypeWhite :: Gen (Piece)
genTypeWhite = do
               r1 <- choose (0,7)
               r2 <- choose (0,7)
               frequency [(8,(return (Piece Pawn White r1 r2))), (2, (return (Piece Bishop White r1 r2))), (2, (return (Piece Knight White r1 r2))), (2, (return (Piece Rook White r1 r2))), (1, (return (Piece Queen White r1 r2)))]

-- The arbitrary for the board should produce a valid board 
-- One of the strongest condition is that the board contains exactly one White and one Black King 
-- The other is that there should be <= 16 pieces of each type Black and White
instance Arbitrary Board where
    arbitrary = do 
                c <- arbitrary
                nBlack <- choose (10,15) -- Black pieces between 10-15
                nWhite <- choose (10,15) -- White pieces between 10-15
                x <- choose (4,7)
                y <- choose (0,3)
                p1 <- vectorOf nBlack $ genTypeBlack
                p2 <- vectorOf nWhite $ genTypeWhite
                k1 <- elements [(Piece King Black x y)] -- the reason why the two Kings are added somewhat manually 
                k2 <- elements [(Piece King White y x)]
                let p = p1 ++ p2 ++ [k1] ++ [k2]   
                return (Board p c)



{-
    -- The arbitrary for the board that only produces a not valid board with 32 random pieces 
    instance Arbitrary Board where
        arbitrary = do
                    c <- arbitrary
                    p <- vectorOf 32 genPiece
                    return (Board p c)
-}

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
------------------------------------------------------------------------------------------- [ChessBase Properties] ---------------------------------------------------------------------------------------------------
{-
    The purpose of writing properties is three-fold:

    * They serve as a specification before you write your functions.
    * During the implementation phase they help you with debugging.
    * When you are finished they serve as mathematically precise documentation for your program.

-}

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

{-
    -- Function (boardContains) should satisfy this property
    -- Given an arbitrary board and manually taken a piece from it then the return value of function (boardContains) should always be True
    -- Not general
    prop_boardContains :: Board -> Property
    prop_boardContains b = boardContains b p 
            where
                ps = pieces b
                p = head ps 
-}            


-- Function (movePieceTo) should satisfy this property
-- Given an arbitrary board, a position (x,y) and an index, taken a pieces from the board's pieces at index 
-- Moving the piece and producing a newBoard through function (movePieceTo)
-- Then the newBoard should contain the newPiece with positions (x,y) i.e. being True 
-- There will be many discarded cases and few passed due to the preconditions 
prop_movePieceTo :: Board -> Int -> Int -> Int -> Property    
prop_movePieceTo b x y index = (isPosValid x y) && (index > 2 && index <= (length (pieces b))) ==> moved
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

{-  
    -- Function (isThisPieceAt) should satisfy this property
    -- Given an arbitrary board and taken a piece from the board's pieces then the return value of function (isThisPieceAt) should always be True 
    -- Not general
    prop_thisPieceAt :: Board -> Bool
    prop_thisPieceAt b = isThisPieceAt x y p
            where
                p = head (pieces b)
                (x,y) = piecePosition p
-}


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
prop_movesForPawn :: Board -> Bool 
prop_movesForPawn b = if (l == 0) then True else contain
    where 
        p = head[p | p <- (pieces b), pieceType p == Pawn]
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForPawn b p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Pawn col (x+nX) (y+nY)) | nX <- [-1,0,1], nY <- [-1,1]]


-- Function (findValidMovesForKing) should satisfy this property
-- Same reasoning as for prop_movesForPawn
-- Not general as it only tests the first board produced by function (findValidMovesForKing), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForKing :: Board -> Bool 
prop_movesForKing b = if (l == 0) then True else contain
    where 
        p = head[p | p <- (pieces b), pieceType p == King]
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForKing b p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece King col (x+nX) (y+nY)) | (nX,nY) <- allDirections]


-- Function (findValidMovesForQueen) should satisfy this property
-- There will be many discarded cases and few tests that pass due to precondition
-- Tests only the first board produced by function (findValidMovesForQueen), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForQueen :: Board -> Piece -> Property 
prop_movesForQueen b p = (pieceType p == Queen) ==> if (l == 0) then True else contain
    where 
        boardWithQueen = Board ((pieces b) ++ [p]) (toMove b)
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForQueen boardWithQueen p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Queen col (x+nX) (y+nY)) | (nX,nY) <- allDirections]


-- Function (findValidMovesForRook) should satisfy this property
-- There will be some discarded cases due to precondition
-- Tests only the first board produced by function (findValidMovesForRook), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForRook :: Board -> Piece -> Property 
prop_movesForRook b p = (pieceType p == Rook) ==> if (l == 0) then True else contain
    where 
        boardWithRook = Board ((pieces b) ++ [p]) (toMove b)
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForRook boardWithRook p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Rook col (x+nX) (y+nY)) | (nX,nY) <- orthogonals]


-- Function (findValidMovesForBishop) should satisfy this property
-- There will be some discarded cases due to precondition
-- Tests only the first board produced by function (findValidMovesForBishop), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForBishop :: Board -> Piece -> Property 
prop_movesForBishop b p = (pieceType p == Bishop) ==> if (l == 0) then True else contain
    where 
        boardWithBishop = Board ((pieces b) ++ [p]) (toMove b)
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForBishop boardWithBishop p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Bishop col (x+nX) (y+nY)) | (nX,nY) <- diagonals]


-- Function (findValidMovesForKnight) should satisfy this property
-- There will be some discarded cases due to precondition
-- Tests only the first board produced by function (findValidMovesForKnight), but by logic it still should be aplicable to the rest of the boards as well
prop_movesForKnight :: Board -> Piece -> Property 
prop_movesForKnight b p = (pieceType p == Knight) ==> if (l == 0) then True else contain
    where 
        boardWithKnight = Board ((pieces b) ++ [p]) (toMove b)
        (x,y) = piecePosition p
        col = pieceColor p
        newB = findValidMovesForKnight boardWithKnight p
        l = length newB
        newB1 = head newB
        contain = or [boardContains newB1 (Piece Knight col (x+nX) (y+nY)) | (nX,nY) <- knightMoves]


------------------------------------------------------------------------------------------- [FEN Properties] ---------------------------------------------------------------------------------------------------

pos :: FenParser -> (Int,Int)
pos (FenParser _ x y) = (x,y)

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

g1 = mkStdGen 7
g2 = mkStdGen 10
g3 = mkStdGen 15

-- The testing board for prop_moveRepresentation since the function (getMoveRepresentation) doesn't give accurate results if the board consist of duplicate positions
-- b is a valid Board in every aspect, hence why the prop_moveRepresentation would fail if run by quickCheck
b = Board [Piece Rook White 7 0,Piece Knight White 6 0,Piece Bishop White 5 0,Piece King White 4 0,Piece Queen White 3 0,Piece Bishop White 2 0,Piece Knight White 1 0,Piece Rook White 0 0,Piece Pawn White 7 1,Piece Pawn White 6 1,Piece Pawn White 5 1,Piece Pawn White 4 1,Piece Pawn White 2 1,Piece Pawn White 1 1,Piece Pawn White 0 1,Piece Pawn White 3 2,Piece Pawn Black 7 6,Piece Pawn Black 6 6,Piece Pawn Black 5 6,Piece Pawn Black 4 6,Piece Pawn Black 3 6,Piece Pawn Black 2 6,Piece Pawn Black 1 6,Piece Pawn Black 0 6,Piece Rook Black 7 7,Piece Knight Black 6 7,Piece Bishop Black 5 7,Piece King Black 4 7,Piece Queen Black 3 7,Piece Bishop Black 2 7,Piece Knight Black 1 7,Piece Rook Black 0 7] Black
prop_moveRepresentation b = s1 == s2
        where
            (n1,g4) = randomR (0,7) g1
            (x,y) = (map (piecePosition) (pieces b)) !! n1
            newB1 = Board [p | p <- (pieces b), (piecePosition p) /= (x,y)] (toMove b)
            p = last (pieces b)
            (px,py) = piecePosition p
            newP = Piece (pieceType p) (pieceColor p) x y
            removeP = [pi | pi <- (pieces newB1), pi /= p]
            newB2 = Board (removeP ++ [newP]) (toMove b)
            s1 = getMoveRepresentation newB1 newB2
            col1 = ['a'..'h'] !! px
            row1 = [1..8] !! py
            col2 = ['a'..'h'] !! x
            row2 = [1..8] !! y
            s2 = [col1] ++ (show row1) ++ [col2] ++ (show row2)


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





