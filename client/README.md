# ScaPi Client
Runs the ScaPi client. **All the steps to run the client should be done from inside the `client` directiory.**

## Requirements:
* Python >= 3.6
* pip



## Initial Setup
Then install the necessary Python packages for running the client. Go into the `client` directory, and then run `pip install -r requirements.txt`.


Next, copy the `client/example.env` file into `client/.env` file, and in this new `.env` file put the necessary configurations:
* **REDIS_ADDRESS**: This should set to the IP address of the ScaPi Server (informed by the Admin).
* **TEAM_NAME**: Put your team name in here (this is camel-sensitive, and should be the exact same name for all students in a given team).
* **USER**: This is your identification inside your team, a simple and clear username should be used (this will only be necessary for the team to manage itself).

## Running a Game
For this, you will need to open a terminals and navigate to the game client directory. Then, execute `./run.py` in order to run the client.

**If an exception occurs, it probably means that your client couldn't connect to the ScaPi Redis Server.**


### User Registration
Once you execute the client, it will required you to check the team and user information that it will be sending to the server.
If their are incorrect, the student should input `n` and the application will exit, allowing the student to fix their credentials in the `.env` file before restarting.

If the informations are correct, just press enter, and it will send the registration data to the ScaPi server. The student should then check in the Server screen if the student username is listed under the proper team.

Once all teams are ready, and the Admin starts the game, all students client screen will change to the game input mode.

### Action Inputs
Once the game starts each team user will receive a random action that only they can perform in their team. These actions will be used to controll the team's pawn in the board (which will be seen in the ScaPi server screen).

To send an action, one must input their corresponding number (as shown in their screen), and press enter.
If a invalid action is sent, an error will be printed and the action will be ignored.

Once an action is sent, the client will again present another action input. This will continue as long as the game has ended (or until the team leaves the maze).