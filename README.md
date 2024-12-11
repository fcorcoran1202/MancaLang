# MancaLang 
MancaLang is a DSL designed for simulating and experimenting with custom Mancala games, enabling users to define custom board configurations and rules. It serves as a versatile tool 
for game design, strategy research, and educational purposes, combining intuitive syntax with powerful simulation capabilities. The language is built in and interpreted by Python. Currently, the language is very basic, but eventually I would like to add more features to it.

## Usage/Grammar
When interpreting a file, a set of grammar rules needs to be followed:

### Board
The 'Board' label is used to define the setup of the board: how many pits and seeds there are. If there isn't anything specified, the default amounts are 12 pits and 4 seeds per pit.

    Board
      Pits 12
      Seeds 4

### Rules
The 'Rules' label is where most of the program takes place. The label is used to define special rules that the programmer specifies. These rules currently include Opposite Capture, Extra Turns, Multipliers, Reverse Order, and Random Seeds.

    Rules
      Randomize
      Multiply 2 by 2
      Multiply 5 by 2
      Multiply 3 by 3
      Multiply 4 by 3
      Multiply 8 by 2
      Multiply 11 by 2
      Multiply 9 by 3
      Multiply 10 by 3

### Play
The 'Play' label marks the end of the program, and begins the simulation of the game with all the above rules. In this example, the board has 12 pits and random seeds from 1-4. The middle 8 pits each have a multiplier applied to them, such that when a seed sowed from that pit is put in the store, it is scored as more than 1 point. The multiplier increases the closer to the middle the pit is.

    Board
      Pits 12
      Seeds 4
    Rules
      Randomize
      Multiply 2 by 2
      Multiply 5 by 2
      Multiply 3 by 3
      Multiply 4 by 3
      Multiply 8 by 2
      Multiply 11 by 2
      Multiply 9 by 3
      Multiply 10 by 3
    Play

