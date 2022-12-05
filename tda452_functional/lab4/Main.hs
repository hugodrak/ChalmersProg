
import ChessBase
import FEN
import MovePredictor

                                
                                
printBoard :: Board -> IO ()
printBoard board = do
                    let s = formatBoard board
                    putStr s
                    
                    
              
printRandomContinuation :: Board -> IO ()
printRandomContinuation board = do
                                    continuation <- selectRandomMove board
                                    printBoard continuation
