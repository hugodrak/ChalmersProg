module Sudoku where

import Test.QuickCheck
import Data.Char
import Data.List

------------------------------------------------------------------------------

-- | Representation of sudoku puzzles (allows some junk)
type Cell = Maybe Int -- a single cell
type Row  = [Cell]    -- a row is a list of cells

data Sudoku = Sudoku [Row] 
 deriving ( Show, Eq )

rows :: Sudoku -> [Row]
rows (Sudoku ms) = ms

-- | A sample sudoku puzzle maybe 
example :: Sudoku
example = 
    Sudoku
      [ [j 3,j 6,n  ,n  ,j 7,j 1,j 2,n  ,n  ]
      , [n  ,j 5,n  ,n  ,n  ,n  ,j 1,j 8,n  ]
      , [n  ,n  ,j 9,j 2,n  ,j 4,j 7,n  ,n  ]
      , [n  ,n  ,n  ,n  ,j 1,j 3,n  ,j 2,j 8]
      , [j 4,n  ,n  ,j 5,n  ,j 2,n  ,n  ,j 9]
      , [j 2,j 7,n  ,j 4,j 6,n  ,n  ,n  ,n  ]
      , [n  ,n  ,j 5,j 3,n  ,j 8,j 9,n  ,n  ]
      , [n  ,j 8,j 3,n  ,n  ,n  ,n  ,j 6,n  ]
      , [n  ,n  ,j 7,j 6,j 9,n  ,n  ,j 4,j 3]
      ]
  where
    n = Nothing
    j = Just

