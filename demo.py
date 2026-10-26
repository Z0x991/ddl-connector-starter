import json
from pathlib import Path
from validator import validate_deadlines

if __name__ == '__main__':
    path = Path(__file__).with_name('sample.json')
    records = json.loads(path.read_text(encoding='utf-8'))
    print(json.dumps(validate_deadlines(records), indent=2))
