import Control.Arrow
import qualified Data.Map as Map
import Debug.Trace

data Rule
    = Term Char
    | RulePair Rule Rule
    | RuleNums [Int]
    deriving (Show)

parseRule :: String -> (Int, Rule)
parseRule line =
    case words line of
        num : ruleText -> (read $ filter (/= ':') num :: Int, buildRule [] ruleText)
    where
        buildRule acc [] = RuleNums (reverse acc)
        buildRule acc [['"', c, '"']] = Term c
        buildRule acc ("|" : rest) = RulePair (RuleNums (reverse acc)) (buildRule [] rest)
        buildRule acc (n : rest) = buildRule ((read n :: Int) : acc) rest

buildRules :: [String] -> Map.Map Int Rule
buildRules ruleList = Map.fromList $ map parseRule ruleList

match :: Map.Map Int Rule -> Rule -> String -> (String -> Bool) -> Bool
match _ (Term c) (curr : rest) matchRest = (curr == c) && matchRest rest
match rules (Term c) [] _ = False
match rules (RuleNums (h : t)) str matchRest =
    match rules (rules Map.! h) str (flip (match rules (RuleNums t)) matchRest)
match _ (RuleNums []) str matchRest = matchRest str
match rules (RulePair r1 r2) str matchRest = match rules r1 str matchRest || match rules r2 str matchRest


matchZero :: Map.Map Int Rule -> String -> Bool
matchZero rules s = match rules (RuleNums [0]) s null


new8 :: Rule
new8 = RulePair (RuleNums [42]) (RuleNums [42, 8])

new11 :: Rule
new11 = RulePair (RuleNums [42, 31]) (RuleNums [42, 11, 31])

part1 :: String -> Int
part1 s =
    let
        (ruleLines, messages) = second tail $ span (/= "") $ lines s
        rules = buildRules ruleLines
    in
        length $ filter (matchZero rules) messages

part2 :: String -> Int
part2 s =
    let
        (ruleLines, messages) = second tail $ span (/= "") $ lines s
        rules = Map.insert 8 new8 $ Map.insert 11 new11 $ buildRules ruleLines
    in
        length $ filter (matchZero rules) messages

main = do
        s <- readFile "input.txt"
        print $ part1 s
        print $ part2 s