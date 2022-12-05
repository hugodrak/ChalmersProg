module ChessBase where 
import System.Random (randomRIO)


data Color = White | Black
    deriving (Show, Eq)

data PieceType = Pawn | King
    deriving (Show,Eq)

data Piece = Piece PieceType Color  Int Int
    deriving (Show, Eq)
    

data Board = Board [Piece] Color
    deriving (Show, Eq)

isPieceOfColor :: Color -> Piece -> Bool
isPieceOfColor c (Piece _ col _ _) = c==col
    
myPieces :: Board -> [Piece]
myPieces (Board pieces turn) = filter (isPieceOfColor turn) pieces



          

movePieceTo :: Board -> Piece -> Int -> Int -> Board
movePieceTo (Board pieces turn) piece x y = Board (newPiece:boardWithPieceRemoved) turn
    
    where boardWithPieceRemoved = filter (/=piece) pieces
          
          newPiece = Piece typ color x y
          
          (color, typ) = case piece of
                              (Piece t col _ _) -> (col,t)




--                        current board
findValidMovesForPiece :: Board -> Piece -> [Board]

findValidMovesForPiece board piece = (subfunction piece) board piece
    
    
    
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

                        
findValidMovesForPawn :: Board -> Piece -> [Board]
findValidMovesForPawn board piece = if isSpaceOccupied board newx newy then [] else [movePieceTo board piece newx newy]
    
    where (curx, cury,color) = case piece of (Piece _ col x y) -> (x,y,col)
          newy = cury + moveDir
          newx = curx
          moveDir = if color == White then 1 else (-1)
    

    
formatBoard :: Board -> String
formatBoard board  = unlines $ map formatRow [0..7]
    where formatRow y = concat [formatCell x y| x <- [0..7]]
          
          formatCell x y = case (getPieceAt board x y) of
                                Nothing -> "."
                                Just (Piece Pawn _ _ _) -> "p"

selectRandomMove :: Board -> IO (Board)
selectRandomMove board = do
                            let availableMoves = concat $ map (findValidMovesForPiece board) (myPieces board)
                            indextoPick <- randomRIO (0, length availableMoves - 1)
                            let selected = availableMoves !! indextoPick
                            return selected
                                            
printBoard :: Board -> IO ()
printBoard board = do
                    let s = formatBoard board
                    putStr s
                    
printRandomContinuation :: Board -> IO ()
printRandomContinuation board = do
                                    continuation <- selectRandomMove board
                                    printBoard continuation
