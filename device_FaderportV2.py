# name=Presonus Faderport V2
# url=
# supportedDevices=

import faderport_v2

# Controller Definition
# Faderport v2 - STUDIO ONE -> Initial setup with Solo button.
# Warning: MCU(Live) does not support Shift button, please, use STUDIO ONE.

# CONTROLLER_MIDI_PROTOCOL
class PresonusFaderportV2_STUDIO_ONE:
	def __init__(self):
		pass

	NAME = 'Presonus Faderport V2'

	SYSEX_HEADER = [0xF0, 0x00, 0x01, 0x06, 0x02]
	# Buttons [0x90, ID(hex), 0x00 (released/led off) | 0x7F (pressed/led on) | 0x01 (flashing led)
	FADER_TOUCH = 0x68

	SOLO = 0x08  # LED
	MUTE = 0x10  # LED
	ARM = 0x00  # LED
	SHIFT = 0x46  # LED

	BYPASS = 0x03  # LED
	TOUCH = 0x4d  # RGB
	READ = 0x4a  # RGB
	WRITE = 0x4b  # RGB

	PREV = 0x2e  # LED
	PUSH_ENCODER = 0x20
	NEXT = 0x2f  # LED

	LINK = 0x05  # RGB
	PAN = 0x2a
	CHANNEL = 0x36
	SCROLL = 0x38  # RGB

	MASTER = 0x3a  # LED
	CLICK = 0x3b  # LED
	SECTION = 0x3c  # LED
	MARKER = 0x3d  # LED

	LOOP = 0x56  # LED
	REWIND = 0x5b  # LED
	FAST_FORWARD = 0x5c  # LED

	STOP = 0x5d  # LED
	PLAY = 0x5e  # LED
	RECORD = 0x5f  # LED

	FOOTSWITCH = 0x66

	# Faders
	FADER = 0xe0
	FADER_MIDI_CHANNEL = 0

	# Encoders
	ENCODER = 0x10
	ENCODER_MIN_STEP_RIGHT = 0x1
	ENCODER_MIN_STEP_LEFT = 0x41

	# LED
	LED_ON = 0x7F
	LED_OFF = 0x00
	LED_BLINK = 0x01
	# LED RGB get
	RED = 0x91
	GREEN = 0x92
	BLUE = 0x93

	# LED RGB set
	MIDI_CHANNEL_TO_SET_RED_COLOR = 1
	MIDI_CHANNEL_TO_SET_GREEN_COLOR = 2
	MIDI_CHANNEL_TO_SET_BLUE_COLOR = 3
	# MIDI channel 1-3 is used to set the RGB values of a LED
	# color with 7-bit resolution per color

class PresonusFaderportV2(PresonusFaderportV2_STUDIO_ONE):
	pass

mcu = faderport_v2.Controller(PresonusFaderportV2())

def OnInit():
	mcu.OnInit()

def OnDeInit():
	mcu.OnDeInit()

def OnDirtyMixerTrack(SetTrackNum):
	pass

def OnRefresh(Flags):
	mcu.OnRefresh(Flags)

def OnMidiIn(event):
	pass

def OnMidiMsg(event):
	mcu.OnMidiMsg(event)

def OnNoteOn(event):
	pass

def OnNoteOff(event):
	pass

def OnControlChange(event):
	mcu.OnControlChange(event)

def OnPitchBend(event):
	mcu.OnPithBend(event)

def OnMidiOutMsg(event):
	pass

def OnSendTempMsg(Msg, Duration = 1000):
	pass

def OnUpdateBeatIndicator(Value):
	pass

def OnUpdateMeters():
	pass

def OnIdle():
	pass

def OnWaitingForInput():
	pass