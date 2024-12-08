import os
from string import Template


class SQLProvider:

    def __init__(self, sql_path: str) -> None:
        self._scripts = {}
        for file_name in os.listdir(sql_path):
            full_file_path = f'{sql_path}/{file_name}'
            if not full_file_path.endswith('.sql'):
                continue
            template = Template(open(full_file_path, 'r').read())
            self._scripts[file_name] = template
        
    def get_sql(self, template_name: str, params) -> str:
        if (params is None):
            return self._scripts[template_name]
        else:
            return self._scripts[template_name].substitute(**params)