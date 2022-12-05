module FEN where
import ChessBase
import Data.Char
import Data.Maybe


-- rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1

parseFEN :: String -> Board
parseFEN fen = Board (parseBoard ((words fen) !! 0)) toPlay -- Only the first part is of interest, the rest is an-passant
    
    where parseBoard str = parseBoard' [] str 7 0
          
                       -- Current parsed board   rest of the fen    row    col    result
          parseBoard' :: [Piece]              -> String          -> Int -> Int -> [Piece]
          parseBoard' board "" _ _ = board -- Stop parseBoard
          parseBoard' board ('/':f) row _ = parseBoard' board f (row-1) 0  -- Continue to next row
          parseBoard' board (digit:f) row col | isDigit digit = parseBoard' board f row (col+ (digitToInt digit)) -- digit means we should skip N positions
          parseBoard' board (letter:f) row col = let updatedBoard = (letterToPiece letter (row,col)) ++ board in
                                                  parseBoard' updatedBoard f row (col+1)
    
          letterToPiece :: Char -> (Int,Int) -> [Piece]
          letterToPiece d _ | (toLower d) /= 'p' = []
          letterToPiece d (row, col)= [Piece (piecetype d) (color d) col row]
          
          color d = case (toLower d) == d of
                            True -> Black  --lowercase
                            False -> White -- uppercase
          piecetype d = case (toLower d) of
                            'p' -> Pawn
          toPlay = color $ head ((words fen) !! 1)
          
          
getMoveRepresentation :: Board -> Board -> String
getMoveRepresentation prevBoard newBoard  = 
    (colToLetter pieceMovedFrom) ++
    (rowToLetter pieceMovedFrom) ++
    (colToLetter pieceMovedTo) ++
    (rowToLetter pieceMovedTo) 
    
    
    where   moveColor = toMove prevBoard
        
        
            pieceMovedTo = head $ difference prevBoard newBoard
            pieceMovedFrom = head $ difference newBoard prevBoard
        
            xpos (Piece _ _ x y) = x
            ypos (Piece _ _ x y) = y
        
            difference prev after = filter (not . piecesContains (piecesOfColor prev moveColor)) $ piecesOfColor after moveColor
        
            rowToLetter piece = show ((ypos piece)+1) 
            colToLetter piece = case xpos piece of
                             0 -> "a"
                             1 -> "b"
                             2 -> "c"
                             3 -> "d"
                             4 -> "e"
                             5 -> "f"
                             6 -> "g"
                             7 -> "h"
                             
          
          
formatBoard :: Board -> String
formatBoard board  = unlines $ map formatRow  $ reverse [0..7]
    where formatRow y =  (show $ y+1) ++ concat [formatCell board x y| x <- [0..7]]
          
          
          
formatCell board x y = [case pieceMaybee of
                    Nothing -> '.'
                    Just _ -> transform letter
                            ]
                            
    where letter = case typ of
                    Pawn -> 'p'
        
          pieceMaybee = getPieceAt board x y
          piece = fromJust pieceMaybee
          (col,typ ) = case piece of (Piece t c _ _ ) -> (c,t)
          transform = if col == White then toUpper else id
          
          
          
          
