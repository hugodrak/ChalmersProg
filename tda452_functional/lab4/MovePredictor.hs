module MovePredictor where
import System.Random (randomRIO)

import ChessBase


selectRandomMove :: Board -> IO (Board)
selectRandomMove board = do
                            let availableMoves = concat $ map (findValidMovesForPiece board) (myPieces board)
                            indextoPick <- randomRIO (0, length availableMoves - 1)
                            let selected = availableMoves !! indextoPick
                            return selected
                                            
