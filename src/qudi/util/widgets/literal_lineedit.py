"""
This module provides QWidget subclasses to enter different literals (complex, dict, list, tuple,
set).

Copyright (c) 2021, the qudi developers. See the AUTHORS.md file at the top-level directory of this
distribution and on <https://github.com/Ulm-IQO/qudi-core/>

This file is part of qudi.

Qudi is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Qudi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with qudi.
If not, see <https://www.gnu.org/licenses/>.
"""

__all__ = [
    'ComplexLineEdit',
    'ComplexValidator',
    'DictLineEdit',
    'DictValidator',
    'ListLineEdit',
    'ListValidator',
    'LiteralLineEdit',
    'LiteralValidator',
    'SetLineEdit',
    'SetValidator',
    'TupleLineEdit',
    'TupleValidator',
]

from collections.abc import Mapping, MutableSequence, Sequence
from typing import Any

from PySide6 import QtCore, QtGui, QtWidgets


class LiteralValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> Any:
        return eval(text)

    def text_from_value(self, value: Any) -> str:
        return repr(value)


class ComplexValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except ValueError:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> complex:
        return complex(text)

    def text_from_value(self, value: complex) -> str:
        if value is None:
            value = complex()
        return repr(complex(value))


class ListValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> list[Any]:
        tmp = eval(text)
        if isinstance(tmp, (list, tuple)):
            return list(tmp)
        raise ValueError

    def text_from_value(self, value: MutableSequence[Any]) -> str:
        if value is None:
            value = list()
        return repr(list(value))


class TupleValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> tuple[Any, ...]:
        tmp = eval(text)
        if isinstance(tmp, tuple):
            return tmp
        raise ValueError

    def text_from_value(self, value: Sequence[Any]) -> str:
        if value is None:
            value = tuple()
        return repr(tuple(value))


class SetValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> set[Any]:
        tmp = eval(text)
        if isinstance(tmp, (tuple, set, frozenset)):
            return set(tmp)
        raise ValueError

    def text_from_value(self, value: set[Any] | frozenset[Any]) -> str:
        if value is None:
            value = set()
        return repr(set(value))


class DictValidator(QtGui.QValidator):
    """ """

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, text: str, position: int) -> QtGui.QValidator.State:
        """ """
        try:
            self.value_from_text(text)
            return self.Acceptable
        except:
            return self.Intermediate

    def fixup(self, text: str) -> str:
        return text

    def value_from_text(self, text: str) -> dict[Any, Any]:
        tmp = eval(text)
        if isinstance(tmp, dict):
            return tmp
        elif isinstance(tmp, tuple):
            return dict(tmp)
        raise ValueError

    def text_from_value(self, value: Mapping[Any, Any]) -> str:
        if value is None:
            value = dict()
        return repr(dict(value))


class LiteralLineEdit(QtWidgets.QLineEdit):
    """ """

    valueChanged = QtCore.Signal(object)

    def __init__(
        self,
        value: Any | None = None,
        parent: QtWidgets.QWidget | None = None,
        validator: QtGui.QValidator | None = None,
    ):
        super().__init__(parent=parent)
        if validator is None:
            validator = LiteralValidator()
        self._last_valid_text = ''
        self.setValidator(validator)
        self.setValue(value)

    def setValue(self, value: Any) -> None:
        """ """
        validator = self.validator()
        text = validator.fixup(validator.text_from_value(value))
        if self._new_text_valid(text):
            self.setText(text)
            self._last_valid_text = text
            self.valueChanged.emit(self.value())
        elif text != self._last_valid_text:
            raise ValueError

    def value(self) -> Any:
        """ """
        return self.validator().value_from_text(self._last_valid_text)

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        self._revert_text()
        return super().focusOutEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        check_text = True
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self._revert_text()
            check_text = False
        ret_val = super().keyPressEvent(event)
        if check_text:
            text = self.text()
            if self._new_text_valid(text):
                self._last_valid_text = text
                self.valueChanged.emit(self.value())
        return ret_val

    def _revert_text(self) -> None:
        text = self.text()
        if self.validator().validate(text, len(text)) != QtGui.QValidator.Acceptable:
            self.setText(self._last_valid_text)

    def _new_text_valid(self, text: str) -> bool:
        """Helper method to check if the given text is suitable to replace the current text as
        valid value.
        """
        if text != self._last_valid_text:
            validator = self.validator()
            return validator.validate(text, len(text)) == QtGui.QValidator.Acceptable
        return False


class ComplexLineEdit(LiteralLineEdit):
    """ """

    valueChanged = QtCore.Signal(complex)

    def __init__(self, value: complex | None = None, parent: QtWidgets.QWidget | None = None):
        if value is None:
            value = complex()
        super().__init__(value=value, parent=parent, validator=ComplexValidator())


class ListLineEdit(LiteralLineEdit):
    """ """

    valueChanged = QtCore.Signal(list)

    def __init__(self, value: MutableSequence | None = None, parent: QtWidgets.QWidget | None = None):
        if value is None:
            value = list()
        super().__init__(value=value, parent=parent, validator=ListValidator())


class TupleLineEdit(LiteralLineEdit):
    """ """

    valueChanged = QtCore.Signal(tuple)

    def __init__(self, value: Sequence | None = None, parent: QtWidgets.QWidget | None = None):
        if value is None:
            value = tuple()
        super().__init__(value=value, parent=parent, validator=TupleValidator())


class SetLineEdit(LiteralLineEdit):
    """ """

    valueChanged = QtCore.Signal(set)

    def __init__(self, value: set | frozenset | None = None, parent: QtWidgets.QWidget | None = None):
        if value is None:
            value = set()
        super().__init__(value=value, parent=parent, validator=SetValidator())


class DictLineEdit(LiteralLineEdit):
    """ """

    valueChanged = QtCore.Signal(dict)

    def __init__(self, value: Mapping | None = None, parent: QtWidgets.QWidget | None = None):
        if value is None:
            value = dict()
        super().__init__(value=value, parent=parent, validator=DictValidator())
