# customScriptChecking
Custom python scripts that opens other python for checking and (potentially) grading

## Usage
It's pretty basic, follow this steps:
- Open the check.py on your favorite text editor
- Change inn and out variables with whatever you expect from the python program
  - inn:
    - Should be a list of multi-line string (""") which will be input for the python program. Start on the same line as the string starts, and every \n will be an enter. You should end the string on the same line as you close the """
  - out:
    - Should be a list of strings composed of numbers you expect from the program
- Inn and Out are both lists because you can test multiple parameters for the program, check.py will use inn and out based on index
  - This means, the first multiline string on inn, will be matched with the output of the first list of number strings on out.
- After this, run check.py on the root of the folder and follow the instructions showed on the console.

## Considerations
- out only supports numbers (strings of numbers), this is intentionally built like this because it's easier for python to find numbers on text than strings
  - This is because the text may not be what you expect, but the output from the program might still be okay.
- this script looks for .py scripts, and can search inside folders, but just one folder deep.
- Above considerations are (obviously) adjustable, if you update the script and offer the changes on a user-friendly way, please submit a PR.