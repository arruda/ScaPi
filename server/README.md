# ScaPi Server
Runs the Redis server and controlls the game logic. **All the steps to run the server should be done from inside the `server` directiory.**

## Requirements:
* Python >= 3.6
* pip
* Docker
* Docker-compose


## Initial Setup

Install [Docker and Docker-compose](https://docs.docker.com/compose/install/). This will be necessary for running the Redis Server in your machine.



Then install the necessary Python packages for running the server. Go into the `server` directory, and then run `pip install -r requirements.txt`.


Next, copy the `server/example.env` file into `server/.env` file, and in this new `.env` file put the necessary configurations:
* **TEAM_NAMES**: This should be a list of names separated by `/` with each team name
* **STUDENT_CLASS**: This is some identifier for the class, eg: `A` , `B`, `Wednesdey`, etc.. Just to keep the leaderboard records of each class separated.
* **BOARD_ID**: What is the board that will be used in the run (see available boards in `server/boards`)
* **ADMIN_PASS**: Password that will be used by the admin script. This should be changed after each lab, just in case.
* **GAMEOVER_TIME**: How long will the game last (in seconds).


### Testing Setup

First,  execute `docker-compose up -d` to start the Redis Server.

Then in one terminal run the ScaPi server with `./server.py`.

*If an error message appears, then it's most likelly that the Redis Server is not running.*


Next, in another terminal run the ScaPi admin script: `./admin_msg.py`. Press enter to confirm that the game is ready to start, and check in the terminal running the server if the game has started.

*if the game hasn't started, re-check the REDIS_PORT, REDIS_ADDRESS and ADMIN_PASS env vars.*

If the game has started, then you can close both terminals, and the setup is correct.


## Running a Game
For this, you will need to open two terminals and navigate to the game server directory in each.
One server will run the Redis Server and the ScaPi server, another will run the admin script. Both terminal screens should be visible so that the students can see both the game (in the ScaPi server terminal) and how long until game over (in the admin terminal).

### Set Proper Class, Teams, Board and Game Duration
In the `.env` file, change the variables `TEAM_NAMES`, `STUDENT_CLASS`, `BOARD_ID` and `GAMEOVER_TIME` to meet the appropriate setup that you want.

### Start Redis Server (Docker-compose)
Run `docker-compose up -d` to start the Redis Server in the background.

### Start ScaPi Server
Run `./server.py` to start the server.
This will present a screen with each team number (randomised on each game), and a list of registered students (users) in each team.
Once a student registers, their name will automatically appear underneath their team name. The game will start once the admin script sends the confirmation to the server (see bellow).

### Start Admin script
In second terminal, run `./admin_msg.py` and wait untill all student teams are ready.
Once all teams are ready, press enter in the to send the start the game action to the server.
The admin script will now start counting down the seconds until game-over (based on the `GAMEOVER_TIME`).
Once the counter hits `0`, the admin_script will send the game-over action to the server, and it will exit.

## During the game
The ScaPi server will present the current Board and team's positions (each team is represented by their team number).

The last sucessfull action of each team and who performed it will be listed under under `Last Team Action`.

Underneath `Team Scores:` it will be presented the list of teams (with their team number in parenthesis), in addition to that team's information, such as: If (and when) the team has left the maze; the amount of Keys the team is holding; and their score.

## On game Over
Once the game reaches the time limit, all teams (that have not yet left the maze) will receive the game over message, and scores from the game will be saved in the `results` directory, in a CSV file with the name based on the `STUDENT_CLASS` variable. Eg: If `STUDENT_CLASS` is set to `Wednessday`, the CSV file with the game results for this class will be saved in `results\class_Wednessday.csv`.

A confirmation is required in order to save the results, in which it is possible to override the CSV file path to a new one, or just press enter to use the current configuration (based on the `STUDENT_CLASS`).

## Leaderboard
Each class score will be save in it's corresponding CSV file inside the `results` directory. In each row it will be presented the **Date**and **scores for each team** (with a colum for each team name).
Newer games will have their scores added to the end of the file.