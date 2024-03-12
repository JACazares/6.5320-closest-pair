# 6.5320 Closest Pair of Points

This is the code for the optional part of the first pset of 6.5320.

## Demo

https://github.com/JACazares/6.5230-closest-pair/assets/17916448/b8d9a602-c99b-49d7-87ba-920c1db92869

## Instalation Instruction

1. Install pygame using
```
pip install pygame
```
2. Clone the repository in the desired directory
```
git clone https://github.com/JACazares/6.5230-closest-pair.git .
```
3. Run the closest_point.py file
```
python closest_point.py
```

## Overview
There are three components to this.

_algorithm.py_: Contains the code for the closest pair algorithm, runs in $O(N \lg^2 N)$, yields at every step where we need to update the image
_draw_state.py_: Contains the ```draw_state``` function, which is used to draw the points and subsequent necessary lines, halfplanes, stripes, depending on which part of the algorithm we are currently executing
_closest_point.py_: Contains the code to draw the main menu window, alongside button functionality and graphical point input.
