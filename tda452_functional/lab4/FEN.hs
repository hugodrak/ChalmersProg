module FEN where
import ChessBase
import Data.Char

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
          
          
get
          
          
formatBoard :: Board -> String
formatBoard board  = unlines $ map formatRow [0..7]
    where formatRow y = concat [formatCell x y| x <- [0..7]]
          
          formatCell x y = case (getPieceAt board x y) of
                                Nothing -> "."
                                Just (Piece Pawn _ _ _) -> "p"
