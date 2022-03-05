# 🚂 Yet Another Train Simulator! 🚂

YATSIM is a collaborative train simulator developed as a course project by [@koluacik](https://github.com/koluacik) and [@ucanyiit](https://github.com/ucanyiit). In this web application, users can create multiple rooms, edit the game grid in a room, run the train simulation and share their grid with others. Users' operations are handled by a backend application and sent to other users so users can receive others' changes instantly.

## General Architecture

YATSIM is built utilizing the client-server architecture.

Django is used to create a backend server. Django REST Framework is used to develop a REST API, and Django Channels is used to send notifications about operations to users.

React is used on the front end. Websockets are used to synchronize clients in a room, and Material UI is used as the UI framework.

Users use the developed frontend application to send HTTP requests to the REST API. After handling the request, the server sends a notification about the operation on the `GameGrid` to other users. The frontend application receives the change and applies it to the grid shown to the user.

## Features

- `User`: The user model is the default user model from Django.
- `Room`: Each room has a single `GameGrid`, a single `owner`, and multiple `Users` in its `guests` lists.
    - Adding a user to the room as `guests` list
    - Remove a user from the `guests` list
    - Deleting the room, leaving from the room
    - Cloning a room (Creates a room with the same `GameGrid`)
- `Cell`: A `Cell` has `X`, `Y`, `Room`, `Type`.
    - Different `Cell` types: Straight, Station, Y Junction, X Junction, etc.
    - Some `Cell` types are junctions, and a state is kept to decide which direction a train should move when it enters the junction.
    - Station typed cells keep a train type and length. It indicates which train it will spawn when a simulation starts. 
- `GameGrid`:
    - Rotating direction of a cell (Setting its direction) 
    - Placing a cell on a given location
    - Switching state of a stateful cell (junctions)
    - Add/remove a train to/from the cell. (Only for station cells)
- `Train`: A train has a `Type` and `Length`. It is alive only when a simulation is running.
- `Simulation`: When a simulation is running, all trains move with the set speed.
    - Starting the simulation: Spawns train objects from the stations
    - Stopping the simulation: Deletes all of the train objects
    - Toggling the simulation: Starts/stops the currently running simulation
    - Changing the speed (period) of the simulation

## Development

There are 4 phases while developing the project. Below is the context of the phases.

1. Initial classes and design for the project. 
    - `GameGrid`, `Cell` and `Train` classes are defined and implemented. 
    - Pygame is used to test this phase.
2. Client-server model is used to create a socket connection. 
    - JSON requests and responses are sent over the socket. 
    - We have used PostgreSQL as the persistent database.
    - A `Room` class is defined so that users can share their game grids with others. `Room` object considers the synchronization problems.
3. Initial Django project is created.
    - All the functionalities are moved to the new Django server. 
    - HTTP requests are used instead of sockets at this phase.
    - A simple user interface is developed. Bootstrap is used.
4. Synchronized operations.
    - Django Channels and Websockets are used to send notifications about operations to all users in a room. This way, each user can see all of the changes instantly without refreshing the page.
    - Django REST Framework is used to refactor the Django code.
    - For the frontend, ReactJS is used to have a more responsive user interface. Material UI is used to have better visuals.

**See CONTRIBUTING.md for setting up the development environment.**