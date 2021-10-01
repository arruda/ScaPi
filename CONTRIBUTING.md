# Contributing Guidelines
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at [https://github.com/arruda/ScaPi/issues](https://github.com/arruda/ScaPi/issues).

If you are reporting a bug, please include:

* Your operating system name and python version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### New Boards Designs
New boards designs should be added to the `server/boards` directory, with a unique name as in `board_{index}` (eg: board_10, board_20). The first digit of the index is to help indicate the dificulty of the board, and  should be either `1` or `2`. Use `1` if the board don't have any magic doors or keys; use `2` if it has magic doors and keys. The following digits should be set to the following digit based on the available boards. Eg: if you are creating a board with no magic doors and no keys, and the is already a `board_11`, `board_12` and `board_13` in the boards directory, then you should name your board as `board_14`.

New board designs should be as balanced as possible for any of the five teams, and they should not be too complex, in order to keep a game round fast (around 5 minutes).
Each board design is a simple text file, with the following representation of characters:
* `|` represents a wall.
* `.` represents a movable path.
* `!` represents a player starting position.
* `@` represents an exit from the maze.
* `#` represents a magical door exit.
* `K` represents a Key for the magical door.

At least five `!` should be present, at least one `@` should be present, and no `.` should be set in the edges of the maze (the maze needs to be encircled by walls).

If using a magical door (`#`) you should at least add two keys (`K`), since two keys is the required count for opening a magical door. Avoid adding too many keys, otherwise they may loose their relative value to the players (they are supposed to be scarce resources that the players must compete to get).

Finally, all boards design files should have an empty line at the end of the file.

## Setting Up the Code for Local Development

Ready to contribute? Here's how to set up `ScaPi` for local development.

1. Fork the `ScaPi` repo on GitHub.
2. Clone your fork locally:
```
$ git clone git@github.com:your_name_here/ScaPi.git
```
3. Install your local copy into a virtualenv using pip. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:
```
$ mkvirtualenv ScaPi
$ cd ScaPi/
$ pip install -r requirements.txt
```
4. If you need to use the ScaPi Server, you will also need to install Docker and Docker Compose in order to run the required Redis Server.

5. Create a branch for local development:
```
$ git checkout -b name-of-your-bugfix-or-feature
```
   Now you can make your changes locally.


6. Commit your changes and push your branch to GitHub:
```
$ git add .
$ git commit -m "Your detailed description of your changes."
$ git push origin name-of-your-bugfix-or-feature
```
7. Submit a pull request through the GitHub website.

## Pull Request Guidelines


Before you submit a pull request, check that it meets these guidelines:

1. The pull request should try to adhere to PEP8 guidelines.
2. If the pull request adds functionality, the docs should be updated, by adding the
   feature to the corresponding README.md.