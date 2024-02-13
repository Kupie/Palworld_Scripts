# Palworld_Scripts
Scripts to manage Palworld dedicated servers

Currently only a "watchdog" script that requires a specific version of python's RCON, since palworld is dumb and doesn't return stuff correctly right now:
https://github.com/conqp/rcon/pull/26

Watchdog script  sends notifications when players join/leave the server, and runs a task with "schtasks" to restart server if we fail to connect 5 times.
