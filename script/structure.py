import pathlib

def get_structure(folder: pathlib.Path) -> dict:
    if not folder.is_dir():
        return {'name': folder.name, 'type': folder.suffix}
    return {'name': folder.name,
            'type': 'folder',
            'children': [get_structure(item) for item in folder.iterdir()]}
