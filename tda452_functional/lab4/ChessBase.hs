module ChessBase where 
import Data.Maybe

data Color = White | Black
    deriving (Show, Eq)

data PieceType = Pawn | King | Queen | Knight | Bishop | Rook
    deriving (Show,Eq)
    
--                                  x   y   = ...  (column) (row)
data Piece = Piece PieceType Color  Int Int
    deriving (Show, Eq)
    
-- A board containing all list of all pieces and who is next to move.
data Board = Board [Piece] Color
    deriving (Show, Eq)

toMove :: Board -> Color
toMove (Board _ color) = color

notToMove :: Board -> Color
notToMove = otherColor . toMove

otherColor :: Color -> Color
otherColor c | c == Black = White
             | c == White = Black
             
nextTurn :: Board -> Board
nextTurn board = Board (pieces board) (notToMove board)
             
isPieceOfColor :: Color -> Piece -> Bool
isPieceOfColor c p = c == pieceColor p

piecePosition :: Piece -> (Int,Int)
piecePosition (Piece _ _ x y) = (x,y)

pieceType :: Piece -> PieceType
pieceType (Piece typ _ _ _) = typ

pieceColor :: Piece -> Color
pieceColor (Piece _ col _ _) = col

pieces :: Board -> [Piece]
pieces (Board p _) = p

piecesOfColor :: Board -> Color -> [Piece]
piecesOfColor (Board pieces _) color = filter (isPieceOfColor color) pieces 

myPieces :: Board -> [Piece]
myPieces board = piecesOfColor board (toMove board)

piecesContains :: [Piece] -> Piece -> Bool
piecesContains pieces piece = any (==piece) pieces

boardContains :: Board -> Piece -> Bool
boardContains board piece = piecesContains (pieces board) piece

isPosValid :: Int -> Int -> Bool
isPosValid x y = (x>=0) && (x<=7) && (y>=0) && (y<=7)  
          
-- Move a piece to a new position. If the new position is occupied - capture and remove that piece
movePieceTo :: Board -> Piece -> Int -> Int -> Board
movePieceTo (Board pieces turn) piece x y = Board (newPiece:boardWithPieceRemoved) turn
                                        
                                        -- capture the piece                remove the piece from the old position
    where boardWithPieceRemoved = filter (not . isThisPieceAt x y) $ filter (/=piece) pieces
          
          newPiece = Piece typ col x y
          col = pieceColor piece
          typ = pieceType piece

-- Try move a piece to a new position without capturing. If the target position is occupied by either color then return Nothing. Otherwise Just the new position.
tryMoveTo :: Board -> Piece -> Int -> Int -> Maybe Board
tryMoveTo board piece x y | isSpaceOccupied board x y = Nothing
                          | otherwise = Just $ movePieceTo board piece x y
                              


diagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]
orthogonals = [(-1,0),(1,0),(0,-1),(0,1)]
allDirections = diagonals ++ orthogonals

-- I'm really proud of this one :D
knightDirections = [(dx,dy) | dx <- [-2,-1,1,2], dy<-[-2,-1,1,2], (abs dx + abs dy) == 3]

-- The moves for each piece (except pawns) is represented as which directions and maximum 
data MoveLength = Single | Unlimited




-- The moves for all pieces (but pawns) is the sum of trying to move in all legal directions for the pieceType
--                    [(dx ,dy )]
moves :: Piece -> ([(Int,Int)],MoveLength)
moves piece = case pieceType piece of
                      King   -> (allDirections, Single) 
                      Queen  -> (allDirections, Unlimited)
                      Knight -> (knightDirections, Single)
                      Rook   -> (orthogonals, Unlimited)
                      Bishop -> (diagonals, Unlimited)
                      _      -> error "Pawns are wierd..."

-- The main method in this files. Find all resulting boards resulting from all available currentMoves
-- Note that this includes "invalid" boards in which the king are in check
                              
findAllValidMoves :: Board -> [Board]
findAllValidMoves board = concatMap (findValidMovesForPiece board) (myPieces board)

                      
                      
-- Find all available moves for a given piece
--                        current board
findValidMovesForPiece :: Board -> Piece -> [Board]

