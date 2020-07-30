This document is used to copy and paste certain chunks of text for the workshop. Thus making the workshop faster so users don't need to manually type all this information. Please only use these when called for during the presentation, otherwise they may cause confusion.

These may not be in order of when they will need to be used.

## Commands

1) Create virtual enivronment (first command is to double check the python version):
    - Windows:
        ```Powershell
        python -V
        python -m venv .venv
        ```
    - Mac OS:
        ```bash
        python3 -V
        python3 -m venv .venv
        ```

2) Activate virtual environment:
    - Windows:
        ```Powershell
        .\.venv\Scripts\activate
        ```
    - Mac OS:
        ```bash
        source ./.venv/bin/activate
        ```

3) Do the pip install:
    ```bash
    pip install -r requirements-dev.txt
    ```

4) Generate resource file:
    ```bash
    pyside2-rcc resources.qrc -o resources.py
    ```

5) Running the UI locally:
```bash
pyside2-rcc resources.qrc -o resources.py; python app.py
```

6) Create executable:
    ```bash
    PyInstaller --hidden-import PySide2.QtXml --hidden-import pkg_resources.py2_warn --name="Python105App" app.py --onefile
    ```


## Code Blocks

1) Import custom widgets
    ```python
    from custom_widgets import MplWidget, MTableWidget
    ```

2) Registering our custom widgets:
    ```python
    loader.registerCustomWidget(MplWidget)
    loader.registerCustomWidget(MTableWidget)
    ```

3) Other connections:
    ```python
    self.ui.btn_save.clicked.connect(self.slot_btn_save_clicked)
    self.ui.btn_reset_fields.clicked.connect(self.slot_btn_reset_fields)
    self.ui.table_widget.cellChanged.connect(self.slot_table_widget_changed)
    self.ui.table_widget.rowRemoved.connect(self.slot_row_removed)
    ```

4) Using our table controller:
    ```python
    self.table = TemperatureTable(self.ui.table_widget, 3)
    ```
5) Making the table headers visible:
    ```python
    self.ui.table_widget.horizontalHeader().setVisible(True) # Make sure table headers are visible
    ```

6) Initialize fields:
    ```python
    self.slot_btn_reset_fields()
    ```

7) Initializing plot stuff
    ```python
    self.ui.mpl_widget_1.canvas.axes.set_xlabel("Timestamp")
    self.ui.mpl_widget_1.canvas.axes.set_ylabel("Temperature (°C)")
    date_format = mdates.DateFormatter("%Y-%m-%dT%H:%M:%S")
    self.ui.mpl_widget_1.canvas.axes.xaxis.set_major_formatter(date_format)
    self.ui.mpl_widget_1.canvas.axes.tick_params(axis='x', labelrotation=60)
    self.update_plot()
    ```

8) Save button slot:
    ```python
    def slot_btn_save_clicked(self):
        """
        Slot for save button:
            Valid data in fields, then save data to table and plot.
        """

        date_time = self.ui.date_time_taken.dateTime().toPython()
        # If we wanted to convert the time to UTC we can use the code commented out below.
        # timestamp = time.mktime(date_time.timetuple())
        # utc_date_time = datetime.utcfromtimestamp(timestamp)

        temp_reading = self.ui.temperature_spin_box.value()

        notes = self.ui.test_edit_notes.toPlainText()

        self.table.insert_row(date_time, temp_reading, notes)

        self.update_plot()

        # If we wanted to, when saving an item to a table we could  use `scollToItem` and
        # `setCurrent` to select that item in the table, but for now we won't do that.
    ```

9) Reset Fields button slot:
    ```python
    def slot_btn_reset_fields(self):
        """
        Slot for reset fields button:
            Clear the entry fields back to their default values.
        """
        cur_datetime = datetime.now()
        cur_date = QDate(cur_datetime.year, cur_datetime.month, cur_datetime.day)
        cur_time = QTime(cur_datetime.hour, cur_datetime.minute, cur_datetime.second)

        self.ui.date_time_taken.setDate(cur_date)
        self.ui.date_time_taken.setTime(cur_time)
        self.ui.test_edit_notes.clear()
        self.ui.temperature_spin_box.setValue(0)
    ```

10) Data in table changed slot:
    ```python
    def slot_table_widget_changed(self, row: int, column: int) -> None:
        """
        Called when a cell in the table is changed.
        
        Arguments:
            row (int): The index of the row where the cell was changed.
            column (int): The index of the column where the cell was changed.
        """
        print(f"Table cell change - row {row} - column {column}")
        self.table.cell_updated(row, column)
        self.update_plot()
    ```

11) Row in table removed slot:
    ```python
    def slot_row_removed(self, row: int) -> None:
        """
        Called when a row in the table is removed.

        Arguments:
            row (int): The index of the row removed.
        """
        print(f"Removing row {row}")
        if row != -1:
            del self.table.rows[row]
            self.table.update()
            self.update_plot()
    ```

12) Update plot code:
    ```python
    def update_plot(self):
        """
        Update the matplotlib plot.
        """

        # First time we have no plot reference, so do a normal plot.
        # .plot returns a list of line <reference>s, as we're
        # only getting one we can take the first element.
        
        if not self.table.rows: # If we have no data then just set the ticks and return
            self.ui.mpl_widget_1.canvas.axes.set_xticks([])
            return

        # Pull out the datetimes and temperatures as the x and y data.
        xdata, ydata, *_ = zip(*self.table.rows)

        # Set the x tick marks to the timestamps.
        self.ui.mpl_widget_1.canvas.axes.set_xticks(matplotlib.dates.date2num(xdata))

        # If we of not yet created a plot, then create a date plot and save it to _plot_ref.
        if self._plot_ref is None:
            plot_ref = self.ui.mpl_widget_1.canvas.axes.plot_date(matplotlib.dates.date2num(xdata), ydata, '--')
            self._plot_ref = plot_ref[0]
        # Else, we have already created a plot so lets just update that one.
        else:
            # Update x and y data
            self._plot_ref.set_xdata(matplotlib.dates.date2num(xdata))
            self._plot_ref.set_ydata(ydata)
            # Resize the graph to match the new data.
            self.ui.mpl_widget_1.canvas.axes.relim()
            self.ui.mpl_widget_1.canvas.axes.autoscale_view()

        # So we don't truncate the x-axis labels, use a tight layout.
        self.ui.mpl_widget_1.figure.tight_layout()
        # Trigger the canvas to update and redraw.
        self.ui.mpl_widget_1.canvas.draw()
        return
    ```

13) MTableWidget keyPressEvent:
    ```python
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            row = self.currentRow()
            self.removeRow(row)
        else:
            super().keyPressEvent(event)
    ```

14) MTableWidget Signal:
    ```python
    rowRemoved = Signal(int)
    # and at the end of the if
    self.rowRemoved.emit(row) 
    ```