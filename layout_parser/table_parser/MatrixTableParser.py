class MatrixTableParser:
    def parse(self, table, parsing_labels:dict)->dict:
        table_data = {}

        for vertical_header in parsing_labels["vertical_headers"]:
            for horizontal_header in parsing_labels["horizontal_headers"]:
                key = f"{horizontal_header['question']}_{vertical_header['question']}"
                table_data[key] = self._get_answer(vertical_header, horizontal_header, table.cells)

        if "dynamic_vertical_headers" in parsing_labels:
            for dynamic_vertical_header in parsing_labels["dynamic_vertical_headers"]:
                dynamic_answer_cell = self._get_dynamic_answer(dynamic_vertical_header, table.cells)
                table_data[dynamic_vertical_header["question"]] = (
                    dynamic_answer_cell[0]["text"] if dynamic_answer_cell else None
                )
                for horizontal_header in parsing_labels["horizontal_headers"]:
                    row_id = (
                        dynamic_answer_cell[0]["cell_ids"][0]
                        if dynamic_answer_cell else None
                    )
                    col_id = self._get_cell_id(table.cells, horizontal_header)[1]
                    key = f"{horizontal_header['question']}_{dynamic_vertical_header['question']}"
                    table_data[key] = (
                        None
                        if not row_id or not col_id
                        else self._get_target_answer(table.cells, row_id, col_id)
                    )

        return table_data

    def _get_answer(self, vertical_header:dict, horizontal_header:dict, cells:list)->int|None:
        target_row_id = self._get_cell_id(cells, vertical_header)[0]
        target_col_id = self._get_cell_id(cells, horizontal_header)[1]

        return None if not target_row_id or not target_col_id else self._get_target_answer(cells, target_row_id, target_col_id)

    def _get_dynamic_answer(self, dynamic_vertical_header:dict, cells:list)->list|None:
        previous_header_cell_id = self._get_cell_id(cells, dynamic_vertical_header["previous_header"])
        next_header_cell_id = self._get_cell_id(cells, dynamic_vertical_header["next_header"])

        return (
            None
            if (
                    not next_header_cell_id[0]
                    or not previous_header_cell_id[0]
                    or ((next_header_cell_id[0] - previous_header_cell_id[0]) != 2)
                    or not next_header_cell_id[1]
                    or not previous_header_cell_id[1]
                    or next_header_cell_id[1] != previous_header_cell_id[1]
            )
            else self._get_dynamic_target_answer(
                cells, previous_header_cell_id[0] + 1, previous_header_cell_id[1]
            )
        )

    def _get_target_answer(self, cells:list, target_row_id:int, target_col_id:int)->str|None:
        return next(
            (cell["text"] for cell in cells if cell["cell_ids"] == [target_row_id, target_col_id]),
            None
        )

    def _get_dynamic_target_answer(self, cells:list, target_row_id:int, target_col_id:int)->list:
        return [
            cell for cell in cells if cell["cell_ids"] == [target_row_id, target_col_id]
        ]

    def _get_cell_id(self, cells:list, header:dict)->list:
        target_cells = self._get_matched_cells(cells, header["header"])
        return (
            target_cells[(header.get("occurrence", 1) - 1)]["cell_ids"]
            if target_cells
            else [-1, -1]
        )

    def _get_matched_cells(self, cells:list, header:dict)->list:
        return [
            cell for cell in cells if header in cell["text"]
        ]