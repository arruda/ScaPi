# ScaPi
ScaPi is a server/client application that helps on teaching concepts and issues multi-threading with the use the Gamification teaching strategy. It is meant to be run using Raspberry Pis in a connected network (hence the name).

Each student(user) takes part in a team, and each team has a single Pawn that must exit a maze before the time runs out. Each user in a team will have a single action that only they can perform in the team pawn, and together they must coordinate their actions in order to scape from a maze with their shared team's pawn.

This mechanics mirrors some of the problems that the CPU has when handling the multiple threads of a process. In this context, each team acts a different process in the CPU, and each user in a team acts as a unique thread in that process.

This leads to a few issues common in this scenario, such as multiple threads competing for the same resource, as well as managing the ordering of operations.

To cope with this issues the teams must devise their own task scheduling algorithm that will allow them to better manage the team and acomplish their goal.

In addition, on an advanced version of the game, the teams will also have to compete scoring in a leaderboard. In this scenarios, each team may try to leave through a "magic door" instead of the regular exit of the mase. But in order to do so, they'll need to retried two Keys that are scathered through the mase, otherwise they won't be able to leave. This scenario, also gives room for the students to see in action how dead-locks occur between threads (i.e.: each team has a key, and neither can leave the maze until the other drops a key).

# ScaPi Server
The ScaPi Server is ran by the Lab tutor (admin) presents the board and the game logicstics, and more information can be seen in it's [README](/server/README.md) file.

# ScaPi Client
The ScaPi Client is executed by the students (the users) and it presents the means for interacting with the game. More information can be seen in it's [README](/client/README.md) file.

# ScaPi Editor
The ScaPi Editor is an app that provides simple GUI for creating new boards (used on the ScaPi Server). More information can be seen in it's [README](/editor/README.md) file.

# License
This project is distributed under the MIT license. See `LICENSE` file for more details.