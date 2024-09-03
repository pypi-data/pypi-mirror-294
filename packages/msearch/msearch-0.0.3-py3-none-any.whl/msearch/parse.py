import functools
import pathlib
from typing import Dict


def extract_non_kw_args(arg_string: str):
    args_non_kw = []
    remaining_args = arg_string

    while True:
        prelude = remaining_args.split("=", 1)[0].split(" ")
        if len(prelude) == 2:
            arg_prelude = prelude[0]
            remaining_args = remaining_args[len(arg_prelude):].lstrip()
        else:
            arg_prelude = None

        if arg_prelude:
            args_non_kw.append(arg_prelude)
        else:
            break
    return args_non_kw, remaining_args



def mparse(arg_string, file_contents=None):
    """Parse a string into a dictionary of key-value pairs.

    Supports various input formats, including JSON, ROS2-style, key-value pairs, command line, and YAML.

    Can be used as a function or as a decorator.

    Example usage as a function:
    ```python
    result = mparse("key1:=value1 key2:=value2")
    ```

    Example usage as a decorator:
    ```python
    @mparse
    def my_function(**kwargs):
        print(kwargs)

    my_function("key1:=value1 key2:=value2")
    ```
    """
    if callable(arg_string):
        # Being used as a decorator
        @functools.wraps(arg_string)
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], str):
                parsed_args = mparse(args[0])
                return arg_string(**{**kwargs, **parsed_args})
            return arg_string(*args, **kwargs)
        return wrapper
    # Check if arg_string is a file path
    path = pathlib.Path(arg_string)
    if path.is_file():
        file_contents = path.read_text()
        arg_string = path.name
    args_non_kw, arg_string = extract_non_kw_args(arg_string)

    # Being used as a regular function
    if isinstance(arg_string, str) and arg_string.startswith('{') and arg_string.endswith('}'):  # JSON
        import json
        return json.loads(arg_string)
    elif ':=' in arg_string:  # ROS2-style
        args_list = arg_string.split()
        pairs = {}
        for arg in args_list:
            key, value = arg.split(':=')
            pairs[key.rstrip(':')] = value
        return args_non_kw, pairs
    elif  '=' in arg_string:  # Key-value pairs
        args_list = arg_string.split()
        pairs = {}
        for arg in args_list:
            key, value = arg.split('=')
            pairs[key] = value
        return args_non_kw, pairs
    elif arg_string.startswith('--') and ' ' in arg_string:  # Command line
        args_list = arg_string.split()
        pairs = {}
        for i in range(0, len(args_list), 2):
            key = args_list[i].lstrip('-')
            value = args_list[i+1]
            pairs[key] = value
        return args_non_kw, pairs
    elif file_contents is not None:  # File
        if arg_string.endswith('.json'):
            import json
            return json.loads(file_contents)
        elif arg_string.endswith('.yaml'):
            import yaml
            return yaml.safe_load(file_contents)
        elif arg_string.endswith('.ros'):
            args_list = file_contents.split()
            pairs = {}
            for arg in args_list:
                key, value = arg.split(':=')
                pairs[key.rstrip(':')] = value
            return args_non_kw, pairs
        else:
            raise ValueError('Unsupported file format')
    elif ':' in arg_string:  # YAML string
        import yaml
        try:
            return yaml.safe_load(arg_string)
        except yaml.YAMLError:
            raise ValueError('Unsupported input format')
    else:
        return args_non_kw, {}