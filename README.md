# OBC
Code base for the on-board computer.

Here are all of the subsystems and commands we will be creating: https://docs.google.com/document/d/1V66NCPwv5Gj4enLfBrGx5tulw45LnQMCcO8KJAWFxOc/edit

Here details our progress so far: https://docs.google.com/spreadsheets/d/1YyC3SZZ9GD2oVFYDaOVtp1qOHoukRk1L-C-yypTSXCk/edit#gid=0

Here are details for the files:
scheduler = the "overlord" process that looks over all other processes, analogous to a kernel
2 types of processes:
    state processes: a file that fires up commands for hardware parts to do: helps get the satellite in a certain "state"
    data processes: a file that collects data from our hardware parts


subsystems = hardware parts that have both data collecting components and commands
    allows our processes to use them


steps for the scheduler:
    read data from data processes
    based on that data, fire up/kill state processes