"""
My Table Widget
"""
# Built Ins
import sys

# 3rd Party
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Signal

# Owned

class MTableWidget(QtWidgets.QTableWidget):
    """
    A simple Widget based off of QTable Widget which overwrites
    the `keyPressEvent` so we can delete rows with the `Delete` key.
    """
    # CHEATSHEET Block 14

    # CHEATSHEET Block 13 (& 14)
