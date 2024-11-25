from layout_parser.table_parser.FormTableParser import FormTableParser
from layout_parser.table_parser.MatrixTableParser import MatrixTableParser
from layout_parser.table_parser.OrthodoxTableParser import OrthodoxTableParser


class TableParser:
    def parse(self, semantic_table, parsing_labels: dict)->dict|list:
        match semantic_table.type:
            case "form":
                form_table_parser = FormTableParser()
                return form_table_parser.parse(semantic_table, parsing_labels)
            case "matrix":
                matrix_table_parser = MatrixTableParser()
                return matrix_table_parser.parse(semantic_table, parsing_labels)
            case "orthodox":
                orthodox_table_parser = OrthodoxTableParser()
                return orthodox_table_parser.parse(semantic_table, parsing_labels)