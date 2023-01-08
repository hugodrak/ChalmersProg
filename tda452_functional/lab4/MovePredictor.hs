module MovePredictor where
import System.Random (random,StdGen,randomR)
import Data.List (maximumBy)
import Control.Parallel.Strategies


import ChessBase

-- Represent a board which has a scored assigned to it. Can be ordered based on score
--                             board score
data RatedBoard = RatedBoard Board Double

rating :: RatedBoard -> Double
rating (RatedBoard _ s) = s

instance Eq RatedBoard where
    s1 == s2 = rating s1 == rating s2

instance Ord RatedBoard where
    compare s1 s2 = compare (rating s1) (rating s2)

-- Add additional score to an already scoredboard
addScore :: RatedBoard -> Double -> RatedBoard
addScore (RatedBoard board s) toAdd = RatedBoard board (s+toAdd)

-- Out of a list of rated boards, select the one with the best rating
bestBoard :: [RatedBoard] -> Board
bestBoard ratings = result
    where b = maximum ratings -- Select the best board
          result = case b of RatedBoard board _ -> board

          
-- Calculate how much the pieces on the board is worth. Each piece is worth a different amount. The materialValue of the opponent is treated as negative.
-- By setting important pieces to a high value the engine is incentivised to capture this peices, (and not lose it's own)
materialValue :: Color -> Board  -> Double
materialValue inFavorOf board = fromIntegral totalScore
    where   totalScore = scoreOfColor inFavorOf - scoreOfColor (otherColor inFavorOf)
            scoreOfColor color = sum $ map pieceScore $ piecesOfColor board color
        
            pieceScore piece = case pieceType piece of
                King -> 1000
                Queen -> 10
                Rook -> 5
                Bishop -> 4
                Knight -> 3
                Pawn -> 1
          
-- We dont detect checkmate. So loosing your king should be heavily penalized to make the engine avoid it at all cost
penalizeMissingKing :: Color -> Board -> Double
penalizeMissingKing color board | hasKing = 0
                                | otherwise = -10000
    where hasKing = any (==King) $ map pieceType $ piecesOfColor board color 
            


-- We should penalize the engine for keeping pieces en the back rank. This should incentivise the engine to move the pieces to a (hopefully) more usefull square.
backRankPenaltly = -0.5
    
penalizePiecesOnBackRank :: Color -> Board -> Double
penalizePiecesOnBackRank color board  = backRankPenaltly * (fromIntegral $ length $ filter isOnBackRank (piecesOfColor board color))


isOnBackRank :: Piece -> Bool
isOnBackRank piece | typ == Pawn = False
                    | typ == King = False
                    | y == backrank = True
                    | otherwise = False
                where typ = pieceType piece
                      (_,y) = piecePosition piece
                      backrank = case pieceColor piece of
                                White -> 0
                                Black -> 7
    
          

-- Calculate the rating of a board. This is a sum of a bunch of evaluations. 
-- We can make a better engine by adding more evaluations which each takes into consideration a different aspect of the game
rateBoard ::  Color -> Board -> RatedBoard
rateBoard inFavorOf board  = RatedBoard board totalRating
    where totalRating = sum $ map (\scoreFunc -> scoreFunc inFavorOf board) ratingFunctions
          
          ratingFunctions = [materialValue, penalizePiecesOnBackRank]--, penalizeMissingKing          ]
    

    

          
-- Method of selecting a board purely random
selectRandomMove :: Board -> StdGen -> Board
selectRandomMove board g = selected
    where availableMoves = concat $ map (findValidMovesForPiece board) (myPieces board)
          (indextoPick,_) =  randomR (0, length availableMoves - 1) g
          selected = availableMoves !! indextoPick
          
-- Method of selecing a move based on if it manage to capture an opposing piece.
-- Not really good as this engine will eagerly sacrifice its own queen for a pawn.
selectGreedyCapture :: Board -> StdGen -> Board
selectGreedyCapture board g = bestBoard scoresWithRandom
    where availableMoves = findAllValidMoves board
          playerColor = toMove board
                                
          scores = map (rateBoard playerColor) availableMoves
                                
          scoresWithRandom = addNoiseToBoards scores g
                                

-- Add a random rating-noise to each rated board.
addNoiseToBoards :: [RatedBoard] -> StdGen -> [RatedBoard]
addNoiseToBoards scores g = map (\(s,n) -> addScore s n) $ zip scores (noise g)

-- Generates an infinite list of random doubles in the range [0-1]
noise  :: StdGen  -> [Double]
noise g = randomVal:noise g'
    where (randomVal, g') = random g

 

-- Method of selecting a move by generating all possible continuations of depth N
-- Assume the engine plays the best rated move and then the player respond with the best move for them
recursionDepth = 3

recursionRating :: Board -> StdGen -> Board
recursionRating board g = bestBoard scoresWithRandom
        where availableMoves = findAllValidMoves board
              playerColor = toMove board
                                
              rating = parMap rdeepseq (recursionRating' playerColor recursionDepth) availableMoves
                                
              scores = zipWith RatedBoard availableMoves rating
                                
              scoresWithRandom = addNoiseToBoards scores g

                                
recursionRating' :: Color -> Int -> Board -> Double
                -- We've reached the recursion depth limit. Rate the board.
recursionRating' inFavorOf 0 board = rating $ rateBoard inFavorOf board
                -- The rating is assuming the oppnent plays the best available move for them.
recursionRating' inFavorOf depth board = rating $ rateBoard inFavorOf counterMove
    where next = nextTurn board
          -- Find all move the other player could make in response to this board
          counterMoves = findAllValidMoves next
          -- Rate them by recursively calling recursionRating. But this time it's the other players turn to make the move.
          counterScores = map (recursionRating' (otherColor inFavorOf) (depth-1)) counterMoves
          -- Find the best move the opponent could make
          counterMove = bestBoard $ zipWith RatedBoard counterMoves counterScores

                                


            
            
            
            
