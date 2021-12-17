import midi

import wrapper

def evaluate_parameter(tuple_parameter):
    result = tuple_parameter
    if type(tuple_parameter) == tuple and len(tuple_parameter) == 1:
        if callable(tuple_parameter[0]):
            result = tuple_parameter[0]()  # return the evaluation of the function inside the tuple
        else:
            result = tuple_parameter[0]  # return the tuple
    else:
        result = tuple_parameter  # is not a tuple
    return result

class Feature:
    def __init__(self):
        self.feature_list = []
        self._event_handled = False
        self.should_use_event_as_argument = False

    def _return_true(self):  # for default feature
        return True

    def inverted(self, function_condition_list):
        return not function_condition_list

    def evaluate_all_conditions_are_false(self):
        is_false = False
        for feature in self.feature_list:
            if len(feature[0]) > 0:
                is_false = is_false or self.evaluate_all_conditions_per_component(feature[0])
        return not is_false

    def evaluate_all_conditions_per_component(self, function_condition_list):
        is_true = True
        for function_condition in function_condition_list:
            is_true = is_true and function_condition()
        return is_true

    def should_run(self, function_condition_list):
        if len(function_condition_list)==0:
            if self.evaluate_all_conditions_are_false():
                return True
            else:
                return False
        elif self.evaluate_all_conditions_per_component(function_condition_list):
            return True
        else:
            return False


    def get_parameters(self, function_parameters_list):
        parameters = None
        if len(function_parameters_list) == 1:
            if callable(function_parameters_list[0]):
                parameters = (function_parameters_list[0]())
            # else:
            #     return function_list[0]  #return first element, as it is the only one
        else:
            parameters = function_parameters_list  #return tuple, for more than one parameter
        return parameters

    def use_event(self):
        self.should_use_event_as_argument = True
        return True

    def exec(self, event):
        for feature in self.feature_list:
            if self.should_run(feature[0]):
                parameters = feature[2:]
                if self.should_use_event_as_argument:
                    feature[1](event)
                    self.should_use_event_as_argument = False
                elif parameters == (None,):
                    feature[1]()
                else:
                    parameter_evaluated = evaluate_parameter(parameters)
                    if parameter_evaluated is tuple:
                        # accept tuple as parameter
                        feature[1](*parameter_evaluated) # prefix * required to accept a tuple
                    else:
                        feature[1](parameter_evaluated)
                self._event_handled = self._event_handled | True  # Event is handled if at least one condition is met
        return self._event_handled

    def add_feature(self, function_condition_list: list, function, *args):
        self.feature_list = self.feature_list + [(function_condition_list, function, *args)]

class Led:
    def __init__(self, id, on_id, off_id):
        self.id = id
        self.on_id = on_id
        self.off_id = off_id
        self._current_status_id = self.off_id

    def set_led_status(self, event, status):
        wrapper.set_led_status_to(event, status)

    def on(self, event):
        self._current_status_id = self.on_id
        self.set_led_status(event)

    def off(self, event):
        self._current_status_id = self.off_id
        self.set_led_status(event)

    def toggle(self, event):
        if self._current_status_id == self.on_id:
            self._current_status_id = self.off_id
        elif self._current_status_id == self.off_id:
            self._current_status_id = self.on_id
        self.set_led_status(event, self._current_status_id)

    def is_led_on(self):
        return self._current_status_id != self.off_id

class BlinkingLed(Led):
    def __init__(self, id, on_id, off_id, blink_id):
        Led.__init__(self, id, on_id, off_id)
        self.blink_id = blink_id

    def blink(self, event):
        self._current_status_id = self.blink_id
        self.set_led_status(event, self._current_status_id)

    def toggle(self, event):
        if self._current_status_id == self.on_id:
            self._current_status_id = self.off_id
        elif self._current_status_id == self.off_id:
            self._current_status_id = self.on_id
        elif self._current_status_id == self.blink_id:
            self._current_status_id = self.off_id
        self.set_led_status(event, self._current_status_id)

class LedRGB(BlinkingLed):
    def __init__(self, id, on_id, off_id):
        Led.__init__(self, id, on_id, off_id)
        self.red = 0
        self.green = 0
        self.blue = 0

    def set_color(self):
        pass

