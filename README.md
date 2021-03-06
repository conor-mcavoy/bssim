# BSSim
## Overview
This program allows you to play a game of battleship versus a computer on a standard 10x10 grid.
The computer determines its best move using a Monte Carlo method.

## Getting started
Clone this repository locally. You'll need Python installed, as well as a library called `pygame`, which can be installed with `pip install pygame` if you have `pip`. Check for `pip` with `pip --version`.
Run the game with `python bssim.py filename` where `filename` is the path to a text file containing your ship data.

You can specify the location of your ships in this text file with the following format: `ship_size column_letter row_number direction`.
* `ship_size`: The length of the ship.
* `column_letter`: The column letter of the topmost, leftmost square the ship occupies. Column letters go from A to J.
* `row_number`: The row number of the topmost, leftmost square the ship occupies. Row numbers go from 1 to 10.
* `direction`: Either 'right' or 'down'.

For example, `5 A 1 down` would put a ship of length 5 in square A1 going downwards to square A5.
One ship can be specified per line of this text file.
Currently, only five ships can be specified, and they must be of lengths 5, 4, 3, 3, and 2 (in any order).
Any other configuration won't work.

Once the game is running, the layout should be intuitive. Good luck, it's not easy to beat the computer!

## Monte Carlo method
The algorithm used is relatively straightforward. The computer records all of its past hits and misses. Each turn, it uses that information to generate a list of all possible locations for each enemy ship. Then it makes random selections among these possibilities and records the valid configurations, compiling the data into a frequency chart. After 100 iterations, the square most often occupied in these simulations is chosen as the next shot.

Because of this method, the computer will likely make its first shots towards the center of the grid, slowly winding its way towards the edges without placing shots too close together. Once it registers a hit on a square, it will probably shoot around that square until it sinks the ship associated with it, just like a real player. Overall, this method is so successful because it mirrors just what an intelligent player would do, which is to think about where enemy ships are most likely to be.

## Future
There will soon be a way to place your ships in-game, without relying on a complicated format in a text file. I also want to add the option to view a heat-map diagram of the square frequency chart mentioned above, which would allow the player to see their own board as the computer imagines it to be laid out.

This game is currently written in Python using the `pygame` library, but I'd like to allow anyone to use it without having to install Python or `pygame`. The best way to do that is to wrap everything into one executable, but `pygame` is too unstable for this to work. Because of this, I will probably be porting this whole project to a different language.