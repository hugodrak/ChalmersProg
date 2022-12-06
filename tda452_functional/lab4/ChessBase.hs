module ChessBase where 
import Data.Maybe

data Color = White | Black
    deriving (Show, Eq)

data PieceType = Pawn | King
    deriving (Show,Eq)

data Piece = Piece PieceType Color  Int Int
    deriving (Show, Eq)
    

data Board = Board [Piece] Color
    deriving (Show, Eq)

toMove :: Board -> Color
toMove (Board _ color) = color

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
          

movePieceTo :: Board -> Piece -> Int -> Int -> Board
movePieceTo (Board pieces turn) piece x y = Board (newPiece:boardWithPieceRemoved) turn
    
    where boardWithPieceRemoved = filter (/=piece) pieces
          
          newPiece = Piece typ color x y
          
          (color, typ) = case piece of
                              (Piece t col _ _) -> (col,t)


                              
                              


--                        current board
findValidMovesForPiece :: Board -> Piece -> [Board]

findValidMovesForPiece board piece = catMaybes $ (subfunction piece) board piece
    
    
    
    where subfunction (Piece t _ _ _) = case (t) of
                                Pawn -> findValidMovesForPawn
                                _ -> error "herp derp"
                        


isSpaceOccupied (Board pieces _) x y = any (isThisPieceAt x y) pieces
getPieceAt (Board pieces _) x y = case maybePiece of
                            (piece:_) -> Just piece
                            otherwise -> Nothing
            where maybePiece = filter (isThisPieceAt x y) pieces

isThisPieceAt x y (Piece _ _ x1 y1) = (x1,y1)==(x,y)

pickPiece (Board pieces _) n = pieces !! n

tryMoveTo :: Board -> Piece -> Int -> Int -> Maybe Board
tryMoveTo board piece x y | isSpaceOccupied board x y = Nothing
                          | otherwise = Just $ movePieceTo board piece x y

                        
findValidMovesForPawn :: Board -> Piece -> [Maybe Board]
findValidMovesForPawn board piece = tryMoveSingleForward:tryMoveDoubleForward:[]

    where forwardDir = if isPieceOfColor White piece then 1 else (-1)
          startRow = if isPieceOfColor White piece then 1 else 6
          (x,y) = piecePosition piece
          
          tryMoveSingleForward = tryMoveTo board piece x (y+forwardDir)
          tryMoveDoubleForward = if y == startRow 
                                    then tryMoveTo board piece x (y+2*forwardDir)
                                    else Nothing

    



      
