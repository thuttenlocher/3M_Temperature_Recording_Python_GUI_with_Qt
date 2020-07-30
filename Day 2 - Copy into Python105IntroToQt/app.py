"""
Entry point to the Qt GUI
"""

# Built Ins
import sys
import random
import time
from datetime import datetime
from bisect import insort

# 3rd Party
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTime, QDate, Qt
import numpy as np
import matplotlib
import matplotlib.dates as mdates


# Owned
import resources # Kinda 3rd party, but exists locally.

# CHEATSHEET Block 1
from widgets.table_widget import TemperatureTable

# Needed for PyInstaller with Windows
try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PySide2.QtWinExtras import QtWin
    myappid = 'com.learnpyqt.mmm.python105'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass

class WindowWrapper(QtCore.QObject):
    """
    Our MainWindow Class
    """
    def __init__(self, *args, **kwargs):
        """ Constructor """

        super(WindowWrapper, self).__init__()

        # ==========================================================================================
        # Load custom widgets and UI file.
        # ==========================================================================================
        loader = QUiLoader()
        # CHEATSHEET Block 2 [2 lines]
    

        self.ui = loader.load(':/ui/mainwindow.ui', None)
        self.ui.show()

        # ==========================================================================================
        # SIGNAL/SLOT CONNECTIONS
        # ==========================================================================================
        self.ui.btn_login.clicked.connect(self.slot_btn_login)
        # CHEATSHEET Block 3

        # ==========================================================================================
        # TABLE AND PLOTS
        # ==========================================================================================
        # CHEATSHEET Block 4
        self._plot_ref = None

        # ==========================================================================================
        # INITIALIZE THE GUI
        # ==========================================================================================
        self.initialize_gui()

    def initialize_gui(self):
        """
        Initialize the gui, default and fields that should have defaults.
        """
        # CHEATSHEET Block 5
        # CHEATSHEET Block 6
        


        # Plot stuff
        # CHEATSHEET Block 7


    # ##############################################################################################
    # SLOTS
    # ##############################################################################################

    def slot_btn_login(self):
        """
        Slot for login button:
            On valid login, switch to the second page.
        """
        username = self.ui.line_edit_username.text()
        password = self.ui.line_edit_password.text()
        self.ui.stacked_widget.setCurrentIndex(1)

    # CHEATSHEET Block 8

    # CHEATSHEET Block 9

    # CHEATSHEET Block 10

    # CHEATSHEET Block 11

    # ##############################################################################################
    # Update functions.
    # ##############################################################################################
    # CHEATSHEET Block 12


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/icon/3m.png')) # Set the window icon.
    main = WindowWrapper()
    sys.exit(app.exec_())
