import os

_path = os.path.join(os.path.dirname(__file__), 'locations.txt')
with open(_path, 'r') as _f:
    _cities = [x.strip() for x in _f.readlines()]

def get_cities() -> list[str]:
    return _cities