
import ChessBase
import FEN
import MovePredictor
import System.Environment
import Data.List
import System.Random (StdGen,newStdGen)


exampleFEN = "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

                                
printBoard :: Board -> IO ()
printBoard board = do
                    let s = formatBoard board
                    putStr s
                    
                    
              
printRandomContinuation :: Board -> IO ()
printRandomContinuation board = do
                                    stdGen <- newStdGen
                                    let continuation = selectRandomMove board stdGen
                                    printBoard continuation

                                    
main :: IO ()
main = do 
        args <- getArgs                  -- IO [String]
        progName <- getProgName          -- IO String
        {-putStrLn "The arguments are:"  
        mapM putStrLn args  
        putStrLn "The program name is:"  
        putStrLn progName
        -}
        
        let input = unwords args
        
        stdGen <- newStdGen
        
        let baseBoard = parseFEN input
        let continuation = recursionRating baseBoard stdGen
        
        let move = getMoveRepresentation baseBoard continuation
        
        putStr move

printEverything [] = do return ()       
printEverything (s:stuff) = do 
                                putStr s
                                printEverything stuff
