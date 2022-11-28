module BlackJack where
import Cards
import RunGame
import Test.QuickCheck
import System.Random


hand2 :: Hand
hand2 = Add (Card (Numeric 2) Hearts)
            (Add (Card Jack Spades) Empty)

-------------------- [A0] ----------------------

sizeSteps :: [Integer]
sizeSteps = [ size hand2
            , size (Add (Card (Numeric 2) Hearts)
                        (Add (Card Jack Spades) Empty))
            , 1 + size (Add (Card Jack Spades) Empty)
            , 1 + 1 + size Empty
            , 1 + 1 + 0
            ,2]



-------------------- [A1] ---------------------------

displayCard :: Card -> String 
displayCard (Card (Numeric n) s) = show n ++ " of " ++ show s ++ "\n"
displayCard (Card r s)           = show r ++ " of " ++ show s ++ "\n"


display :: Hand -> String
display Empty = ""
display (Add card hand) = displayCard card ++ display hand


--------------------- [A2] --------------------------

initialValue :: Hand -> Integer -> Integer
initialValue Empty  _           = 0
initialValue (Add card hand) aceValue = valueRank (rank card) + initialValue hand aceValue
                    where 
                        valueRank :: Rank -> Integer
                        valueRank (Numeric n) = n
                        valueRank Ace = aceValue
                        valueRank _ = 10


value :: Hand -> Integer
value hand | x <= 21   = x
           | otherwise = initialValue hand 1
        where 
            x = initialValue hand 11
                   

-------------------- [A3] ----------------------------

gameOver :: Hand -> Bool 
gameOver hand = value hand > 21 


-------------------- [A4] ----------------------------

winner :: Hand -> Hand -> Player 
winner player bank | gameOver player = Bank
                   | gameOver bank = Guest
                   | value player > value bank = Guest
                   | otherwise = Bank

-------------------- [B1] --------------------------

(<+) :: Hand -> Hand -> Hand
(<+) Empty hand2            = hand2
(<+) (Add card Empty) hand2 = Add card hand2
(<+) (Add card hand1) hand2 = Add card (hand1 <+ hand2)


prop_onTopOf_assoc :: Hand -> Hand -> Hand -> Bool
prop_onTopOf_assoc p1 p2 p3 =
    p1<+(p2<+p3) == (p1<+p2)<+p3


prop_size_onTopOf :: Hand -> Hand -> Bool
prop_size_onTopOf p1 p2 =
    size p1 + size p2 == size (p1 <+ p2)

-------------------- [B2] --------------------------

fullDeck :: Hand
fullDeck = foldr Add Empty cards
           where cards = [Card rank suit |
                     suit <- [Clubs, Hearts, Spades, Diamonds],
                     rank <- [Numeric x | x <- [2..10]] ++ [Jack, Queen, King, Ace]
                     ]

prop_fullDeckSize = size fullDeck == 52

---------------------- [B3] --------------------------

-- Draw the Nth card. drawNthCard [5J, 6S, 10J] 1 = (6s, [5J, 10J])
drawNth :: Hand -> Hand -> Integer -> (Hand, Hand)
drawNth Empty _ _ = error "draw: the deck is empty"
drawNth (Add card deck) hand 0 = (deck, Add card hand)
drawNth (Add card deck) hand n = (Add card smallerDeck, biggerHand)
            where (smallerDeck, biggerHand) = drawNth deck hand (n-1)


-- Draw a card in the range [0...1] 0 picks the first card, 0.3333 a card 1/3 in the deck. When >= 1.0 pick the last card
drawNthDouble :: Hand-> Hand -> Double -> (Hand, Hand)
drawNthDouble deck hand n | n >= 1.0 = drawNth deck hand last
    where last = (size deck) - 1
drawNthDouble deck hand n = drawNth deck hand cardToPick
    where cardToPick = floor (n * (size deck))

    
draw :: Hand -> Hand -> (Hand, Hand)
draw deck hand = drawNth deck hand 0

----------------------- [B4] --------------------------

playBank :: Hand -> Hand
playBank deck = snd (playBankHelper deck Empty)

playBankHelper :: Hand -> Hand-> (Hand, Hand)
playBankHelper deck hand | value hand >= 16 = (deck, hand)
                         | otherwise = playBankHelper  smallerDeck biggerHand
  where (smallerDeck, biggerHand) = draw deck hand

------------------- [B5]---------------------------------

--- Generates a list of N random doubles in the range [0...1]
randomList :: StdGen -> Integer -> [Double]
randomList g n | n == 0 = []
                        | otherwise = n1: otherNumber
                          where (n1, g') = random  g
                                otherNumber = randomList g' (n-1)

-- First generate a list of random doubles in range 0..1, then for each pick the card of that position in the current deck and add it to result
shuffleDeck :: StdGen->Hand -> Hand
shuffleDeck g deck = resultingDeck
   where (_, resultingDeck) =  foldr (\random (d, hand) -> drawNthDouble d hand random)
                               (deck, Empty) randomNumbers
         randomNumbers = randomList g deckSize
         deckSize = size deck


------------------[B5-tests]----------------------

---- DONT RUN THIS, Quickcheck hangs on this, dont understand why :(
--prop_randomListSize :: StdGen->Integer->Bool
--prop_randomListSize g n = length (randomList g n 10) == fromInteger n

contains:: Hand -> Card -> Bool
contains Empty _ = False
contains (Add c rest) card = (c == card) || contains rest card


prop_shuffle_contains_all :: Hand->StdGen-> Bool
prop_shuffle_contains_all deck g = and [contains shuffled card| card<- toList deck]
    where shuffled = shuffleDeck g deck

          toList Empty = []
          toList (Add card rest) = card:toList rest


prop_shuffle_sameCards :: StdGen -> Card -> Hand -> Bool
prop_shuffle_sameCards g c h =
    c `belongsTo` h == c `belongsTo` shuffleDeck g h


belongsTo :: Card -> Hand -> Bool
c `belongsTo` Empty = False
c `belongsTo` (Add c' h) = c == c' || c `belongsTo` h


prop_size_shuffle :: StdGen -> Hand -> Bool
prop_size_shuffle g h = size (shuffleDeck g h) == size h


----------------------------- [Main] -------------------------------

implementation = Interface
  { iFullDeck = fullDeck
  , iValue    = value
  , iDisplay  = display
  , iGameOver = gameOver
  , iWinner   = winner 
  , iDraw     = draw
  , iPlayBank = playBank
  , iShuffle  = shuffleDeck
  }

main :: IO ()
main = runGame implementation
