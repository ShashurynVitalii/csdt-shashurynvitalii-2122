# csdt-shashurynvitalii-2122
## General info about project

- Group - KI-48
- Student - Shashuryn Vitalii
- Subject - CSDT
- Game - Sea Battle
- HW i-face - I2C
- Data driven format - XML

## Description

This project contains a code for so called Sea Battle game. It is designed as single player game.\
Game is built mainly using **pygame** [package](https://www.pygame.org) for Python. As a player you\
can place your ships and play againts computer oponent. Game is not ideally produced and has some \
flaws (for example, in classic game you can sunk ship only if you hit all it's cells on the board, \
but in this particular realization hitting only one single cell of the ship will cause it to sunk)\

###### Controls

- To place ships you only need to use your mouse (left click). Order of the ships to place match the
one shown on the game preparation screen (from top to bottom). After placing your ships just press any 
key (as it said on the screen) to start the game.
- To hit cell on the board also use your mouse (player board is placed on the right). Be aware: after
your turn click left mouse button one more time to let computer oponent perform it's move
- To quit the game just use close button on game window.

## Instalation and run

In order to run the game you firstly will need to install [Python](https://www.python.org/downloads/)\
Project was build on Python 3.9, so you can just use the same. After that go to SeaBattleGame directory.\
There you will see two important files:
```
Pipfile
Pipfile.lock
```
Those two files contain all info about needed packages and dependencies. In order to use them you need to \
use the following commands:
```
pipenv shell
pipenv install
```
Those two commands will create a virtual environment to work with (very common practice in Python projects,\
also you will need to run it every time you restart your terminal), and then install all packages and\
dependencies listed in Pipfile and Pipfile.lock\

After all that use the following command in order to run the game:
```
python controller.py
```
###### Version
- 1.0