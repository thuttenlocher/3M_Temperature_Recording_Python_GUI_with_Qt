"""
Matplot lib widgets
"""

# Built Ins

# 3rd Party
from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure

# Owned


class NavigationToolbar(NavigationToolbar2QT):
    """
    Navigation Toolbar for MplWidget.
    Functions we can overwrite:
    https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/backend_qt5.py#L723
    """
    def edit_parameters(self):
        print("before")
        super(NavigationToolbar, self).edit_parameters()
        print("after")


# ------------ ------ MplWidget ------------------ 
class MplWidget(QWidget): 
    """
    Maplotlib Widget used to show Matplotlib graphs/plots.

    Attributes:
        figure (matplotlib.figure.Figure): Figure used by the Widget.
        canvas (FigureCanvas): Matplotlib Canvas used by the Widget.
    """
    def __init__(self, parent, *args, **kwargs): # Important, we must pass parent so QActions aren't deleted
        """ Constructor """
        super(MplWidget, self).__init__(*args, **kwargs)
        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
