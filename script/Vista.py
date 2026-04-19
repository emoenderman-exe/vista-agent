from pathlib import Path
import os
from pprint import pprint

import structure


class Vista:
    def __init__(self, work_dir: str) -> None:
        self.work_dir = Path(work_dir)
        self.structure = structure.get_structure(self.work_dir)
        self.storage = dict()
        print(f'Welcome to Vista. Your current working directory is {self.work_dir.resolve()}.')

    def run(self) -> None:
        #The main method
        while True:
            cmd = input('>>> ')
            if cmd == 'quit':
                print('[Info] Quitting Vista...')
                break
            self.process(cmd)
        return

    def process(self, cmd: str) -> None:

        #Processing ls
        if cmd == 'ls':
            self.ls()
            return

        #Processing chdir
        if cmd.startswith(('cd ', 'chdir ')):
            args = cmd.split(' ')
            if len(args) != 2:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.chdir(args[1])
            print('[Info] The working directory is updated to\n'
                  f'  -{self.work_dir.resolve()}')
            return

        #Processing mkdir
        if cmd.startswith(('md ', 'mkdir ')):
            args = cmd.split(' ')
            if len(args) != 2:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.mkdir(args[1])
            return

        #Processing rmdir
        if cmd.startswith(('rm ', 'rd ', 'rmdir ')):
            args = cmd.split(' ')
            if len(args) != 2:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.rmdir(args[1])
            return

        #Processing makefile
        if cmd.startswith(('mkf ', 'mkfile ', 'makefile ')):
            args = cmd.split(' ')
            if len(args) != 2:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.makefile(args[1])
            return

        #Processing outfile
        if cmd.startswith(('of ', 'outfile ', 'w ', 'write ')):
            args = cmd.split(' ')
            if len(args) < 4:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
                return
            self.outfile(True if args[1] == 'a' or args[1] == 'append' else False,
                         args[2],
                         ' '.join(args[3:]))
            return

        #Processing infile
        if cmd.startswith(('if ', 'infile ', 'r ', 'read ')):
            args = cmd.split(' ')
            if len(args) == 3:
                self.storage[args[1]] = self.infile(args[2])
            elif len(args) == 5:
                self.storage[args[1]] = self.infile(args[2], int(args[3]), int(args[4]))
            else:
                print(f'[Error] The command "{cmd}" is not used properly.\n'
                      '[Command Request Denied]')
            return

        #Processing exec
        if cmd.startswith(('exec ', 'python ', 'pycommand ')):
            args = cmd.split(' ')
            if len(args) >=2:
                vista: Vista = self
                exec(' '.join(args[1:]))
            return

        #Error
        print(f'[Error] The Command "{cmd}" is not valid.\n'
              '[Command Request Denied]')
        return

    def ls(self) -> None:
        pprint(self.structure, sort_dicts=False)
        return

    def chdir(self, new_path: str) -> None:
        self.work_dir = self.work_dir / new_path
        os.chdir(self.work_dir.resolve())
        self.structure = structure.get_structure(self.work_dir)
        return

    def mkdir(self, folder: str) -> None:
        (self.work_dir / folder).mkdir(parents=True, exist_ok=True)
        return

    def rmdir(self, folder: str) -> None:
        if input(f'[Warning] Remove {folder}? y/[n]:').lower() != 'y':
            return

        def rmdir_worker_fn(path: Path) -> None:
            if not path.is_dir():
                path.unlink()
                return
            for item in path.iterdir():
                if item.is_dir():
                    rmdir_worker_fn(item)
                else:
                    item.unlink()
            path.rmdir()
            return
        rmdir_worker_fn(self.work_dir / folder)
        return

    def makefile(self, path: str) -> None:
        Path(self.work_dir / path).touch()
        return

    def outfile(self, append: bool, path: str, content: str) -> None:
        if not append:
            Path(self.work_dir / path).write_text(content, encoding='utf-8')
            return
        with Path(self.work_dir / path).open('a', encoding='utf-8') as f:
            f.write(content)
        return

    def infile(self, file: str, start: int=0, end: int=-1) -> list[str]:
        with Path(self.work_dir / file).open('r', encoding='utf-8') as f:
            return f.readlines()[start:end]
