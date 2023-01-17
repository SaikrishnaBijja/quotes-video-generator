import json

def is_exist(check, filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    try:
        if data[f'{check}']:
            return False
        else:
            return True
    except KeyError:
        return True

def to_enter(value, filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    y = {f"{value}":1}
    data.update(y)
    with open(filepath, "w") as outfile:
        json.dump(data, outfile)
