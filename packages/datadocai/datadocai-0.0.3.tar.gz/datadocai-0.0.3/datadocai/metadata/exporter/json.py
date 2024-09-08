import re
import os
import json
from datadocai.models import CurrentTable
from datadocai.metadata.exporter.base import MetadataExporterBase
from datadocai.models import DocumentationTable


class MetadataJsonExporter(MetadataExporterBase):
    def __init__(self, current_table: CurrentTable,
                 base_output_dir: str = 'outputs'):
        super().__init__(current_table)
        self.base_output_dir = base_output_dir
        self.output_dir = os.path.join(base_output_dir,
                                       self.current_table.trino_catalog,
                                       self.current_table.trino_schema)

    def prepare(self):
        try:
            os.makedirs(self.output_dir)
        except Exception as e:
            print(e)

    def process(self, json_data: DocumentationTable):
        result = json_data.model_dump_json()

        #
        # Save the output
        #
        file_name = f"{self.current_table.trino_table}" + ".json"

        with open(os.path.join(self.output_dir, file_name), 'w') as file:
            file.write(result)

        return result
