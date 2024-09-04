import os
import pickle
import shutil
from itertools import count


class Path:
    def __init__(self, path=None, path2=None, make=False):
        if path is None:
            path = os.getcwd()
        if path is not None and isinstance(path, str):
            if path2 is not None:
                if isinstance(path2, Path):
                    path2 = path2.path
                path = os.path.join(path2, path)
        if path is not None and isinstance(path, Path):
            path = path.path
        self.path = os.path.abspath(path)
        if make and not self:
            self.make()

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def before(self):
        return Path(os.path.dirname(self.path))

    def __eq__(self, other):
        return isinstance(other, Path) and self.path == other.path

    def __bool__(self):
        return self.exists()

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"Path(path={self.path})"

    def make(self, with_errors=False):
        try:
            os.mkdir(self.path)
        except IOError as e:
            print(e, type(e))
            if with_errors:
                raise e

    def make_new_folder(self):
        for ind in count(1):
            if ind == 1:
                name = f'New Folder'
            else:
                name = f'New Folder ({ind})'
            p2 = Path(name, self)
            if not p2:
                p2.make()
                return p2

    def recent(self, ext=None):
        if ext is None:
            return max(self.listdir(ext=ext), key=File.date_modified)

    def __iter__(self):
        return iter(self.listdir())

    def size(self):
        size_ = 0
        for file in self.walk():
            size_ += file.size()
        return round(size_, 2)

    def size_bytes(self):
        size_ = 0
        for file in self.walk():
            size_ += file.size_bytes()
        return size_

    def walk(self):
        for r, _, fi in os.walk(self.path):
            for file in fi:
                yield File(file, r)

    def walk_folders(self):
        for r, fo, _ in os.walk(self.path):
            for folder in fo:
                yield Path(os.path.join(r, folder))

    def rmtree(self):
        shutil.rmtree(self.path)

    def rmdir(self):
        os.rmdir(self.path)

    def date_created(self):
        return os.stat(self.path).st_ctime

    def date_modified(self):
        return os.stat(self.path).st_mtime

    def date_accesed(self):
        return os.stat(self.path).st_atime

    def __fspath__(self):
        return self.path

    def rename(self, name):
        new_path = os.path.join(self.before, name)
        os.rename(self.path, new_path)
        return Path(new_path)

    def remove_empty_folders(self):
        x_all = False
        while True:
            x_ture = False
            for r, fo, fi in os.walk(self.path):
                if not fo and not fi:
                    try:
                        Path(r).rmdir()
                    except PermissionError:
                        continue
                    x_ture = True
                    x_all = True
            if not x_ture:
                break
        return x_all

    def exists(self):
        return os.path.exists(self.path)

    def listdir(self, ext=None):
        for item in os.listdir(self.path):
            if ext is not None and isinstance(ext, str):
                ext = [ext]
            if ext is not None and isinstance(ext, list):
                x_true = False
                for e in ext:
                    if item.lower().endswith(e.lower()):
                        x_true = True
                        break
                if not x_true:
                    continue
            yield File(item, self.path)

    def listdir_folders(self):
        for item in self:
            if not item.is_file():
                yield Path(item.file)

    def listdir_list(self, ext=None):
        try:
            return list(self.listdir(ext=ext))
        except PermissionError:
            return []

    def walk_list(self):
        return list(self.walk())

    def file(self, filename):
        return File(filename, self.path)

    def free_size(self):
        return shutil.disk_usage(self.path).free

    def mkdir(self, name):
        new_path = Path(name, self)
        os.mkdir(new_path)
        return new_path

    def move(self, path: 'Path'):
        shutil.move(self, path.path)
        return Path(self.name, path)


class File:

    def __init__(self, filename=None, path=None, whole_path=None):
        if isinstance(filename, File):
            whole_path = filename.file
        if whole_path is not None:
            path, filename = self.split(whole_path)
        self.path = Path(path)
        self.file = os.path.join(self.path, filename)

    @property
    def dir(self) -> str:
        return os.path.split(self.file)[0]

    @property
    def filename(self) -> str:
        return os.path.split(self.file)[1]

    @property
    def name(self) -> str:
        return os.path.splitext(self.filename)[0]

    @property
    def ext(self) -> str:
        return os.path.splitext(self.filename)[1]

    def __fspath__(self):
        return self.file

    def open(self, mode='r', encoding=None):
        return open(self, mode=mode, encoding=encoding)

    def write(self, text):
        with self.open('w', encoding='utf-8') as f:
            f.write(text)

    @property
    def text(self, encoding=None) -> str:
        with self.open(encoding='utf-8' if encoding is None else encoding) as f:
            text = f.read()
        return text

    @property
    def name_lower(self) -> str:
        return self.name.lower()

    def is_file(self):
        return os.path.isfile(self.file)

    def is_pickle(self):
        return self.is_file() and self.ext == '.pkl'

    def exists(self):
        return os.path.exists(self.file)

    def __repr__(self):
        return f"File(file='{self.filename}',path='{self.path}')"

    def __str__(self):
        return self.file

    def rename(self, new_name, hyp=False):
        if isinstance(new_name, File):
            new_name = new_name.name
        if isinstance(new_name, str) and not new_name.endswith(self.ext):
            new_name += self.ext
        file = File(new_name, self.path)
        if not hyp:
            os.rename(self.file, file.file)
        return file

    def add_start(self, name, hyp=False):
        return self.rename(f"{name}{self.name}", hyp=hyp)

    def move(self, new_path):
        new_path = Path(new_path)
        if not new_path.exists():
            raise IOError
        if new_path == self.path:
            return self
        shutil.move(self.file, new_path)
        return File(self.filename, new_path)

    def copy(self, new_path):
        new_path = Path(new_path)
        if not new_path.exists():
            raise IOError
        if new_path == self.path:
            return self
        shutil.copy(self.file, new_path)
        return File(self.filename, new_path)

    def remove(self):
        os.remove(self.file)

    def size(self):
        try:
            return round(os.stat(self.file).st_size / pow(2, 20), 2)
        except FileNotFoundError:
            return 0

    def size_bytes(self):
        try:
            return os.stat(self.file).st_size
        except FileNotFoundError:
            return 0

    def date_created(self):
        return os.stat(self.file).st_ctime

    def date_accessed(self):
        return os.stat(self).st_atime

    def date_modified(self):
        return os.stat(self.file).st_mtime

    def __eq__(self, other):
        if isinstance(other, str):
            return self.file == other
        if isinstance(other, File):
            return self.file == other.file
        return NotImplemented

    def __bool__(self):
        return self.exists()

    def __hash__(self):
        return hash(self.file)

    def is_video(self):
        return self.ext[1:] in {'mkv', 'mp4', 'avi', 'm4v', 'mov', 'ts', 'webm'}


class Pickle(File):
    def __init__(self, filename=None, path=None, should_exist=False, whole_path=None):
        if isinstance(filename, File):
            File.__init__(self, whole_path=filename.file)
            return
        if filename is not None and not filename.endswith('.pkl'):
            filename = filename + '.pkl'
        File.__init__(self, filename=filename, path=path, whole_path=whole_path)

    def read(self):
        with self.open('rb') as f:
            return pickle.load(f)

    def write(self, obj):
        with self.open('wb') as f:
            pickle.dump(obj, f)
