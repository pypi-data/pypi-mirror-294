import subprocess
import json

class SystemInfo:
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    def get_data(self):
        try:
            # Run the osquery command for the specific table
            command = ['osqueryi', '--json', f'SELECT * FROM {self.table_name};']
            output = subprocess.run(command, capture_output=True, check=True)
            result = json.loads(output.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' failed with exit code {e.returncode}")
            print(e.stderr)
            return None
    
    def get_values_by_key(self, query_key: str):
        result = self.get_data()
        if not result:
            return "No data found"

        # Extract values for the specified key
        values = [item.get(query_key, 'Key not found') for item in result]
        return values

    def get_all_data(self):
        return self.get_data()
