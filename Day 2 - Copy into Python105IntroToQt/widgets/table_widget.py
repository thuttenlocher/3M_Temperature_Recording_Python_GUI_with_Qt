"""
This is the controller we use to work with the QTableWidget and
its items.
"""

# Built In
import bisect
from typing import List, Any
from datetime import datetime

# 3rd Party
from PySide2.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QMessageBox
)
from PySide2.QtCore import Qt

# Owned



class TableWidgetItem(QTableWidgetItem):
    """
    Create a child class off of QTableWidgetItem so we can properly
    handle sorting the table by date.
    """
    def __init__(self, data_type, *args, **kwargs):
        """
        Use parents constructor, except added a new argument which is the
        data type of the value passed to the QTableWidgetItem.
        In other words, pass `tpye(your_var)` as the first argument to this
        constructor.
        """
        super(TableWidgetItem, self).__init__(*args, **kwargs)
        self.data_type = data_type

    def __lt__(self, other):
        """
        If the data type is a datetime object then we will conver the strings to dates
        and compare the dates for sorting, objects native less than operator.
        """
        if isinstance(self.data_type, datetime):
            d1 = datetime.strptime(self.data(Qt.EditRole), "%Y-%m-%dT%H:%M:%S")
            d2 = datetime.strptime(other.data(Qt.EditRole), "%Y-%m-%dT%H:%M:%S")
            return d1 < d2
        return self.data(Qt.EditRole) < other.data(Qt.EditRole)


class TemperatureTable:
    """
    Controller class to work with the table in our GUI. Handles
    storing and manipulation the data.

    Attributes:
        table (QTableWidget): The reference to the QTableWidget used in the GUI.
        num_columns (int): The number of columns the table should have.
        rows (List[List[Any]]): A list of lists where each list is a row in the table.
                                Rows are sorted by the datetime field.
    """
    def __init__(self, table: QTableWidget, num_columns: int):
        """
        Constructor

        Args:
            table: A reference to the QTableWidget used in the GUI.
            num_columns: The number of columns that the table should have.
        """
        self.table = table
        self.num_columns = num_columns
        self.rows = []
        self.table.setHorizontalHeaderLabels(['Timestamp', 'Temp.', 'Notes'])

    def cell_updated(self, row: int, col: int) -> None:
        """
        This function should be called when a cell in the table is updated (SLOT).
        Handles changing the value in the `rows` field and updating the table.

        Args:
            row (int): The index of the row that was changed.
            col (int): The index of the column that was changed.
        """
        if col == 0: # Datetime changed
            try:
                self.rows[row][col] = datetime.strptime(
                    self.table.item(row, col).data(Qt.EditRole),
                    "%Y-%m-%dT%H:%M:%S"
                )
            except ValueError:
                # A bad value was entered, throw up a message box.
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Invalid datetime format")
                msg.setInformativeText('The updated datetime was invalid.')
                msg.setWindowTitle("Error")
                msg.exec_()
        elif col == 1: # Temperature changed
            self.rows[row][col] = int(self.table.item(row, col).data(Qt.EditRole))
        else: # Notes changed
            self.rows[row][col] = self.table.item(row, col).data(Qt.EditRole)

        self.rows.sort() # Sort the rows O(N LOGN)
        self.update()

    def insert_row(self, timestamp: datetime, temp: int, notes: str) -> None:
        """
        Insert the given fields as a row in the table.

        Args:
            timestamp (datetime): The datetime the data was taken (Local Time).
            temp (int): The temperature reading.
            notes (str): Notes about the data entry.
        """
        # Bisect is just a quick way to insert a row into a sorted list
        # O(LOGN)
        bisect.insort(self.rows, [timestamp, temp, notes])
        self.update()

    def update(self) -> None:
        """
        Update the QTableWidget with `rows` attribute.
        """
        self.table.blockSignals(True) # Prevent the cellChanged from being called (as well as all other)
        self.table.setRowCount(0) # Delete all rows from table

        # Disable sorting until the data is all added. Otherwise issues may occur
        sorting_status = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)

        for row_number, row in enumerate(self.rows):
            if len(row) != self.num_columns:
                raise ValueError(
                    f"Number of fields in iterable ({len(row)}) "
                    f"does not match number of columns in table ({self.num_columns})."
                )
            timestamp, temp, notes = row
            self.table.insertRow(row_number) # Add blank row

            # Add timestamp
            table_item = TableWidgetItem(type(timestamp))
            table_item.setData(Qt.EditRole, timestamp.isoformat())
            self.table.setItem(row_number, 0, table_item)

            # Add temperature
            table_item = TableWidgetItem(type(temp))
            table_item.setData(Qt.EditRole, str(temp))
            self.table.setItem(row_number, 1, table_item)

            # Add notes
            table_item = TableWidgetItem(type(notes))
            table_item.setData(Qt.EditRole, str(notes))
            self.table.setItem(row_number, 2, table_item)

        self.table.setSortingEnabled(sorting_status) # Set the table sorting status back to what it was.
        self.table.sortItems(0) # Sort the table based on the first column (0th column)
        self.table.blockSignals(False) # Let singals be sent again
