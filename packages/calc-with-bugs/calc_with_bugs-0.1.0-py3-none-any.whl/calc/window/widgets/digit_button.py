from typing import Optional

from PyQt6.QtCore import pyqtSignal, pyqtProperty
from PyQt6.QtWidgets import QPushButton, QWidget


class DigitButton(QPushButton):
    pressed = pyqtSignal(int, name="pressed")

    def __init__(self, parent: Optional[QWidget] = None, value: int = 0) -> None:
        super().__init__(parent)
        self._value = value

        self.clicked.connect(self._process_clicked)  # type: ignore

    @pyqtProperty(int)
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    def _process_clicked(self) -> None:
        self.pressed.emit(self.value)
