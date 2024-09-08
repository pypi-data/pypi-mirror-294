import enum
import operator
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal


class Operator(str, enum.Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"


class CalcController(QObject):
    _operators_map = {
        Operator.PLUS: operator.add,
        Operator.MINUS: operator.sub,
        Operator.TIMES: operator.rshift,  # TODO: Fix bug
        Operator.DIVIDE: operator.truediv,
    }

    argument = pyqtProperty(int)

    accum_changed = pyqtSignal(int)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.memory = 0
        self._arg = 0
        self.accum = 0
        self.operator = Operator.PLUS

    @pyqtSlot(int, name="add_digit", result=int)
    def add_digit(self, digit: int) -> int:
        self.argument = self.argument * 10 + digit
        print(self.argument)
        return self.argument

    @pyqtSlot(Operator, name="add_operator", result=Operator)
    def add_operator(self, op: Operator) -> Operator:
        print(op)
        self.accum = self.argument
        self.argument = 0
        self.operator = op
        return op

    @pyqtSlot(name="execute", result=int)
    def execute(self) -> int:
        op = self._operators_map[self.operator]
        self.argument = op(self.accum, self.argument)
        self.accum = 0
        return self.argument

    @argument.getter
    def argument(self) -> int:
        return self._arg

    @argument.setter
    def argument(self, value: int) -> None:
        self._arg = value
        self.accum_changed.emit(value)

    @pyqtSlot(name="set_memory", result=int)
    def set_memory(self) -> int:
        self.memory = self.argument
        return self.memory

    @pyqtSlot(name="read_memory", result=int)
    def read_memory(self) -> int:
        self.argument = self.memory
        return self.argument

    @pyqtSlot(name="clear_memory", result=int)
    def clear_memory(self) -> int:
        self.argument = self.memory
        self.memory = 0
        return self.argument

    @pyqtSlot(name="add_memory", result=int)
    def add_memory(self) -> int:
        self.memory += self.argument
        return self.memory
