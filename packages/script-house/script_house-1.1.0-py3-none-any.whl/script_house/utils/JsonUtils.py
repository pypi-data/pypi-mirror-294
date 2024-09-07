import json
from os.path import isfile

from script_house.utils.FileSystemUtils import assert_is_file

try:
    from pydantic import BaseModel
    from bson import json_util
except ImportError as e:
    raise ImportError(f"Required dependencies for this utility are not installed: {e.name}. "
                      f"Please install them using `pip install pydantic==2.5.3 bson==0.5.10 pymongo==4.6.1`")

"""
The conversion flow:
str <-> built-in types <-> custom class 
            ^
            |
            v
           file
           
(1) str <-> built-in types 
    uses python's default json module
    
(2) built-in types <-> custom class 
    uses Pydantic and requires the custom class inherits pydantic.BaseModel

(3) built-in types <-> file
    uses python's default json module
"""


def write(obj, file: str, force_write: bool = False, clazz: type = None):
    if isfile(file) and not force_write:
        raise Exception(f'file already exists, but force write is not allowed.')

    if clazz is not None:
        obj = obj.model_dump()

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, default=json_util.default)


def read(file: str, clazz: type = None):
    assert_is_file(file)
    with open(file, 'r', encoding='utf-8') as f:
        obj = json.load(f, object_hook=json_util.object_hook)

    if clazz is None:
        return obj
    return clazz(**obj)


def to_str(obj, clazz: type = None):
    if clazz is not None:
        obj = obj.model_dump()
    return json.dumps(obj, ensure_ascii=False, indent=4, default=json_util.default)


def to_obj(string: str, clazz: type = None):
    # return a dict
    obj = json.loads(string, object_hook=json_util.object_hook)
    if clazz is None:
        return obj
    return clazz(**obj)


if __name__ == '__main__':
    obj = to_obj('{"a":true}')
    print(obj)
