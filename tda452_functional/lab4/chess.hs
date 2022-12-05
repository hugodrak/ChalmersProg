import Data.Char

data Color = White | Black
    deriving (Show, Eq)

data PieceOwner = Me | Opponent
    deriving (Show, Eq)

data PieceType = Pawn | King
    deriving (Show,Eq)

data Piece = Piece PieceType PieceOwner Int Int
    deriving (Show, Eq)
    

type Board = [Piece]




exampleFEN = "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

--               Piece    current player    result
colorsToOwner :: Color -> Color ->       PieceOwner
colorsToOwner piece iPlay  = if (piece == iPlay) then Me else Opponent


parseFEN :: String -> Board
parseFEN fen = parseBoard ((words fen) !! 0) -- Only the first part is of interest, the rest is an-passant
    
    where parseBoard str = parseBoard' [] str 0 0
          
                       -- Current parsed board   rest of the fen    row    col    result
          parseBoard' :: Board                -> String          -> Int -> Int -> Board
          parseBoard' board "" _ _ = board -- Stop parseBoard
          parseBoard' board ('/':f) row _ = parseBoard' board f (row+1) 0  -- Continue to next row
          parseBoard' board (digit:f) row col | isDigit digit = parseBoard' board f row (col+ (digitToInt digit)) -- digit means we should skip N positions
          parseBoard' board (letter:f) row col = let updatedBoard = (letterToPiece letter (row,col)) ++ board in
                                                  parseBoard' updatedBoard f row (col+1)
    
          letterToPiece :: Char -> (Int,Int) -> [Piece]
          letterToPiece d _ | (toLower d) /= 'p' = []
          letterToPiece d (row, col)= [Piece (piecetype d) (colorsToOwner (color d) turn) col row]
          
          color d = case (toLower d) == d of
                            True -> Black  --lowercase
                            False -> White -- uppercase
          piecetype d = case (toLower d) of
                            'p' -> Pawn
          turn = color $ head ((words fen) !! 1)
          

whoStarts :: String -> Color
whoStarts "b" = Black
whoStarts "w" = White

movePieceTo :: Board -> Piece -> Int -> Int -> Board
movePieceTo board piece x y = newPiece:boardWithPieceRemoved
    
    where boardWithPieceRemoved = filter (/=piece) board
          
          newPiece = Piece typ color x y
          
          (color, typ) = case piece of
                              (Piece t col _ _) -> (col,t)




--                        current board            which way is forward (for moving pawns)
findValidMovesForPiece :: Board        -> Piece -> Int                                      -> [Board]

findValidMovesForPiece board piece forward = (subfunction piece) board piece forward
    
    
    
    where subfunction (Piece t _ _ _) = case (t) of
                                Pawn -> findValidMovesForPawn
                                _ -> error "herp derp"
                        


isSpaceOccupied board x y = any (isThisPieceAt x y)  board
getPieceAt board x y = case maybePiece of
                            (piece:_) -> Just piece
                            otherwise -> Nothing
            where maybePiece = filter (isThisPieceAt x y) board

isThisPieceAt x y (Piece _ _ x1 y1) = (x1,y1)==(x,y)
          

                        
findValidMovesForPawn :: Board -> Piece -> Int -> [Board]
findValidMovesForPawn board piece f = if isSpaceOccupied board newx newy then [] else [movePieceTo board piece newx newy]
    
    where (curx, cury) = case piece of (Piece _ _ x y) -> (x,y)
          newy = cury + f
          newx = curx
    

    
formatBoard :: Board -> String
formatBoard board  = unlines $ map formatRow [0..7]


    where formatRow y = concat [formatCell x y| x<-[0..7]]
          
          formatCell x y = case (getPieceAt board x y) of
                                Nothing -> "."
                                Just (Piece Pawn _ _ _) -> "p"

printBoard :: Board -> IO ()
printBoard board = do
                    let s = formatBoard board
                    putStr s
                    






