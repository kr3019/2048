# 2048 AGENT AI
This is an AI agent that plays the game of 2048. The agent uses the expectiminimax algorithm with alpha-beta pruning to choose its moves.

## Installation
To use the agent, you'll need to have Python 3 installed on your system. You'll also need to install the numpy and termcolor packages. You can do this using pip:

```
pip install numpy termcolor
```

## Usage
To run the agent, simply execute the GameManager.py script:
```
python3 GameManager.py
```
## Heuristics
The agent uses three different heuristics to evaluate the quality of the game board and make decisions on the moves to make. These heuristics are:

- Monotonicity Heuristic: This heuristic checks whether the values in rows and columns are sorted in either ascending or descending order. If they are, then the heuristic rewards the grid with the difference between the highest and lowest value. If the values are not sorted, the heuristic punishes the grid by subtracting the difference between the highest and lowest values. This heuristic is intended to reward grids that have a consistent trend of increasing or decreasing values and to punish those with irregular patterns.

- Corner Heuristic: This heuristic adds up the product of each tile's value and the square of its position. The idea is to prioritize tiles in the corners of the board as they are harder to merge and can create roadblocks. The higher the sum of the values, the better the board.

- Identical Heuristic: This heuristic assigns a score to the board based on the number of identical tiles. The higher the number of identical tiles, the better the score. This heuristic aims to prioritize grids with many identical tiles as they are easier to merge.

- The intelligent agent evaluates the quality of the board using all three heuristics and combines the scores to determine the overall utility of the grid. The agent then uses the expectiminimax algorithm with alpha-beta pruning to determine the best move to make based on the utility of the grid.
