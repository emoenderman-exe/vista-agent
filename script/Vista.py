import pathlib
import os

import structure

class Vista:
    def __init__(self, work_dir: pathlib.Path) -> None:
        self.work_dir = work_dir
        self.structure = structure.get_structure(self.work_dir)
        print(f'Welcome to Vista. Your current work directory is {self.work_dir.resolve()}.')

    def run(self) -> None:
        while True:
            cmd = input('>>> ')
            if cmd == 'quit':
                break
            print(cmd)

    def chdir(self, new_path: str) -> None:
        os.chdir(new_path)
        self.work_dir = pathlib.Path.cwd()
        self.structure = structure.get_structure(self.work_dir)
