import json
import os

DATA_FILE = 'data.json'

def save(data):
    """Guarda los datos en formato JSON, crea el archivo si no existe."""
    if not isinstance(data, dict):
        data = dict(item.split(':') for item in data.split(','))
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r+') as f:
            current_data = json.load(f)
            current_data.update(data)
            f.seek(0)
            json.dump(current_data, f, indent=4)
    else:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def get(key=None):
    """Obtiene un valor específico o todos los datos si no se proporciona la clave."""
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        return data.get(key) if key else data

def remove(key=None):
    """Elimina un valor específico o todos los datos si no se proporciona la clave."""
    if not os.path.exists(DATA_FILE):
        return
    if key:
        with open(DATA_FILE, 'r+') as f:
            data = json.load(f)
            if key in data:
                del data[key]
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
    else:
        os.remove(DATA_FILE)