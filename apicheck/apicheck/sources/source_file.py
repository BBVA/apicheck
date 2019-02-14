def file_source(path: str) -> str:
    if not path:
        raise ValueError('path is requiered')
    with open(path, 'r') as f:
        content = f.read()
    return content
