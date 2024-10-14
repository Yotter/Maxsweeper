# Maxsweeper / No-Guess Minesweeper
A work-in-progress implementation of no-guess Minesweeper!

## History
I started this project back in 2017 when I was learning how to program. I regretfully did not know about git back then and so the start of this repository is when I decided to migrate all my small projects hitherto on loose files onto Github.

I decided at a certain point that having to guess was no fun, so I added a feature where you could click middle mouse button on a tile to tell what mouse button you should press on it (left click for reveal, right click for flag), but that was kind of lame. I eventually decided to try to figure out how to generate boards that don't require guesses.

## No-Guess

The idea with No-Guess Minesweeper is that the board you start out with is guaranteed to be solvable using logic alone, no guesses necessary.

My goal with this was to create boards that were identical in their feel and potential difficulty as a regular randomized board, just without the unsolvable ones.

To do this, I just needed to figure out how to solve a board, then I can generate Minesweeper boards until I get one that my solver can solve, simple! Simple?

## Optimization

The solver generates all possible permutations ("configurations" in code) of bomb / not bomb on the exposed tiles, and then sees which tiles are always a bomb / always not a bomb and flags / reveals accordingly. To generate the configurations, I used backtracking.

But... even with backtracking it is pretty slow. The problem is that every 50/50 multiplies the number of possible configurations by 2 and so things get really exponential really quick with big boards.

The first major optimization was to first try to find the 'easy' tiles; number tiles whose number matches the number of unrevealed tiles around them, or number tiles who already have their number of flags around them. Running this before trying all the different configurations speeds up things A LOT because often just revealing a single tile can kill 1 or even 2 50/50s.

More needs to be done. I'm thinking of a different approach to the configuration generation... More to come soon

## How to run this code

1. Make sure you have Python3 installed and the pygame library installed:

```bash
pip install pygame
```

2. Run the code using python:
```
python Minesweeper.py
```
