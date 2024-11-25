class FormTableParser:
    def parse(self, table, parsing_labels:dict) ->dict:
        cells = table.cells
        table_data = {}

        for label_details in parsing_labels['targets']:
            answer = None

            header_cell_id = [
                cell['cell_ids']
                for cell in cells
                if label_details['header'] in cell['text']
            ]

            begin_label_index = self._get_index(cells, label_details['begin_label'])
            end_label_index = (
                self._get_index(cells, label_details['end_label'])
                if 'end_label' in label_details else len(cells)
            )

            # Filter and extract data between begin and end indices
            if begin_label_index is not None and end_label_index is not None:
                target_cells = cells[begin_label_index + 1:end_label_index]
                answer = [
                    cell['text']
                    for cell in target_cells
                    if header_cell_id and header_cell_id[0][1] == cell['cell_ids'][1]
                ]

            # Store the result in table_data
            table_data[label_details['question']] = answer[0] if answer else None

        return table_data

    def _get_index(self, cells: dict, label:str) -> int|None:
        data = [index for index, cell in enumerate(cells) if label in cell['text']]
        return data[0] if data else None