findValidMovesForPiece board piece | pieceType piece == Pawn = findValidMovesForPawn board piece
                                   | otherwise = let (directions, moveLength) = moves piece 
                                     in concatMap (tryMoveOrCaptureInDirection board piece moveLength) directions

-- If there is any piece at a specific position
isSpaceOccupied board x y = any (isThisPieceAt x y) (pieces board)
isSpaceOccupiedByColor board color x y = any (isThisPieceAt x y) (piecesOfColor board color)


-- Try get the piece at a given position. If there is no piece there, return Nothing
getPieceAt (Board pieces _) x y = case maybePiece of
                            (piece:_) -> Just piece
                            otherwise -> Nothing
            where maybePiece = filter (isThisPieceAt x y) pieces

isThisPieceAt x y piece = piecePosition piece == (x,y)


-- Move to position. There must be a opponent piece at the target position.
tryCaptureAt :: Board -> Piece -> Int -> Int -> Maybe Board
tryCaptureAt board piece x y | isSpaceOccupiedByColor board (otherColor $ toMove board) x y 
                                    = Just $ movePieceTo board piece x y
                             | otherwise = Nothing

                             
-- Try move or capture in a direction. The direction is given by (dx,dy). If that space is not occupied also try moving to the next space in that direction. This returns all the new boards generated by moving the piece in the direction. For the king it will at most be 1 board. But for the rook it might be up to 7.
--                                               maxMoves (dx, dy)     
tryMoveOrCaptureInDirection :: Board -> Piece -> MoveLength -> (Int,Int) -> [Board]
tryMoveOrCaptureInDirection board piece Unlimited dPos = tryMoveOrCaptureInDirection' board piece dPos 1
tryMoveOrCaptureInDirection board piece Single (dx,dy) 
    | not $ isPosValid newX newY = []
    | occupiedByMe = []
    | otherwise = [movePieceTo board piece newX newY]
    where newX = curX + dx
          newY = curY + dy
          (curX,curY) = piecePosition piece 
          occupiedByMe = isSpaceOccupiedByColor board (toMove board) newX newY


   

tryMoveOrCaptureInDirection' board piece (dx,dy) currentMoves
    | not $ isPosValid newX newY = [] -- outside board stop searching
    | occupiedByMe = [] -- cannot move here, stop searching
    
    -- occupiedByOther, Capture The piece but then stop searching
    | occupiedByOther = [moveThere]
    -- not occupied, move there but also continue searching in the direction, with currentMoves incremented
    | otherwise = moveThere: tryMoveOrCaptureInDirection' board piece (dx,dy) (currentMoves+1)
                        
    where newX = curX + dx * currentMoves
          newY = curY + dy * currentMoves
          (curX,curY) = piecePosition piece
          moveThere = movePieceTo board piece newX newY
          
          occupiedByMe = isSpaceOccupiedByColor board (toMove board) newX newY
          occupiedByOther = isSpaceOccupiedByColor board (notToMove board) newX newY



-- This is super honky-wonky, I'm very sorry for whoever have to look at this. Pawn has alot of special moves and cannot be implmented as the other pieces.
findValidMovesForPawn :: Board -> Piece -> [Board]
findValidMovesForPawn board piece = catMaybes $
                            tryMoveSingleForward:tryMoveDoubleForward:tryCaptureLeft:tryCaptureRight:[]

    where forwardDir = if isPieceOfColor White piece then 1 else (-1)
          startRow = if isPieceOfColor White piece then 1 else 6
          (x,y) = piecePosition piece
          tryMoveSingleForward = if isPosValid x (y+forwardDir) then tryMoveTo board piece x (y+forwardDir) else Nothing
          tryMoveDoubleForward = if y == startRow && (not $ isSpaceOccupied board x (y+forwardDir)) 
                                    then tryMoveTo board piece x (y+2*forwardDir)
                                    else Nothing
          
          tryCaptureLeft = tryCaptureAt board piece (x-1) (y+forwardDir)
          tryCaptureRight = tryCaptureAt board piece (x+1) (y+forwardDir)

          

      
