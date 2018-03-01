from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFontDatabase, QTextCursor, QTextFormat, QTextCharFormat, QFont, QBrush, QColor
from pyte import control as ctrl, escape as esc
from term_em import TerminalEmulator


class Terminal(QTextEdit):
    def __init__(self, parent):
        super(Terminal, self).__init__()

        QApplication.instance().setCursorFlashTime(0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setFont(QFont('Menlo'))
        self.setFontPointSize(12)
        self._default_text_format = self.currentCharFormat()

        self._text_width = self.fontMetrics().maxWidth() + 1.5  # This could be cleaner
        self._text_height = self.fontMetrics().lineSpacing() + 2.3  # This could be cleaner too

        self._parent = parent
        self._term_em: TerminalEmulator = None

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
        self.setText(self._term_em.get_text())

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
        if key == Qt.Key_Backspace:
            return w(ctrl.BS)
        elif key == Qt.Key_Up:
            self._term_em.key_up()
        elif key == Qt.Key_Down:
            self._term_em.key_down()
        elif key == Qt.Key_Left:
            self._term_em.key_left()
        elif key == Qt.Key_Right:
            self._term_em.key_right()
        elif key == Qt.Key_Escape:
            return w(ctrl.ESC)
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
        line_nums = self._term_em.dirty_lines()
        if line_nums:
            for line_num in line_nums:
                line = self._term_em.get_line(line_num)
                line_extra = self._term_em.get_line_styles(line_num)
                # replace line
                cursor: QTextCursor = self.textCursor()
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line_num)
                cursor.select(QTextCursor.LineUnderCursor)
                # cursor.insertText(line)
                for char in line_extra:
                    text_format: QTextCharFormat = QTextCharFormat()
                    text_format.merge(self._default_text_format)
                    # data, fg, bg, bold, italics, underscore, strikethrough, reverse
                    if char.fg != 'default':
                        text_format.setForeground(QColor(char.fg))
                    if char.bg != 'default':
                        text_format.setBackground(QColor(char.bg))
                    if char.bold:
                        text_format.setFontWeight(QFont.Bold)
                    if char.italics:
                        text_format.setFontItalic(True)
                    if char.underscore:
                        text_format.setFontUnderline(True)
                    if char.strikethrough:
                        text_format.setFontStrikeOut(True)
                    if char.reverse:
                        ...
                    cursor.setCharFormat(text_format)
                    cursor.insertText(char.data)
                self.setTextCursor(cursor)
            self._term_em.clear_dirty()
        x, y = self._term_em.get_cursor()
        curs: QTextCursor = self.textCursor()
        new_position = x + (self._width + 1) * y
        if curs.position() != new_position:
            curs.setPosition(new_position)
            self.setTextCursor(curs)
