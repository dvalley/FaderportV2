# name=dvalley functions
# url=

import device
import general
import mixer
import arrangement
# Do not add device controller logic here, only FLStudio wrapper or util functions
import transport
import ui

import midi
# User libraries
# import pykeys

ENABLE = 1
DISABLE = 0
TOGGLE = -1

# Speed
HALF_SPEED = 0.5
DOUBLE_SPEED = 2
STANDARD_SPEED = 1

OFF_ON = ('off', 'on')

def debug_event(event, name = ''):
    print(f'DEBUG -{name}- Midi event ID: {[decimal_to_hex_without_0x(i) for i in [event.midiId, event.data1, event.data2]]} '
          f'- SysEx {event.sysex} - pmeFlags {event.pmeFlags} - midiChannel {event.midiChan} - port {event.port}'
          )

def get_value_from_tuple(tuple_parameter):
    result = tuple_parameter
    if type(tuple_parameter) == tuple and len(tuple_parameter) == 1:
        if callable(tuple_parameter[0]):
            result = tuple_parameter[0]()  # return the evaluation of the function inside the tuple
        else:
            result = tuple_parameter[0]  # return the tuple
    else:
        result = tuple_parameter  # is not a tuple
    return result

# Note on is 0x90 and data2 = 0x7f, note off is data2 = 0x00
def is_note_on(event):
    return (event.midiId == midi.MIDI_NOTEON) & (event.data2 > 0)
    # return event.data2 > 0
# returns DISABLED if off, ENABLED if on
def enable_or_disable(event):
    if is_note_on(event):
        return ENABLE
    else:
        return DISABLE

def show_hint(message):
    ui.setHintMsg(message)

def show_is_on_or_off(message, boolean_parameter):
    show_hint(message + OFF_ON[boolean_parameter])

# def send_message_to_ui(Msg, Duration=500):
#
#     if len(Msg)>2:
#         if (RouteTempTextToFLDisplay):
#             ui.setHintMsg((Msg+' '*56)[0:56])
#         if (TargetSecondDisplays):
#             self.SendMsg('  '+Msg.ljust(54, ' '), 0, 2)
#         elif RouteTempTextToClassic:
#             if SplitAccrossScribbleStrips:
#                 self.OnSendTempMsg(self.TidyScribbles(Msg),Duration)
#             else:
#                 self.OnSendTempMsg(Msg,Duration)

def dec_to_hex(decimal):
    return hex(decimal)

def decimal_to_hex_without_0x(decimal):
    return dec_to_hex(decimal).replace('0x','')

# multiply used to reuse code from different functions
def send_event_to_globaltransport(event, midi_fpt, multiply = 1):
    transport.globalTransport(midi_fpt, enable_or_disable(event) * multiply, event.pmeFlags)

def set_playback_speed_to_normal():
    transport.setPlaybackSpeed(1)

def play_pause(event):
    send_event_to_globaltransport(event, midi.FPT_Play)

def play_stop():
    set_playback_speed_to_normal()
    if transport.isPlaying():
        transport.stop()
    else:
        transport.start()

def stop(event):
    send_event_to_globaltransport(event, midi.FPT_Stop)

def rewind(event):
    send_event_to_globaltransport(event, midi.FPT_Rewind, 2)

def fast_forward(event):
    send_event_to_globaltransport(event, midi.FPT_FastForward, 2)

def record(event):
    send_event_to_globaltransport(event, midi.FPT_Record)

def song_loop(event):
    send_event_to_globaltransport(event, midi.FPT_Loop)

def get_song_position_in_ms():
    return transport.getSongPos(midi.SONGLENGTH_ABSTICKS)

def scroll_song(steps):
    transport.setSongPos(get_song_position_in_ms() + steps, midi.SONGLENGTH_ABSTICKS)

def scroll_to_left(steps):
    scroll_song(steps * -1)

def scroll_to_right(steps):
    scroll_song(steps * 1)

def mode(event):
    send_event_to_globaltransport(event, midi.FPT_Mode)
    device.directFeedback(event)

def metronome(event):
    send_event_to_globaltransport(event, midi.FPT_Metronome)

def precount(event):
    send_event_to_globaltransport(event, midi.FPT_CountDown)

def next_snapmode(event):
    send_event_to_globaltransport(event, midi.FPT_SnapMode)

def snap(event):
    send_event_to_globaltransport(event, midi.FPT_Snap)

