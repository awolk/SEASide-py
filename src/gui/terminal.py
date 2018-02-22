from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFontDatabase
from pyte import control as ctrl, escape as esc
from term_em import TerminalEmulator


class Terminal(QTextEdit):
    def __init__(self, parent):
        super(Terminal, self).__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setFontPointSize(12)
        self._text_width = self.fontMetrics().maxWidth() + 1.5  # This could be cleaner
        self._text_height = self.fontMetrics().lineSpacing() + 2.3  # This could be cleaner too
        # self.setStyleSheet('background-color: black; color: white')
        self._parent = parent
        self._term_em = None

    def start(self):
        self._term_em = TerminalEmulator(self._parent.get_connection())
        self._resize(self.width(), self.height())
        timer = QTimer(self)
        timer.timeout.connect(self._check_input)
        timer.start(0)  # TODO: Prevent input checking blocking: make changing text more efficient (using dirty fields)

    def _resize(self, width, height):
        self._height = int(height / self._text_height)
        self._width = int(width / self._text_width)
        self._term_em.resize(self._height, self._width)

    def resizeEvent(self, evt):
        size = evt.size()
        width = size.width()
        height = size.height()
        self._resize(width, height)
        super(Terminal, self).resizeEvent(evt)

    def keyPressEvent(self, evt):
        key = evt.key()

        modifiers = evt.modifiers()
        shift = bool(modifiers & Qt.ShiftModifier)
        control = bool(modifiers & Qt.ControlModifier)
        alt = bool(modifiers & Qt.AltModifier)
        meta = bool(modifiers & Qt.MetaModifier)  # ctrl

        text = evt.text()

        w = self._term_em.write
        cursor_escape = 'O' if 32 in self._term_em._screen.mode else '['
        if key == Qt.Key_Backspace:
            return w(ctrl.BS)
        elif key == Qt.Key_Up:
            return w(ctrl.ESC + cursor_escape + esc.CUU)
        elif key == Qt.Key_Down:
            return w(ctrl.ESC + cursor_escape + esc.CUD)
        elif key == Qt.Key_Left:
            return w(ctrl.ESC + cursor_escape + esc.CUB)
        elif key == Qt.Key_Right:
            return w(ctrl.ESC + cursor_escape + esc.CUF)
        elif meta:
            if text == ' ':
                return w(b'\000')
            elif ord('A') <= key <= ord('Z'):
                return w(chr(key - ord('A') + 1))
            elif text == '[':
                return w('\033')
            elif text == '\\':
                return w('\034')
            elif text == ']':
                return w('\035')
            elif text == '~':
                return w('\036')
            elif text == '?':
                return w('\037')
        else:
            w(text)

    @pyqtSlot()
    def _check_input(self):
        self._term_em.receive()
        if self._term_em.is_dirty():
            self._term_em.clear_dirty()
            self.setText(self._term_em.get_text())
        x, y = self._term_em.get_cursor()
        curs = self.textCursor()
        curs.setPosition(x + (self._width + 1) * y)
        self.setTextCursor(curs)
