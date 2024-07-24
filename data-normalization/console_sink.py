
from prettytable.colortable import ColorTable, Themes
from datetime import datetime

class ConsoleSink:
    def __init__(self, table_width :int = 150, max_column_width: int = 20, rows_visible: int = 5, max_columns :int = 5) -> None:
        self._rows_visible = rows_visible
        self._table_width = table_width
        self._max_columns = max_columns
        self._max_column_width = max_column_width
        self._rows = []
        self._columns = []
        
        
    def print_with_metadata(self, row: dict, key: str, timestamp: int, _):
        row_with_metadata = {
            "[time]": str(datetime.fromtimestamp(timestamp / 1000)),
            "[key]": key,
            **row
        }
        
        self.print(row_with_metadata)


    def print(self, row: dict):
        
        self._rows.append(row)
        
        # Update current columns
        for column in row.keys():
            if column not in self._columns:
                self._columns.append(column)
     
        current_columns = self._columns

        if len(current_columns) > self._max_columns:
            current_columns = list(current_columns)[:self._max_columns]
            current_columns.append("...")

        # Create a new PrettyTable with updated columns
        #table = PrettyTable(current_columns)

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
                if column is "...":
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
