import Test.QuickCheck
import Data.Maybe

import ChessBase

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
    -- The arbitrary for the board that only produces a board with 32 random pieces 
    instance Arbitrary Board where
        arbitrary = do
                    c <- arbitrary
                    p <- vectorOf 32 genPiece
                    return (Board p c)
-}


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