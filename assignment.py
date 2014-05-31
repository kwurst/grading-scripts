import pathlib
import json
import os


class Assignment(object):
    '''Provides traversal and path resolution for visitors over an assignment
    directory.
    '''

    def __init__(self, config_file, verbose=False):
        self._verbose = verbose
        self._config_file = pathlib.Path(config_file).resolve()
        self._config = None
        self._submission_directories = []

        self._load_config()
        self._load_submission_directories()

    def _load_config(self):
        self._config = self._read_config()
        self._config['directory'] = self._resolve(self._config['directory'], root=self._config_file.parent)
        self._config['files'] = [pathlib.Path(file_) for file_ in self._config['files']]

    def _read_config(self):
        config = None
        with self._config_file.open() as file_:
            config = json.load(file_)
        return config

    def _load_submission_directories(self):
        self._submission_directories = [
                self._resolve(d, root=self._config['directory'])
                for d in self._config['directory'].glob('*')
                if d.is_dir()
                ]

    @staticmethod
    def _resolve(path, root=None):
        path = pathlib.Path(path)
        if path.is_absolute():
            return path
        elif root is None:
            return path.resolve()
        else:
            return (pathlib.Path(root).resolve() / path).resolve()

    def accept(self, visit, cd=False):
        '''
        Calls visit(directory, files) for each submission directory.  Directory
        is a pathlib.Path that is the submission directory being visited. Files
        is a list of pathlib.Path objects that are the files within the
        directory to process.

        visit: callable

        cd: boolean - True causes accept to change into each submission directory.
        '''
        for directory in self._submission_directories:
            if self._verbose:
                print('Processing', directory)
            if cd:
                if self._verbose:
                    print('Entering')
                cwd = pathlib.Path.cwd()
                os.chdir(str(directory))
            visit(directory, self._get_resolved_files(directory))
            if cd:
                if self._verbose:
                    print('Exiting')
                os.chdir(cwd)

    def _get_resolved_files(self, root):
        return [self._resolve(f, root=root) for f in self._config['files']]
