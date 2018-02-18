from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from src.term_em import TerminalEmulator
from pyte import control as ctrl, escape as esc

BG_COLOR = (0, 0, 0, 1)
FG_COLOR = (1, 1, 1, 1)


class Terminal(TextInput):
    def __init__(self, **kwargs):
        super(Terminal, self).__init__(
            text='',
            font_name="RobotoMono-Regular",
            background_color=BG_COLOR,
            foreground_color=FG_COLOR,
            cursor_color=FG_COLOR,
            cursor_blink=False,
            **kwargs
        )
        self._term_em = None

    def start(self):
        self._term_em = TerminalEmulator(self.parent.get_connection())
        Clock.schedule_interval(lambda dt: self._term_em.receive(), 0.1)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print(repr(keycode[1]), modifiers)
        if keycode[1] == 'backspace':
            self._term_em.write(ctrl.BS)
        elif keycode[1] == 'up':
            self._term_em.write(ctrl.ESC + '[' + esc.CUU)
        elif keycode[1] == 'down':
            self._term_em.write(ctrl.ESC + '[' + esc.CUD)
        elif keycode[1] == 'left':
            self._term_em.write(ctrl.ESC + '[' + esc.CUB)
        elif keycode[1] == 'right':
            self._term_em.write(ctrl.ESC + '[' + esc.CUF)
        elif 'ctrl' in modifiers:
            if text == 'd':
                self._term_em.write(b'\004')

    def on_touch_down(self, touch):
        super(Terminal, self).on_touch_down(touch)
        self.cursor = self._term_em.get_cursor()
        return True