def set_time_display_to_minutes():
    ui.setTimeDispMin()

def flip(event):
    device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16))

def show_browser():
    ui.showWindow(midi.widBrowser)

def show_channel_rack():
    ui.showWindow(midi.widChannelRack)

def show_mixer():
    ui.showWindow(midi.widMixer)
    ui.setFocused(midi.widMixer)

def add_marker(event, is_shift_enabled):
    if is_shift_enabled:
        send_event_to_globaltransport(event, midi.FPT_AddAltMarker)
    else:
        send_event_to_globaltransport(event, midi.FPT_AddMarker)

def get_selected_tracknumber():
    return mixer.trackNumber()

def mute_multiple():
    for track in range(mixer.trackCount()):
        if mixer.isTrackSelected(track):
            mute(track)

def set_tracknumber(track_number):
    mixer.setTrackNumber(track_number)

def number_of_tracks():
    return mixer.trackCount()

def select_next_track(step = 1):
    final_track_number = get_selected_tracknumber() + step
    if final_track_number > max_count_of_tracks():
        final_track_number = final_track_number - max_count_of_tracks() - 1
    mixer.setTrackNumber(final_track_number, midi.curfxScrollToMakeVisible | midi.curfxMinimalLatencyUpdate)
    show_selected_track()

def select_previous_track(step = 1):
    final_track_number = get_selected_tracknumber() - step
    if final_track_number < 0:
        final_track_number = max_count_of_tracks() - final_track_number
    mixer.setTrackNumber(final_track_number, midi.curfxScrollToMakeVisible | midi.curfxMinimalLatencyUpdate)
    show_selected_track()

def max_count_of_tracks():
    FLSTUDIO_RESERVED_TRACKS = 2
    return mixer.trackCount() - FLSTUDIO_RESERVED_TRACKS

def show_selected_track():
    show_hint('Selected track %s' % get_selected_tracknumber())

# Turn Led on, off or blink
def set_led_status_to(event, status):
    modified_event = event
    modified_event.data2 = status
    device.directFeedback(modified_event)

def set_led_on_condition(id, condition):
    device.midiOutMsg((id << 8) + midi.TranzPort_OffOnT[condition], 0)

def set_led_on(id):
    device.midiOutMsg((id << 8) + midi.TranzPort_OffOnT[1], 0)

def set_led_off(id):
    device.midiOutMsg((id << 8) + midi.TranzPort_OffOnT[0], 0)

def send_midi_message_to_device(midiId, channel, data1, data2):
    if device.isAssigned():
        device.midiOutMsg(midiId, channel, data1, data2)

def solo(*track_number_tuple):
    mixer.soloTrack(get_value_from_tuple(track_number_tuple), midi.fxSoloToggle)

def is_solo(track_number = get_selected_tracknumber()):
    return mixer.isTrackSolo(track_number)

# Not needed in FLStudio. Solo button is clearing solo when unselected.
def solo_clear():
    pass

def mute(*track_number_tuple):
    mixer.enableTrack(get_value_from_tuple(track_number_tuple))

def is_muted(track_number = get_selected_tracknumber()):
    return mixer.isTrackMuted(track_number)

def mute_clear():
    for track in range(mixer.trackCount()):
        if not mixer.isTrackEnabled(track):
            mixer.enableTrack(track)

def arm():
    mixer.armTrack(get_selected_tracknumber())

def is_armed(track_number = get_selected_tracknumber()):
    return mixer.isTrackArmed(track_number)

# Not needed in most cases.
def arm_all():
    pass

def open_previous_plugin():
    transport.globalTransport(midi.FPT_MixerWindowJog, -1, 2)

def open_next_plugin():
    transport.globalTransport(midi.FPT_NextMixerWindow, 1, 111)

def close_window():
    ui.escape()

def is_bypassed(track_number = get_selected_tracknumber()):
    return not mixer.isTrackSlotsEnabled(track_number)

def bypass_fx_toggle(*track_number_tuple):
    track_number = get_value_from_tuple(track_number_tuple)
    # This "if" is because of TOGGLE not working so far.
    if mixer.isTrackSlotsEnabled(track_number):
        operation = DISABLE
    else:
        operation = ENABLE
    mixer.enableTrackSlots(get_value_from_tuple(track_number_tuple), operation)

def bypass_fx_all():
    for track in range(mixer.trackCount()):
        bypass_fx_toggle(track)

