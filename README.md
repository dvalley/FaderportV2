# Presonus Faderport V2
Script supporting the Presonus Faderport V2 Control Surface 
More info see here: https://forum.image-line.com/viewtopic.php?p=1676355#p1676355

## Setup

Create a **faderport** folder in 
* MacOS: $HOME/Image-Line/FL Studio/Settings/Hardware/
* Windows: TODO

Copy following python files into this folder.

[device_FaderportV2](device_FaderportV2.py): Controller hex midi protocol.

[Faderport_v2](faderpor_v2.py): Controller logic.

[Components](components.py): Object-Oriented Programming components like Buttons, Leds, Encoders\Knobs, Sliders/Faders.

[Wrapper](wrapper.py): Fl Studio wrapper library with simplified and easy to understand functions/methods.

Port must be set to 0 on input and output. To open MIDI settings: F10.
I do not know why but Omni channel must be also set to 1, otherwise unasigned buttons triggers channel element playback.

## Customize
Customize files if needed.

#### Best code practices to facilitate contribution
* Avoid more than 500 lines of code in the same file. Keep it as small as possible.
* Constants:
    * Avoid magic hardcoded numbers. Use constants with meaningful names inside the functions.
* Naming:
    * Use full words instead of abbreviations.
    * Use a meaningful and easy to understand name for functions, variables, classes, etc.

[Python style from Google](https://google.github.io/styleguide/pyguide.html)



