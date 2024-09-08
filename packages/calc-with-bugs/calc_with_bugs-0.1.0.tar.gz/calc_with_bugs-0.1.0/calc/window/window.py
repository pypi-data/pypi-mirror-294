import webbrowser

from PyQt6.QtWidgets import QMainWindow, QMessageBox

from calc.app import CalcController
from calc.window.design.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
            self,
            controller: CalcController,
    ):
        super().__init__(None)
        self.setupUi(self)
        self.controller = controller

        self.digit_buttons = [
            self.digit_button_0,
            self.digit_button_1,
            self.digit_button_2,
            self.digit_button_3,
            self.digit_button_4,
            self.digit_button_5,
            self.digit_button_6,
            self.digit_button_7,
            self.digit_button_8,
            self.digit_button_9,
        ]

        self.operator_buttons = [
            self.plus_button,
            self.times_button,
            self.minus_button,
            self.divide_button,
        ]

        self._register_signals()

    def _register_signals(self) -> None:
        for button in self.digit_buttons:
            button.pressed.connect(self.controller.add_digit)

        # TODO: Fix bug
        self.digit_button_0.clicked.connect(self.buggy_zero)
        self.mem_clear_button.clicked.connect(self.buggy_memory_clear)

        def set_result(accum: int) -> None:
            self.result_line_edit.setText(str(accum))

        self.controller.accum_changed.connect(set_result)

        def set_argument(text: str) -> None:
            self.controller.argument = int(text or '0')

        self.result_line_edit.textChanged.connect(set_argument)

        for button in self.operator_buttons:
            button.pressed.connect(self.controller.add_operator)

        self.equal_button.clicked.connect(self.controller.execute)

        self.mem_read_button.clicked.connect(self.controller.read_memory)
        self.mem_set_button.clicked.connect(self.controller.set_memory)
        self.mem_add_button.clicked.connect(self.controller.add_memory)
        # TODO: Fix bug
        # self.mem_clear_button.clicked.connect(self.controller.clear_memory)

    def buggy_zero(self) -> None: # TODO: Fix bug
        msg = QMessageBox()
        msg.warning(
            None,
            "Цифра недоступна",
            "Эта цифра недоступна. Чтобы разблокировать эту цифру отправьте 100 рублей по номеру +79771283764",
        )

    def buggy_memory_clear(self) -> None:  # TODO: Fix bug
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", autoraise=True)
