# Yet Another Train Simulator - Phase 1

## Design

In this phase, `GameGrid`, `Train`, `Cell` classes are implemented. Additionally an abstract factory class for creating `Cell` objects is also implemented. Finally, some basic helper classes for enumerations are implemented to enforce safety. An overview of the classes are given below. You can read the docstrings of classes and their methods for more detailed explanation.

* `GameGrid` encapsulates trains and cells. In this phase it is the top level class for managing the "game".

* `Train` is the moving actors in the game. They can move through cells as long as they are active. If they try to get out of the map or reach the end of a track, they stop. In this phase, only the first train car is displayed as the simulation and therefore the car placement algorithms are not implemented. However, basic `pygame` tests are included to demonstrate the classes.

* `Cell` implements the atomic parts of the grid. For each type of cell there exists a subtype of `Cell` class. The cells are intended to be created with a factory method. A simple factory class that implement the abstract factory class is provided for demonstration purposes. If the different aspects of a cell's behavior can be completely isolated, Bridge pattern can be used to evoid subclass proliferation. If that happens to be case, cell's will be composed agents responsible for different aspects of the behavior. For example a ConcreteCell object can have a ConcreteRouter object handling `self.switch_state()`, `self.next_cell()`; a ConcreteTimer object handling `get_duration()`, and `get_stop()` etc.

Also, `Direction` class that extends `Enum` is used instead of `int` for representing the four directions is used to better leverage the code analysis tools, and to avoid error prone operations with `int`.

## TODOs, Nice to Haves, and Future Considerations

- Bridge pattern can be used to decouple the cell related interface and its implementation. In fact, `Cell` class will aggregate multiple interfaces.

- A *visitor* for displaying the game objects can be used. This way different users can choose to use their viewer object of choice to customize the visuals of the game for themselves. For example a user can have a B/W theme on their browser, while another can use a low contrast theme, or a TUI theme.

- Unit and integration tests to check the correctness of the code once the API is more stable. It can be integrated to the precommit hooks/

- Automatic API reference generation from docstrings. Doctests can be utilized to keep the docstrings up-to-date.
