from typing import Optional

from PyQt6.QtCore import pyqtProperty, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QWidget

from calc.app import Operator


class OperatorButton(QPushButton):
    operator = pyqtProperty(str)
    pressed = pyqtSignal(Operator)
    operator_changed = pyqtSignal(str)

    def __init__(
            self,
            parent: Optional[QWidget] = None,
            operator: Operator = Operator.PLUS,
    ) -> None:
        super().__init__(parent)
        self._operator = operator
        self.operator_changed.connect(self.setText)
        self.clicked.connect(self._process_clicked)  # type: ignore

    @operator.getter
    def operator(self) -> Operator:
        return self._operator

    @operator.setter
    def operator(self, operator: Operator) -> None:
        print(operator)
        self._operator = Operator(operator)
        self.operator_changed.emit(str(operator))

    def _process_clicked(self) -> None:
        self.pressed.emit(self.operator)