class Button(Feature):
    def __init__(self, id, led_on, led_off, led_blink):
        super().__init__()
        self.id = id
        self.led = BlinkingLed(id, led_on, led_off, led_blink)

    def do_nothing(self):
        pass

    def is_enabled(self):
        return self.led.is_led_on()

    def handle_midi_event(self, event, toggle_led=False):
        if not event.handled and event.data1 == self.id:
            event.handled = self.exec(event)
            if toggle_led:
                self.led.toggle(event)

    def refresh(self, condition):
        wrapper.set_led_on_condition(self.id, condition)

class ButtonRGB(Button):
    def __init__(self, id, led_on, led_off, led_blink, led_red_id, led_green_id, led_blue_id,
                 midi_channel_for_red, midi_channel_for_green, midi_channel_for_blue):
        Button.__init__(self, id, led_on, led_off, led_blink)
        self.led_red_id = led_red_id
        self.led_green_id = led_green_id
        self.led_blue_id = led_blue_id
        self.midi_channel_to_set_red = midi_channel_for_red
        self.midi_channel_to_set_green = midi_channel_for_green
        self.midi_channel_to_set_blue = midi_channel_for_blue
        self.LED_RED_OffOn = [led_red_id, led_red_id + (0x7F << 16)]
        self.LED_GREEN_OffOn = [led_green_id, led_green_id + (0x7F << 16)]
        self.LED_BLUE_OffOn = [led_blue_id, led_blue_id + (0x7F << 16)]
        self.default_color = [50,50,50]
        self.reset_color()

    def change_color_to(self, rgb):
        wrapper.send_midi_message_to_device(self.led_red_id, self.midi_channel_to_set_red, self.id, rgb[0])
        wrapper.send_midi_message_to_device(self.led_green_id, self.midi_channel_to_set_green, self.id, rgb[1])
        wrapper.send_midi_message_to_device(self.led_blue_id, self.midi_channel_to_set_blue, self.id, rgb[2])

    def refresh(self, condition):
        if condition:
            self.change_color_to([255,0,0])
        else:
            self.reset_color()

    def reset_color(self):
        self.change_color_to(self.default_color)

class EndlessEncoder(Feature):
    def __init__(self, id, id_left, id_right, alternative_multiplied_step):
        super().__init__()
        self.id = id
        self.id_right = id_right
        self.id_left = id_left
        self.feature = Feature()
        self.step = 0
        self.MULTIPLY_STEP_BY = alternative_multiplied_step  # ex. for scrolling song faster

    def do_nothing(self):
        pass

    def is_encoder_event(self, event):
        return (event.midiId == midi.MIDI_CONTROLCHANGE) & (event.data1 == self.id)

    def is_left_event(self, event):
        return event.data2 >= self.id_left

    def is_right_event(self, event):
        return (event.data2 <= self.id_left) & (event.data2 >= self.id_right)

    # in my case id_right is 0x41, and 3 steps to the left is 0x44
    def extract_step(self, event):
        if event.data2 >= self.id_left:
            step = event.data2 - self.id_left + 1
        else:
            step = event.data2 - self.id_right + 1
        return step

    def get_step(self):
        return self.step

    def get_step_multiplied(self):
        return self.step * self.MULTIPLY_STEP_BY

    def handle_midi_event_with_feature(self, event):
        if self.is_encoder_event(event):
            self.step = self.extract_step(event)
            result = self.exec(event)
            event.handled = result

class Slider():  # aka Fader
    def __init__(self, id):
        self.id = id
        self.FADER_SMOOTH_SPEED = 469
        self.MAXIMUM_VALUE = round(13072 * 16000 / 12800)

    def track_level_to_slider(self, Value, Max = midi.FromMIDI_Max):
        return round(Value / Max * self.MAXIMUM_VALUE)

    def track_slider_to_level(self, Value, Max = midi.FromMIDI_Max):
        return min(round(Value / self.MAXIMUM_VALUE * Max), Max)

    def pitchbend_number_to_midi_message(self, pitchbend):
        coarse = pitchbend >> 7
        fine = pitchbend - (coarse << 7)
        return (midi.MIDI_PITCHBEND, fine, coarse)

    def midi_message_to_pitchbend_number(self, event):
        return (event.data1 << 7) + event.data2