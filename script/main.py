import pathlib
import argparse

import Vista

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vista Agent')
    parser.add_argument('--work-dir',
                        type=str,
                        help='provide work directory',
                        default=pathlib.Path.cwd().resolve())
    args = parser.parse_args()

    vista = Vista.Vista(args.work_dir)
    vista.run()
