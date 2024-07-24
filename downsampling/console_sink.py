
from prettytable.colortable import ColorTable, Themes
from datetime import datetime
from quixstreams.sinks import Sink
from quixstreams.sinks.base import SinkBatch

class ConsoleSink(Sink):
    def __init__(self, 
                table_width :int = 150,
                max_column_width: int = 20, 
                rows_visible: int = 5, 
                max_columns :int = 5,
                metadata: bool = False) -> None:
        self._rows_visible = rows_visible
        self._table_width = table_width
        self._max_columns = max_columns
        self._max_column_width = max_column_width
        self._metadata = metadata
        self._rows = []
        self._columns = []

        super().__init__()


    def write(self, batch: SinkBatch):

        for row in batch:
            
            value = row.value

            if self._metadata:
                value = {
                    "[time]": str(datetime.fromtimestamp(row.timestamp / 1000)),
                    "[key]": row.key,
                    **row.value
                }
            
            self._rows.append(value)

            # Update current columns
            for column in value.keys():
                if column not in self._columns:
                    self._columns.append(column)
        
        # Create a new PrettyTable with updated columns
        #table = PrettyTable(current_columns)

        current_columns = self._columns
        if len(current_columns) > self._max_columns:
            current_columns = list(current_columns)[:self._max_columns]
            current_columns.append("...")

        table = ColorTable(current_columns, theme=Themes.OCEAN)

        # Set max width for each column
        for col in current_columns:
            table.max_width[col] = self._max_column_width

        table.max_table_width = self._table_width

        if len(self._rows) > self._rows_visible:
            placeholder = []
            for _ in current_columns:
                placeholder.append("...")
            table.add_row(placeholder)

        # Add row to the table
        for row in self._rows[-self._rows_visible:]:
            row_cells = []
            for column in current_columns:
                if column == "...":
                    row_cells.append("...")
                elif column in row:
                    cell_content = str(row[column])
                    if len(cell_content) > self._max_column_width:
                        cell_content = cell_content[:self._max_column_width - 3] + "..."

                    row_cells.append(cell_content)
                else:
                    row_cells.append(" ")

            table.add_row(row_cells)

        if len(self._rows) > self._rows_visible:
            self._rows = self._rows[-self._rows_visible:]
        
        # Clear the console
        print("\033c", end="")
        # Print the updated table
        print(table)
        
        