def bypass_fx_selected():
    for track in range(mixer.trackCount()):
        if mixer.isTrackSelected(track):
            bypass_fx_toggle(track)

def is_reversed_polarity(track_number = get_selected_tracknumber()):
    return mixer.isTrackRevPolarity(track_number)

def reverse_polarity_selected():
    for track in range(mixer.trackCount()):
        if mixer.isTrackSelected(track):
            reverse_polarity_toggle(track)

def reverse_polarity_toggle(*track_number_tuple):
    track_number = get_value_from_tuple(track_number_tuple)
    # This "if" is because of TOGGLE not working so far.
    if mixer.isTrackRevPolarity(track_number):
        operation = DISABLE
    else:
        operation = ENABLE
    mixer.revTrackPolarity(track_number, operation)

def is_swap_left_right_channels(track_number = get_selected_tracknumber()):
    return not mixer.isTrackSwapChannels(track_number)

def swap_left_right_channels_selected():
    for track in range(mixer.trackCount()):
        if mixer.isTrackSelected(track):
            swap_left_right_channels(track)

def swap_left_right_channels(*track_number_tuple):
    track_number = get_value_from_tuple(track_number_tuple)
    # This "if" is because of TOGGLE not working so far.
    if mixer.isTrackSwapChannels(track_number):
        operation = DISABLE
    else:
        operation = ENABLE
    mixer.swapTrackChannels(track_number, operation)

def undo_redo(event):
    if (transport.globalTransport(midi.FPT_Undo, int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global) & (event.data2 > 0):
        show_hint(ui.getHintMsg() + ' (level ' + general.getUndoLevelHint() + ')')

def redo():
    general.undoDown()

def undo():
    general.undoUp()

def set_pan(pan_amount):
    mixer.setTrackPan(get_selected_tracknumber(), pan_amount)

def get_incremented_pan(number):
    return mixer.getTrackPan(get_selected_tracknumber()) + number

def pan_right(increment = 0.1): # 0.1 = 10%
    set_pan(get_incremented_pan(increment))

def pan_left(increment = 0.1):
    set_pan(get_incremented_pan(-increment))

def pan_reset():
    set_pan(0)

def is_pan_left(track_number):
    return mixer.getTrackPan(track_number) < 0

def is_pan_right(track_number):
    return mixer.getTrackPan(track_number) > 0

# conditions
def is_playing():
    return transport.isPlaying() == midi.PM_Playing

def is_stopped():
    return transport.isPlaying() == midi.PM_Stopped

def is_precount():
    return transport.isPlaying == midi.PM_Precount

def is_pattern_mode():
    return transport.getLoopMode() == midi.SM_Pat

def is_song_mode():
    return transport.getLoopMode() == midi.SM_Song

def is_recording():
    return transport.isRecording()

def get_slider_event_id(track_number):
    return mixer.getTrackPluginId(track_number, 0) + midi.REC_Mixer_Vol

def get_slider_event_value(track_number):
    return mixer.getEventValue(track_number)

def go_to_previous_marker(select = False):
    return arrangement.jumpToMarker(-1, select)

def go_to_next_marker(select = False):
    return arrangement.jumpToMarker(1, select)

def link_track_to_channel():
    mixer.linkTrackToChannel(midi.ROUTE_ToThis)

def get_track_color(index =  get_selected_tracknumber()):
    return mixer.getTrackColor(index)

def tap_tempo():
    pass
    # TODO
    #pykeys.send('f5', shift, 1, ctrl, opt_alt)
    # transport.globalTransport(midi.FPT_TapTempo, 1)
    # current_tempo = str(mixer.getCurrentTempo(True))[:-2]
    # show_hint("Tempo: "+current_tempo)

def get_slider_data(event):
    event.inEv = event.data1 + (event.data2 << 7)
    event.outEv = (event.inEv << 16) // 16383
    event.inEv -= 0x2000
    return event.inEv + 0x2000

def set_fader(arguments_in_tuple):
    if callable(arguments_in_tuple[0]):
        track_event_id = get_current_track_event_id(arguments_in_tuple[0]())
    else:
        track_event_id = arguments_in_tuple[0]
    level = arguments_in_tuple[1]
    smooth_speed = arguments_in_tuple[2]
    mixer.automateEvent(track_event_id, level, midi.REC_MIDIController, smooth_speed)

def get_current_track_event_id(track_number):
    return get_slider_event_id(track_number)