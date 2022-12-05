import Data.Char

data Color = White | Black
    deriving (Show, Eq)

data PieceType = Pawn | King
    deriving (Show,Eq)

data Piece = Piece PieceType Color  Int Int
    deriving (Show, Eq)
    

data Board = Board [Piece] Color
    deriving (Show, Eq)



exampleFEN = "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"


parseFEN :: String -> Board
parseFEN fen = Board (parseBoard ((words fen) !! 0)) toPlay -- Only the first part is of interest, the rest is an-passant
    
    where parseBoard str = parseBoard' [] str 0 0
          
                       -- Current parsed board   rest of the fen    row    col    result
          parseBoard' :: [Piece]              -> String          -> Int -> Int -> [Piece]
          parseBoard' board "" _ _ = board -- Stop parseBoard
          parseBoard' board ('/':f) row _ = parseBoard' board f (row+1) 0  -- Continue to next row
          parseBoard' board (digit:f) row col | isDigit digit = parseBoard' board f row (col+ (digitToInt digit)) -- digit means we should skip N positions
          parseBoard' board (letter:f) row col = let updatedBoard = (letterToPiece letter (row,col)) ++ board in
                                                  parseBoard' updatedBoard f row (col+1)
    
          letterToPiece :: Char -> (Int,Int) -> [Piece]
          letterToPiece d _ | (toLower d) /= 'p' = []
          letterToPiece d (row, col)= [Piece (piecetype d) (color d) col row]
          
          color d = case (toLower d) == d of
                            True -> White  --lowercase
                            False -> Black -- uppercase
          piecetype d = case (toLower d) of
                            'p' -> Pawn
          toPlay = color $ head ((words fen) !! 1)
          

whoStarts :: String -> Color
whoStarts "b" = Black
whoStarts "w" = White

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

printBoard :: Board -> IO ()
printBoard board = do
                    let s = formatBoard board
                    putStr s
                    
