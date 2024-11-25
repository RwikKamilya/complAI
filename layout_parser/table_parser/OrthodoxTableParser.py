class OrthodoxTableParser:
    def parse(self, table, parsing_labels:dict)->list:
        table_data = []
        cells = table.cells
        total_rows = cells[-1]['cell_ids'][0] if cells else 0
        header_row = self._get_header_row(cells, parsing_labels['headers']) or total_rows

        for row in range(header_row + 1, total_rows + 1):
            row_data = {}
            for parsing_label in parsing_labels['headers']:
                col = self._get_header_col(cells, parsing_label)
                row_data[parsing_label['question']] = (
                    self._get_answer(cells, row, col) if col is not None else None
                )
            table_data.append(row_data)

        return table_data

    def _get_header_row(self, cells:list, headers:dict)->int|None:
        header_cell_id = [
            cell["cell_ids"]
            for cell in cells
            if headers[0]["header"] in cell["text"]
        ]

        occurrence = headers[0].get("occurrence", 1)
        return None if not header_cell_id else header_cell_id[occurrence - 1][0]

    def _get_header_col(self, cells:list, headers:dict)->int|None:
        header_cell_id = [
            cell["cell_ids"]
            for cell in cells
            if headers["header"] in cell["text"]
        ]

        occurrence = headers.get("occurrence", 1)
        return None if not header_cell_id else header_cell_id[occurrence - 1][1]

    def _get_answer(self, cells:list, row:int, col:int)->str|None:
        target_answer = [
            cell["text"]
            for cell in cells
            if cell["cell_ids"] == [row, col]
        ]
        return None if not target_answer else target_answer[0]