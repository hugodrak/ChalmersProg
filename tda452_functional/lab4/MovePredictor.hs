module MovePredictor where
import System.Random (randomRIO, random,StdGen,newStdGen)
import Data.List (maximumBy)

import ChessBase

-- Represent a board which has a scored assigned to it. Can be ordered based on score
--                             board score
data ScoredBoard = ScoredBoard Board Double

score :: ScoredBoard -> Double
score (ScoredBoard _ s) = s

instance Eq ScoredBoard where
    s1 == s2 = score s1 == score s2

instance Ord ScoredBoard where
    compare s1 s2 = compare (score s1) (score s2)

    
addScore :: ScoredBoard -> Double -> ScoredBoard
addScore (ScoredBoard board s) toAdd = ScoredBoard board (s+toAdd)

bestBoard :: [ScoredBoard] -> Board
bestBoard scores = bestBoard
    where b = maximum scores
          bestBoard = case b of ScoredBoard board _ -> board


pieceScore :: Piece -> Int
pieceScore piece = score
    where score = case pieceType piece of
            King -> 1000
            _ -> 10
          
          
scoreBoard :: Board -> ScoredBoard
scoreBoard board = ScoredBoard board totalScore
    where totalScore = fromIntegral $ scoreOfColor (toMove board) - scoreOfColor (notToMove board)
          scoreOfColor color = sum $ map pieceScore $ piecesOfColor board color
          
          

selectRandomMove :: Board -> IO (Board)
selectRandomMove board = do
                            let availableMoves = concat $ map (findValidMovesForPiece board) (myPieces board)
                            indextoPick <- randomRIO (0, length availableMoves - 1)
                            let selected = availableMoves !! indextoPick
                            return selected
                                            
selectGreedyCapture :: Board -> IO (Board)
selectGreedyCapture board = do
                                g <- newStdGen
                                let availableMoves = findAllValidMoves board
                                
                                let scores = map scoreBoard availableMoves
                                
                                let scoredWithRandom = map (\(s,n) -> addScore s n) $ zip scores (noise g)
                                
                                return $ bestBoard scoredWithRandom
                                
                                    
                                
                                
                                            
                                    
noise  :: StdGen  -> [Double]
noise g = randomVal:noise g'
    where (randomVal, g') = random g
            

