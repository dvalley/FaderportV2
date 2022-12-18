# Presonus Faderport V2
Script supporting the Presonus Faderport V2 Control Surface 
More info see here: https://forum.image-line.com/viewtopic.php?p=1676355#p1676355

## Release Notes
### 1.1.0 
Added bypass, reverse polarity and swap channel in mixer tracks. 
Removed open next plugin on bypass button, already included in FL Studio as keyboard shortcut.


## Setup

Create a **faderport** folder in 
* MacOS: $HOME/Image-Line/FL Studio/Settings/Hardware/
* Windows: C:\Program Files\Image-Line\FL Studio 20\System\Hardware

Copy following python files into this folder.

[device_FaderportV2](device_FaderportV2.py): Controller hex midi protocol.

[Faderport_v2](faderpor_v2.py): Controller logic.

[Components](components.py): Object-Oriented Programming components like Buttons, Leds, Encoders\Knobs, Sliders/Faders.

[Wrapper](wrapper.py): Fl Studio wrapper library with simplified and easy to understand functions/methods.

Port must be set to 0 on input and output. To open MIDI settings: F10.
I do not know why but Omni channel must be also set to 1, otherwise unasigned buttons triggers channel element playback.

## Features

### Buttons

| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Solo | Toggle Solo selected or locked track | Ready ||
| Solo + SHIFT | TBD | TODO | Solo Clear is not needed, since it is the default behaviour when toggling the solo button |
| Mute | Mute | OK | |
| Mute + SHIFT | Mute Clear | OK | |
| Arm | Arm selected mixer track | OK | |
| Arm + SHIFT | TBD | TODO | Arm All is not a common use case to be implemented |
| SHIFT  | Enable shift | OK | |
| Bypass  | Bypass | OK | Toggle bypass effect on selected mixer tracks |
| Bypass + SHIFT  | Bypass all | OK | Toggle bypass effect on all mixer tracks |
| Touch  | Reverse polarity | OK | Toggle reverse polarity effect on selected mixer tracks |
| Touch + SHIFT  | Swap left right channel | OK | Toggle Swap left right channel on all mixer tracks |
| Write  | TBD | TODO | |
| Write + SHIFT   | TBD | TODO | |
| Read  | TBD | TODO | Change to blue color if there are changes and it is not saved |
| Read + SHIFT   | TBD | TODO | |
| Prev  | Select previous mixer track | OK | |
| Prev + SHIFT  | Undo | OK | |
| Next  | Select next mixer track | OK | |
| Next + SHIFT  | Redo | OK | |
| Link | TBD | TODO | |
| Link + SHIFT| TBD | TODO | |
| Pan | See encoder | TODO | |
| Pan + SHIFT| TBD | TODO | |
| Channel | Unlock selected mixer track | OK | |
| Channel + SHIFT| Lock selected mixer track | OK | Led is blinking |
| Scroll | See encoder | TODO | |
| Scroll + SHIFT| TBD | TODO | |
| Master | TBD | TODO | |
| Master + SHIFT| TBD | TODO | |
| Click | Enable metronome | TODO | |
| Click + SHIFT| TBD | TODO | |
| Section | TBD | TODO | |
| Section + SHIFT| TBD | TODO | |
| Marker | Marker navigation. See encoder | OK | |
| Marker + SHIFT| Marker selection. See encoder | OK | |
| Loop | Toggle between pattern and sond mode | OK | |
| Rewind | Rewind | OK | |
| Fast Forward | Fast Forward| OK |
| Stop | Stop | OK | |
| Play | Play and pause | OK | |
| Record | Enable record | OK | |


### Encoder
#### Encoder default
| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Rotate Left | Select previous mixer track | OK | |
| Push | Reset fader level | OK | |
| Push + SHIFT | Set fader level to minimum | OK | | 
| Rotate Right | Select next mixer track | OK | |

#### Encoder + Pan button
| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Rotate Left | Pan left selected mixer track | OK | |
| Push | Reset pan | OK | |
| Push + SHIFT | TBD | TODO | | 
| Rotate Right | Pan right selected mixer track | OK | |

#### Encoder + Marker button
| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Rotate Left | Pan left selected mixer track | OK | |
| Push | Reset pan | OK | |
| Push + SHIFT | TBD | TODO | | 
| Rotate Right | Pan right selected mixer track | OK | |

#### Encoder + Scroll button (Small increments)
| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Rotate Left | Scroll playlist cursor to left | OK | |
| Push | TBD | TODO | |
| Push + SHIFT | TBD | TODO | |
| SHIFT | Big scroll increments enabled | OK | | 
| Rotate Right | Scroll playlist cursor to right | OK | |

### Fader
| Trigger Elements | Feature | Status | Comments |
| ---------------- | ------- | ------ | -------- |
| Fader | Send level to selected or locker mixer | OK | |
| Touch | Send level to selected or locker mixer | DISABLED | |

TBD: TO BE DEFINED

TODO: TO BE DONE


## Customize and Contribute
Customize files if needed and then update this README file.
Create a Pull Request to master branch.

#### Best code practices to facilitate contribution
* Avoid more than 500 lines of code in the same file. Keep it as small as possible.
* Constants:
    * Avoid magic hardcoded numbers. Use constants with meaningful names inside the functions.
* Naming:
    * Use full words instead of abbreviations.
    * Use a meaningful and easy to understand name for functions, variables, classes, etc.

[Python style from Google](https://google.github.io/styleguide/pyguide.html)


