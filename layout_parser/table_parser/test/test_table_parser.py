import json
from configparser import ConfigParser
from layout_parser.table_merger.TableMerger import TableMerger
from layout_parser.table_parser.TableParser import TableParser

table_merger = TableMerger()
table_parser = TableParser()

with open('llp_8_table_cells.json','r') as file:
    visual_cells = json.load(file)

with open('../../configs/llp_8/parsing.json', 'r') as file:
    parsing_labels = json.load(file)

merge_config_parser = ConfigParser()
merge_config_parser.read('../../configs/llp_8/table_merge.ini')

merge_config = dict(map(lambda section:(section, dict(merge_config_parser.items(section))), merge_config_parser.sections()))

semantic_table_cells = table_merger.merge('LLPFORMNO.8', visual_cells, merge_config)
for table_name, table_details in semantic_table_cells.items():
    target_table_parsing_labels = dict(
        (table_name, table)
        for table in filter(lambda table: table_name.startswith(table['name']), parsing_labels)
    )
    table_data = table_parser.parse(table_details, target_table_parsing_labels[table_name])
    print(table_data)