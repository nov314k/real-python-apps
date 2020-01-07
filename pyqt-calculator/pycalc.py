#!/usr/bin/env python3

# Filename: pycalc.py

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""PyCalc is a simple calculator built using Python and PyQt5.

It was created following: https://realpython.com/python-pyqt-gui-calculator/
Minimally changed and adapted relative to the original code.

"""

import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

ERROR_MSG = "ERROR"


class PyCalcInterface(QMainWindow):
    """PyCalc graphical user interface."""

    def __init__(self):
        """Init PyCalcInterface."""
        super().__init__()
        self.setWindowTitle('PyCalc')
        self.setFixedSize(235, 235)
        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)
        self._create_display()
        self._create_buttons()

    def _create_display(self):
        """Create calculator display screen (line)."""
        self.display_screen = QLineEdit()
        self.display_screen.setFixedHeight(35)
        self.display_screen.setAlignment(Qt.AlignRight)
        self.display_screen.setReadOnly(True)
        self.general_layout.addWidget(self.display_screen)

    def _create_buttons(self):
        """Create and arrange calculator buttons."""
        self.buttons = {}
        buttons_layout = QGridLayout()
        buttons_arrangement = {
                '7': (0, 0),
                '8': (0, 1),
                '9': (0, 2),
                '/': (0, 3),
                'C': (0, 4),
                '4': (1, 0),
                '5': (1, 1),
                '6': (1, 2),
                '*': (1, 3),
                '(': (1, 4),
                '1': (2, 0),
                '2': (2, 1),
                '3': (2, 2),
                '-': (2, 3),
                ')': (2, 4),
                '0': (3, 0),
                '000': (3, 1),
                '.': (3, 2),
                '+': (3, 3),
                '=': (3, 4)
        }
        for btn_text, pos in buttons_arrangement.items():
            self.buttons[btn_text] = QPushButton(btn_text)
            self.buttons[btn_text].setFixedSize(40, 40)
            buttons_layout.addWidget(self.buttons[btn_text], pos[0], pos[1])
        self.general_layout.addLayout(buttons_layout)

    def set_display_text(self, text):
        """Set text to, and focus on, calculator display screen."""
        self.display_screen.setText(text)
        self.display_screen.setFocus()

    def display_text(self):
        """Get text from the calculator display screen."""
        return self.display_screen.text()

    def clear_display(self):
        """Clear calculator display screen."""
        self.set_display_text("")


class PyCalcController:
    """PyCalc controller."""

    def __init__(self, model, view):
        """Init PyClalc controller."""
        self._model = model
        self._view = view
        self._connect_signals()

    def _connect_signals(self):
        """Connect event signals."""
        for btn_text, btn in self._view.buttons.items():
            if btn_text not in {'=', 'C'}:
                btn.clicked.connect(partial(self._build_expression, btn_text))
        self._view.buttons['='].clicked.connect(self._calculate_result)
        self._view.display_screen.returnPressed.connect(self._calculate_result)
        self._view.buttons['C'].clicked.connect(self._view.clear_display)

    def _build_expression(self, pressed_button):
        """Build up an expression as the user selects digits and operators."""
        if self._view.display_text() == ERROR_MSG:
            self._view.clear_display()
        expression = self._view.display_text() + pressed_button
        self._view.set_display_text(expression)

    def _calculate_result(self):
        """Convey between model and controller to calculate the result."""
        result = self._model.evaluate_expression(
                expression=self._view.display_text())
        self._view.set_display_text(result)


class PyCalcModel():
    """PyCalc model (logic)."""

    @staticmethod
    def evaluate_expression(expression):
        """Evaluate the expression that the user has built up."""
        try:
            result = str(eval(expression, {}, {}))
        except Exception:
            result = ERROR_MSG
        return result


def main():
    """Main function."""
    pycalc_app = QApplication(sys.argv)
    view = PyCalcInterface()
    view.show()
    model = PyCalcModel()
    PyCalcController(model, view)
    sys.exit(pycalc_app.exec_())


if __name__ == '__main__':
    main()
