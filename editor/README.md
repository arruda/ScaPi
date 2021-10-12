# ScaPi Editor
Runs the ScaPi board Editor. **All the steps to run the editor should be done from inside the `editor` directiory.**

## Requirements:
* Python >= 3.6
* pip


## Initial Setup
Then install the necessary Python packages for running the board editor. Go into the `editor` directory, and then run `pip install -r requirements.txt`.

## Running the Editor
To run the editor execute: `run.py`.

## Create New Board
The user will be asked the Height and Width of the new board, and then presented with the Board Edit window.

## Board Edit
The user must click on which tile it wants to have active in the Menu (ex: `.`). Then, the active tile type will be marked as red, and it will allow the user to replace any tile in the board by clicking on the tile it wishes to replace with the active tile type.

Once the user is satisfied with the board, they should click on the `Save` button.
In the next window they will be asked the file name of the new board they wish to save (the board file should follow the naming convention of specified in [New Board Designs](/CONTRIBUTING.md#new-boards-designs))

