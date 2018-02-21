from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QPoint
from PyQt5.QtGui import QFontDatabase, QTextCursor
from pyte import control as ctrl, escape as esc
from term_em import TerminalEmulator


class Terminal(QTextEdit):
    def __init__(self, parent):
        super(Terminal, self).__init__()
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setFontPointSize(12)
        # self.setStyleSheet('background-color: black; color: white')
        self._parent = parent

    def start(self):
        self._term_em = TerminalEmulator(self._parent.get_connection())
        timer = QTimer(self)
        timer.timeout.connect(self._check_input)
        timer.start(0)

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
        x, y = self._term_em.get_cursor()
        curs = self.textCursor()
        curs.setPosition(x + 81 * y)  # TODO: Remove hardcoded width
        self.setTextCursor(curs)
        if self._term_em.is_dirty():
            self._term_em.clear_dirty()
            self.setText(self._term_em.get_text())