-- | A sample sudoku puzzle
example2 :: Sudoku
example2 =
    Sudoku
      [ [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      , [j 3,j 6,j 2,j 4,j 7,j 1,j 5,j 8,j 9]
      ]
  where
    n = Nothing
    j = Just


-- * A1

-- | allBlankSudoku is a sudoku with just blanks
allBlankSudoku :: Sudoku
allBlankSudoku = Sudoku allRows   
            where 
              allRows   = [row x | x <- row Nothing]
              row = replicate 9



-- * A2

-- | isSudoku sud checks if sud is really a valid representation of a sudoku
-- puzzle
isSudoku :: Sudoku -> Bool
isSudoku sudo              = allSudo
          where 
            maping         = map length $ rows sudo
            allSudo        = (length maping == 9) && (all (== 9) maping) &&
                             (all isValidCell $ concat (rows sudo))
            isValidCell Nothing = True
            isValidCell (Just n) = n > 0 && n < 10


-- * A3

-- | isFilled sud checks if sud is completely filled in,
-- i.e. there are no blanks
isFilled :: Sudoku -> Bool
isFilled sudo = notElem Nothing . concat $ rows sudo



------------------------------------------------------------------------------

-- * B1

-- | printSudoku sud prints a nice representation of the sudoku sud on
-- the screen
printSudoku :: Sudoku -> IO ()
printSudoku sudo | isSudoku sudo = putStr $ unlines $ map printRow (rows sudo) 
                 | otherwise     = putStr "Program error: Not a Sudoku!\n"
            where
              printRow row        = foldl (++) "" $ map printCell row
              printCell Nothing   = "." 
              printCell (Just n)  = show n


-- * B2

-- | readSudoku file reads from the file, and either delivers it, or stops
-- if the file did not contain a sudoku
readSudoku :: FilePath -> IO Sudoku
readSudoku path = do 
                sudoLines <- readFile path
                let sudoWords = words sudoLines
                return (intoSudoku sudoWords)
      where 
        intoSudoku []     = Sudoku []
        intoSudoku xs     = Sudoku [map intoCell x | x <- xs]  
        intoCell '.'      = Nothing
        intoCell n        = Just $ digitToInt n

------------------------------------------------------------------------------

-- * C1

-- | cell generates an arbitrary cell in a Sudoku
cell :: Gen (Cell)
cell = do 
  let j = elements $ sequence $ Just [1..9]
  let n = return Nothing
  frequency [(3,j),(7,n)]



-- * C2

-- | an instance for generating Arbitrary Sudokus
instance Arbitrary Sudoku where
  arbitrary = do 
            rs <- vectorOf 81 cell
            let sudo = makeSudo rs
            return $ Sudoku sudo
        where
          makeSudo [] = []
          makeSudo cs = take 9 cs:makeSudo (drop 9 cs) 


 -- hint: get to know the QuickCheck function vectorOf
 
-- * C3

prop_Sudoku :: Sudoku -> Bool
prop_Sudoku sudo = isSudoku sudo


  -- hint: this definition is simple!
  
------------------------------------------------------------------------------

type Block = [Cell] -- a Row is also a Cell


-- * D1

isOkayBlock :: Block -> Bool
isOkayBlock block = arr == nub arr    
        where 
          arr = [c | c <- block, c /= Nothing] 


-- * D2

blocks :: Sudoku -> [Block]
blocks sudo = r ++ transpose (r) ++ getAllCells
          where
            getAllCells = [getCell x y| x<- [0,3..6], y<-[0,3..6]]
            getCell blockx blocky = [(r !! y) !! x | x<-[blockx..(blockx+2)], y<-[blocky..(blocky+2)]]
            r = rows sudo


prop_blocks_lengths :: Sudoku -> Bool
prop_blocks_lengths sudo = length b == 27 && (all (==9) $ map length b)
    where b = blocks sudo

-- * D3

isOkay :: Sudoku -> Bool
isOkay sudo = all (isOkayBlock) $ blocks sudo 


---- Part A ends here --------------------------------------------------------
------------------------------------------------------------------------------
---- Part B starts here ------------------------------------------------------


-- | Positions are pairs (row,column),
-- (0,0) is top left corner, (8,8) is bottom left corner
type Pos = (Int,Int)

-- * E1

-- Loops through all y and x in (0,0)..(8,8) and if there is a blank there then return that coordinate
blanks :: Sudoku -> [Pos]
blanks sudoku = [
            (row,col) | row <- [0..8], col<-[0..8] , isBlank row col
            ]
    where isBlank r c = case (((rows sudoku) !! r) !! c) of
                                Nothing -> True
                                otherwise -> False

prop_blanks_allBlanks :: Bool
prop_blanks_allBlanks = length expected == 81 &&  expected == actual
    where expected = [(x,y) | x<-[0..8],y<-[0..8]]
          actual = blanks allBlankSudoku


-- * E2

(!!=) :: [a] -> (Int,a) -> [a]
xs !!= (whereToInsert,new) = [if i==whereToInsert then new else existing| (existing, i)<-zip xs [0..]]

prop_bangBangEquals_correct :: [Int] -> [Int] -> Int -> Bool 
prop_bangBangEquals_correct x y randomnumber = expected == (newList !!= ((length x), 0))
    -- Test so that it correctly replaces a number in the middle of some random lists
    where newList = x ++ [randomnumber] ++ y
          expected = x ++ [0] ++ y


-- * E3

update :: Sudoku -> Pos -> Cell -> Sudoku
update sudoku (row,col) new = Sudoku $ allRows !!= (row, newRow)
            where allRows = rows sudoku
                  newRow = ((rows sudoku) !! row) !!= (col, new)

prop_update_updated :: Int -> Int -> Bool
prop_update_updated row col | or [row<0,col<0,row>8,col>8] = True
                            | otherwise = actual == expected
    where actual = update allBlankSudoku (row,col) (Just 9)
          
          expected = Sudoku $ (replicate 9 blankRow) !!= (row, blankRow !!= (col, Just 9))
          blankRow = replicate 9 Nothing


------------------------------------------------------------------------------

-- * F1

solve :: Sudoku -> Sudoku
solve sudoku = head $ solve' sudoku (blanks sudoku)

solve' :: Sudoku -> [(Int, Int)] -> [Sudoku]
solve' sudoku [] = if isOkay sudoku then [sudoku] else []

solve' sudoku (pos:rest) | not $ isOkay sudoku = []
                       | otherwise = concat $ [solve' (update sudoku pos (Just i)) rest | i<- [1..9]]


-- * F2


-- * F3


-- * F4
