module FEN where
import ChessBase
import Data.Char
import Data.Maybe


--FEN string look like this:
-- pieces                                         who to play    junk we dont care about
--"rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR   b             KQkq - 0 1"
--   /\             /\                /\
--   ||             ||                ||
-- Piece    8 Empty positions         Goto next row


-- We wanna parse it using foldl. Define a state to hold the current parser state

--                                  x  y
data FenParser = FenParser [Piece] Int Int
    deriving (Show)

result :: FenParser -> [Piece]
result (FenParser pieces _ _) = pieces

initialParser = FenParser [] 0 7

-- Parse a single letter
parseFenLetter :: FenParser -> Char -> FenParser
parseFenLetter (FenParser currentPieces x y) char | char == '/' = FenParser currentPieces 0 (y-1) -- Continue to next row
                                                  | isDigit char = FenParser currentPieces (x+digitToInt char) y -- skip this many m positions
                                                  | otherwise = FenParser (newPiece:currentPieces) (x+1) y -- Parse piece
    where newPiece = Piece typ color x y
          color = case (toLower char) == char of
                            True -> Black  --lowercase
                            False -> White -- uppercase
          typ = case (toLower char) of
                            'p' -> Pawn
                            'q' -> Queen
                            'r' -> Rook
                            'b' -> Bishop
                            'n' -> Knight
                            'k' -> King

parseFEN :: String -> Board
parseFEN fen = Board pieces whoStarts 
    
    where pieces = result $ foldl parseFenLetter initialParser piecesStr
          whoStarts = case whoStartsStr of
                            "w" -> White
                            "b" -> Black
          
          -- Only the first part is of interest, the rest is an-passant
          piecesStr = (words fen) !! 0
          whoStartsStr = (words fen) !! 1
          
          
          
-- Get a move representation by comparing two boards
-- If a piece moves from g2 to g3 the move representation is "g2g3"
getMoveRepresentation :: Board -> Board -> String
getMoveRepresentation prevBoard newBoard  = 
    (colToLetter pieceMovedFrom) ++
    (rowToLetter pieceMovedFrom) ++
    --(if isCapture then "x" else "") ++
    (colToLetter pieceMovedTo) ++
    (rowToLetter pieceMovedTo) 
    
    
    where   moveColor = toMove prevBoard
        
        
            pieceMovedTo = head $ difference prevBoard newBoard
            pieceMovedFrom = head $ difference newBoard prevBoard
        
            xpos :: Piece -> Int
            ypos :: Piece -> Int
            xpos p = fst $ piecePosition p
            ypos p = snd $ piecePosition p
            
            difference prev after = filter (not . piecesContains (piecesOfColor prev moveColor)) $ piecesOfColor after moveColor
        
            isCapture = length (pieces prevBoard) /= length (pieces newBoard)
        
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
                    Queen  -> 'q'
                    Rook -> 'r'
                    Bishop -> 'b'
                    Knight -> 'n'
                    King -> 'k'
        
          pieceMaybee = getPieceAt board x y
          piece = fromJust pieceMaybee
          (col,typ ) = case piece of (Piece t c _ _ ) -> (c,t)
          transform = if col == White then toUpper else id
          
          
          
          
