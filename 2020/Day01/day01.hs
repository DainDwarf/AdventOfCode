import Data.List
import System.IO

-- partOne :: [Int] -> Maybe Int
partOne [] = Nothing
partOne (x:xs) =
    let found = find (== (2020-x)) xs in
    case found of
        Nothing -> partOne xs
        Just y  -> Just (x*y)

parseInput = map read . lines

main = do
    withFile "input" ReadMode (\fh -> do
        content <- hGetContents fh
        putStrLn $ show $ partOne $ parseInput content)
