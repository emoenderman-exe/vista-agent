import pathlib
import os

import structure

class Vista:
    def __init__(self, work_dir: pathlib.Path) -> None:
        self.work_dir = work_dir
        self.structure = structure.get_structure(self.work_dir)
        print(f'Welcome to Vista. Your current working directory is {self.work_dir.resolve()}.')

    def run(self) -> None:
        while True:
            cmd = input('>>> ')
            if cmd == 'quit':
                print('[Info] Quitting Vista...')
                break
            self.process(cmd)
        return

    def process(self, cmd: str) -> None:
        if cmd.startswith('cd') or cmd.startswith('chdir'):
            args = cmd.split(' ')
            if len(args) != 2:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.chdir(args[1])
            print('[Info] The working directory is updated to\n'
                  f'  -{self.work_dir.resolve()}')
            return
        print(f'[Error] The Command "{cmd}" is not valid.\n'
              '[Command Request Denied]')

    def chdir(self, new_path: str) -> None:
        os.chdir(new_path)
        self.work_dir = pathlib.Path.cwd()
        self.structure = structure.get_structure(self.work_dir)
        return
