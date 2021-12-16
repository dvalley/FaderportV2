# FLStudio API modules
import device
import general
import mixer
# Python libraries already included
import midi
# Custom libraries
import wrapper
import components

class Controller():
    def __init__(self, controller):
        self.controller = controller

        self.fader = components.Slider(controller.FADER)
        self.MULTIPLY_STEP_BY = 100
        self.encoder_turn_left = components.EndlessEncoder(controller.ENCODER, controller.ENCODER_MIN_STEP_LEFT, controller.ENCODER_MIN_STEP_RIGHT, self.MULTIPLY_STEP_BY)
        self.encoder_turn_right = components.EndlessEncoder(controller.ENCODER, controller.ENCODER_MIN_STEP_LEFT, controller.ENCODER_MIN_STEP_RIGHT, self.MULTIPLY_STEP_BY)

        self.solo_button = components.Button(controller.SOLO, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.mute_button = components.Button(controller.MUTE, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.arm_button = components.Button(controller.ARM, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.shift_button = components.Button(controller.SHIFT, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

        self.bypass_button = components.Button(controller.BYPASS, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.touch_button = components.ButtonRGB(controller.TOUCH, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                      controller.RED, controller.GREEN, controller.BLUE,
                                                 controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                 controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)
        self.write_button = components.ButtonRGB(controller.WRITE, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                      controller.RED, controller.GREEN, controller.BLUE,
                                                 controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                 controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)
        self.read_button = components.ButtonRGB(controller.READ, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                     controller.RED, controller.GREEN, controller.BLUE,
                                                controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)

        self.prev_button = components.Button(controller.PREV, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

        self.encoder_button = components.Button(controller.PUSH_ENCODER, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

        self.next_button = components.Button(controller.NEXT, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

        self.link_button = components.ButtonRGB(controller.LINK, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                     controller.RED, controller.GREEN, controller.BLUE,
                                                controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)
        self.pan_button = components.ButtonRGB(controller.PAN, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                    controller.RED, controller.GREEN, controller.BLUE,
                                               controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                               controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)
        self.channel_button = components.ButtonRGB(controller.CHANNEL, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                        controller.RED, controller.GREEN, controller.BLUE,
                                                   controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                   controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)
        self.scroll_button = components.ButtonRGB(controller.SCROLL, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK,
                                       controller.RED, controller.GREEN, controller.BLUE,
                                                  controller.MIDI_CHANNEL_TO_SET_RED_COLOR, controller.MIDI_CHANNEL_TO_SET_GREEN_COLOR,
                                                  controller.MIDI_CHANNEL_TO_SET_BLUE_COLOR)

        self.master_button = components.Button(controller.MASTER, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.click_button = components.Button(controller.CLICK, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.section_button = components.Button(controller.SECTION, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.marker_button = components.Button(controller.MARKER, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

        self.loop_button = components.Button(controller.LOOP, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.rewind_button = components.Button(controller.REWIND, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.fast_forward_button = components.Button(controller.FAST_FORWARD, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.stop_button = components.Button(controller.STOP, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.play_button = components.Button(controller.PLAY, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)
        self.record_button = components.Button(controller.RECORD, controller.LED_ON, controller.LED_OFF, controller.LED_BLINK)

    def OnInit(self):
        self.update_leds()
        # Setting controller logic as features
        # Feature = ([conditions list], function name, extra parameters if any)
        self.encoder_button.add_feature([self.pan_button.is_enabled], wrapper.pan_reset, None)

        self.encoder_turn_left.add_feature([self.pan_button.is_enabled], wrapper.pan_left, None)
        self.encoder_turn_left.add_feature([self.marker_button.is_enabled], wrapper.go_to_previous_marker, None)
        self.encoder_turn_left.add_feature([self.scroll_button.is_enabled], wrapper.scroll_to_left, self.encoder_turn_left.get_step)
        self.encoder_turn_left.add_feature([self.shift_button.is_enabled, self.scroll_button.is_enabled], wrapper.scroll_to_left, self.encoder_turn_left.get_step_multiplied)
        self.encoder_turn_left.add_feature([self.shift_button.is_enabled, self.marker_button.is_enabled], wrapper.go_to_previous_marker, True)
        self.encoder_turn_left.add_feature([], wrapper.select_previous_track, None) # default

        self.encoder_turn_right.add_feature([self.pan_button.is_enabled], wrapper.pan_right, None)
        self.encoder_turn_right.add_feature([self.marker_button.is_enabled], wrapper.go_to_next_marker, None)
        self.encoder_turn_right.add_feature([self.scroll_button.is_enabled], wrapper.scroll_to_right, self.encoder_turn_right.get_step)
        self.encoder_turn_right.add_feature([self.shift_button.is_enabled, self.scroll_button.is_enabled], wrapper.scroll_to_right, self.encoder_turn_right.get_step_multiplied)
        self.encoder_turn_right.add_feature([self.shift_button.is_enabled, self.marker_button.is_enabled], wrapper.go_to_next_marker, True)
        self.encoder_turn_right.add_feature([], wrapper.select_next_track, None) # default

        # Buttons
        self.solo_button.add_feature([], wrapper.solo, wrapper.get_selected_tracknumber)
        self.mute_button.add_feature([], wrapper.mute, wrapper.get_selected_tracknumber)
        self.mute_button.add_feature([self.shift_button.is_enabled], wrapper.mute_clear, None)
        self.arm_button.add_feature([], wrapper.arm, None)

        self.bypass_button.add_feature([], wrapper.open_next_plugin, None)
        self.bypass_button.add_feature([self.shift_button.is_enabled], wrapper.close_window, None)
        self.touch_button.add_feature([], wrapper.open_previous_plugin, None)
        self.write_button.add_feature([self.write_button.use_event], wrapper.snap, None)

        self.prev_button.add_feature([self.shift_button.is_enabled], wrapper.undo, None)
        self.prev_button.add_feature([], wrapper.select_previous_track, None)
        self.next_button.add_feature([self.shift_button.is_enabled], wrapper.redo, None)
        self.next_button.add_feature([], wrapper.select_next_track, None)

        self.master_button.add_feature([], wrapper.tap_tempo, None)
        self.click_button.add_feature([self.click_button.use_event], wrapper.metronome)

        self.play_button.add_feature([self.shift_button.is_enabled], wrapper.play_stop, None)
        self.play_button.add_feature([self.play_button.use_event], wrapper.play_pause, None)
        self.stop_button.add_feature([self.stop_button.use_event], wrapper.stop, None)
        self.loop_button.add_feature([self.loop_button.use_event], wrapper.song_loop, None)
        self.record_button.add_feature([self.record_button.use_event], wrapper.record, None)
        self.rewind_button.add_feature([self.rewind_button.use_event], wrapper.rewind, None)
        self.fast_forward_button.add_feature([self.fast_forward_button.use_event], wrapper.fast_forward, None)

        wrapper.show_hint(f'{self.controller.NAME} controller linked')

    def OnDeInit(self):
        wrapper.show_hint(f'{self.controller.NAME} controller unlinked')

    def OnRefresh(self, flags):
        print('OnRefresh')

        if flags & midi.HW_Dirty_Mixer_Sel:
            print('Mixer_Sel')
            pass
        if flags & midi.HW_Dirty_Mixer_Display:
            print('Mixer_Display')
            pass
        if flags & midi.HW_Dirty_Mixer_Controls:
            self.update_device_fader()
        if flags & midi.HW_Dirty_LEDs:
            self.update_leds()

    def update_device_fader(self):
        track_number = wrapper.get_selected_tracknumber()
        trackEventId = wrapper.get_slider_event_id(track_number)
        level = wrapper.get_slider_event_value(trackEventId)
        pitchbend = self.fader.track_level_to_slider(level)
        midi_pitchbend_data = self.fader.pitchbend_number_to_midi_message(pitchbend)
        if device.isAssigned():
            wrapper.send_midi_message_to_device(midi_pitchbend_data[0], self.controller.FADER_MIDI_CHANNEL,
                                                        midi_pitchbend_data[1], midi_pitchbend_data[2])

    def OnMidiMsg(self, event):
        self.rewind_button.handle_midi_event(event, toggle_led=True)
        self.fast_forward_button.handle_midi_event(event, toggle_led=True)

        if wrapper.is_note_on(event):
            self.play_button.handle_midi_event(event, toggle_led=True)
            self.stop_button.handle_midi_event(event, toggle_led=True)
            self.loop_button.handle_midi_event(event, toggle_led=True)
            self.record_button.handle_midi_event(event, toggle_led=True)

            self.solo_button.handle_midi_event(event, toggle_led=True)
            self.mute_button.handle_midi_event(event, toggle_led=True)
            self.arm_button.handle_midi_event(event, toggle_led=True)

            self.shift_button.handle_midi_event(event, toggle_led=True)

            self.bypass_button.handle_midi_event(event, toggle_led=False)
            self.touch_button.handle_midi_event(event, toggle_led=False)
            self.write_button.handle_midi_event(event, toggle_led=True)
            self.read_button.handle_midi_event(event, toggle_led=True)

            self.prev_button.handle_midi_event(event, toggle_led=False)
            self.next_button.handle_midi_event(event, toggle_led=False)

            self.link_button.handle_midi_event(event, toggle_led=True)
            self.pan_button.handle_midi_event(event, toggle_led=True)
            self.channel_button.handle_midi_event(event, toggle_led=True)
            self.scroll_button.handle_midi_event(event, toggle_led=True)
            self.master_button.handle_midi_event(event, toggle_led=False)
            self.click_button.handle_midi_event(event, toggle_led=True)
            self.section_button.handle_midi_event(event, toggle_led=True)
            self.marker_button.handle_midi_event(event, toggle_led=True)

            self.encoder_button.handle_midi_event(event)

    def OnControlChange(self, event):
        if self.encoder_turn_left.is_left_event(event):
            self.encoder_turn_left.handle_midi_event_with_feature(event)
        elif self.encoder_turn_right.is_right_event(event):
            self.encoder_turn_right.handle_midi_event_with_feature(event)

    def OnPithBend(self, event):
        trackEventId = wrapper.get_slider_event_id(wrapper.get_selected_tracknumber())
        level = self.fader.track_slider_to_level(wrapper.get_slider_data(event))
        mixer.automateEvent(trackEventId, level,
                            midi.REC_MIDIController, self.fader.FADER_SMOOTH_SPEED)
        event.handled = True

    def update_leds(self):
        selected_tracknumber = wrapper.get_selected_tracknumber()
        if device.isAssigned():
            self.stop_button.refresh(wrapper.is_stopped())
            self.loop_button.refresh(wrapper.is_pattern_mode())
            self.record_button.refresh(wrapper.is_recording())
            # changed flag
            self.read_button.refresh(general.getChangedFlag() > 0)
            # channel strip
            self.solo_button.refresh(wrapper.is_solo(selected_tracknumber))
            self.mute_button.refresh(wrapper.is_muted(selected_tracknumber))
            self.arm_button.refresh(wrapper.is_armed(selected_tracknumber))
            if self.pan_button.is_enabled():
                self.prev_button.refresh(wrapper.is_pan_left(selected_tracknumber))
                self.next_button.refresh(wrapper.is_pan_right(selected_tracknumber))
            else:
                self.prev_button.refresh(False)
                self.next_button.refresh(False)