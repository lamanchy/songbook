import os

from scripts.settings import SONGS_DIR


class Song(object):
    extension = ".txt"
    separator = " - "

    def __init__(self, file_name: str):
        self.__file_name = None
        self.file_name = file_name

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        if not value.endswith(self.extension):
            raise ValueError(f"{value} does not end with extension {self.extension}")

        name = self.remove_extension(value)
        if name.count(self.separator) != 1:
            raise ValueError(f"{value} contains {name.count(self.separator)} separators, there should be only"
                             f"one '{self.separator}'")

        title, author = name.split(self.separator)

        if len(title) == 0: raise ValueError(f"title of {value} is empty")
        if len(author) == 0: raise ValueError(f"author of {value} is empty")

        if self.__file_name is None:
            self.__file_name = value

        title = title.strip()
        author = author.strip()
        title = title[0].upper() + title[1:]
        author = author[0].upper() + author[1:]

        new_file_name = title + self.separator + author + self.extension

        if self.__file_name != new_file_name:
            os.rename(os.path.join(SONGS_DIR, self.__file_name), os.path.join(SONGS_DIR, new_file_name))
            self.__file_name = new_file_name

    def set_file_name(self, title, author):
        self.file_name = title + self.separator + author + self.extension

    @property
    def title(self):
        return self.file_name[:-len(self.extension)].split(self.separator)[0]

    @title.setter
    def title(self, value):
        self.file_name = value + self.separator + self.author + self.extension

    @property
    def author(self):
        return self.file_name[:-len(self.extension)].split(self.separator)[1]

    @author.setter
    def author(self, value):
        self.file_name = self.title + self.separator + value + self.extension

    @property
    def path(self):
        return os.path.join(SONGS_DIR, self.file_name)

    def load(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"{self.path} is not valid song name, it does not exists")

    def remove_extension(self, file_name):
        return file_name[:-len(self.extension)]
