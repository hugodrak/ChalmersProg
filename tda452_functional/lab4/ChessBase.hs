module ChessBase where 
import Data.Maybe

data Color = White | Black
    deriving (Show, Eq)

data PieceType = Pawn | King | Queen | Knight | Bishop | Rook
    deriving (Show,Eq)

data Piece = Piece PieceType Color  Int Int
    deriving (Show, Eq)
    

data Board = Board [Piece] Color
    deriving (Show, Eq)

toMove :: Board -> Color
toMove (Board _ color) = color

notToMove :: Board -> Color
notToMove = otherColor . toMove

otherColor :: Color -> Color
otherColor c | c == Black = White
             | c == White = Black
             
isPieceOfColor :: Color -> Piece -> Bool
isPieceOfColor c (Piece _ col _ _) = c==col

piecePosition :: Piece -> (Int,Int)
piecePosition (Piece _ _ x y) = (x,y)

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
          

movePieceTo :: Board -> Piece -> Int -> Int -> Board
movePieceTo (Board pieces turn) piece x y = Board (newPiece:boardWithPieceRemoved) turn
    
    where boardWithPieceRemoved = filter (not . isThisPieceAt x y) $ filter (/=piece) pieces
          
          newPiece = Piece typ color x y
          
          (color, typ) = case piece of
                              (Piece t col _ _) -> (col,t)


tryMoveTo :: Board -> Piece -> Int -> Int -> Maybe Board
tryMoveTo board piece x y | isSpaceOccupied board x y = Nothing
                          | otherwise = Just $ movePieceTo board piece x y
                              
                              

findAllValidMoves :: Board -> [Board]
findAllValidMoves board = concat $ map (findValidMovesForPiece board) (myPieces board)

--                        current board
findValidMovesForPiece :: Board -> Piece -> [Board]

findValidMovesForPiece board piece =  (subfunction piece) board piece
    
    where subfunction (Piece t _ _ _) = case (t) of
                                Pawn -> findValidMovesForPawn
                                King -> findValidMovesForKing
                                _ -> findNoMoves
          findNoMoves _ _= [] 
                        


isSpaceOccupied board x y = any (isThisPieceAt x y) (pieces board)
isSpaceOccupiedByColor board color x y = any (isThisPieceAt x y) (piecesOfColor board color)
getPieceAt (Board pieces _) x y = case maybePiece of
                            (piece:_) -> Just piece
                            otherwise -> Nothing
            where maybePiece = filter (isThisPieceAt x y) pieces

isThisPieceAt x y piece = piecePosition piece == (x,y)

pickPiece (Board pieces _) n = pieces !! n


tryCaptureAt :: Board -> Piece -> Int -> Int -> Maybe Board
tryCaptureAt board piece x y | isSpaceOccupiedByColor board (otherColor $ toMove board) x y 
                                    = Just $ movePieceTo board piece x y
                             | otherwise = Nothing

--                                               maxMoves dx     dy     
tryMoveOrCaptureInDirection :: Board -> Piece -> Int -> (Int,Int) -> [Board]
tryMoveOrCaptureInDirection board piece maxMoves dPos= tryMoveOrCaptureInDirection' board piece dPos 1 maxMoves


-- 
tryMoveOrCaptureInDirection' :: Board -> Piece -> (Int,Int) -> Int -> Int -> [Board]          
tryMoveOrCaptureInDirection' _ _ _ currentMoves maxMoves | currentMoves > maxMoves = []
tryMoveOrCaptureInDirection' board piece (dx,dy) currentMoves maxMoves
    | not $ isPosValid newX newY = [] -- outside board stop searching
    | occupiedByMe = [] -- cannot move here, stop searhing
    
    -- occupiedByOther, Capture The piece but then stop searching
    | occupiedByOther = [moveThere]
    -- not occupied, move there but also continue searching in direction
    | otherwise = moveThere: tryMoveOrCaptureInDirection' board piece (dx,dy) (currentMoves+1) maxMoves
                        
    where newX = curX + dx * currentMoves
          newY = curY + dy * currentMoves
          (curX,curY) = piecePosition piece
          moveThere = movePieceTo board piece newX newY
          
          occupiedByMe = isSpaceOccupiedByColor board (toMove board) newX newY
          occupiedByOther = isSpaceOccupiedByColor board (notToMove board) newX newY



                             
findValidMovesForPawn :: Board -> Piece -> [Board]
findValidMovesForPawn board piece = catMaybes $
                            tryMoveSingleForward:tryMoveDoubleForward:tryCaptureLeft:tryCaptureRight:[]

    where forwardDir = if isPieceOfColor White piece then 1 else (-1)
          startRow = if isPieceOfColor White piece then 1 else 6
          (x,y) = piecePosition piece
          
          tryMoveSingleForward = tryMoveTo board piece x (y+forwardDir)
          tryMoveDoubleForward = if y == startRow && (not $ isSpaceOccupied board x (y+forwardDir)) 
                                    then tryMoveTo board piece x (y+2*forwardDir)
                                    else Nothing
          
          tryCaptureLeft = tryCaptureAt board piece (x-1) (y+forwardDir)
          tryCaptureRight = tryCaptureAt board piece (x+1) (y+forwardDir)
          
findValidMovesForKing :: Board -> Piece -> [Board]
findValidMovesForKing board piece = concat $ map (tryMoveOrCaptureInDirection board piece 1) [(dx,dy) |dx<-[(-1),0,1], dy<-[(-1),0,1], (dx/=0) || (dy/=0)]



      
