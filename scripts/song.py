import os

import czech_sort

from scripts.settings import BASE_DIR
from scripts.song_text import SongText


class Song(object):
    extension = ".txt"
    separator = " - "
    SONGS_DIR = os.path.join(BASE_DIR, "songs")

    def __init__(self, file_name: str, categories):
        self.categories = categories
        self.file_name = file_name
        self.text = SongText(self.path)

    @classmethod
    def load_songs(cls):
        songs = []
        for root, dirs, files in os.walk(cls.SONGS_DIR):
            categories = root[len(cls.SONGS_DIR) + 1:].split(os.sep)
            for name in files:
                assert categories[0] != ""
                songs.append(Song(os.path.join(root, name), categories))
        return sorted(songs, key=lambda song: song.get_sort_key())

    @classmethod
    def load_song(cls, name):
        songs = [song for song in cls.load_songs() if song.title.startswith(name)]
        if len(songs) == 0:
            raise RuntimeError("Unknown song")
        if len(songs) > 1:
            raise RuntimeError("There are multiple songs with this name")

        return songs[0]

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

        self.validate_file_name()

        self.validate_name(self.title, "title")
        if self.author:
            self.validate_name(self.author, "author")

    def validate_file_name(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"{self.path} is not valid song name, file does not exists")

        if not self.file_name.endswith(self.extension):
            raise ValueError(f"{self.file_name} does not end with extension {self.extension}")

        # name = self.remove_extension()
        # if name.count(self.separator) != 1:
        #     raise ValueError(f"{self.file_name} contains {name.count(self.separator)} separators, "
        #                      f"there should be only one '{self.separator}'")

    def set_file_name(self, title, author):
        self.file_name = title + self.separator + author + self.extension

    @property
    def title(self):
        return self.parse_title_and_author()[0]

    @title.setter
    def title(self, value):
        self.set_file_name(value, self.author)

    @property
    def author(self):
        return self.parse_title_and_author()[1]

    @author.setter
    def author(self, value):
        self.set_file_name(self.title, value)

    @property
    def path(self):
        return os.path.join(self.SONGS_DIR, self.file_name)

    def parse_title_and_author(self):
        name = self.remove_extension()
        if self.separator not in name:
            return [name, '']
        return name.split(self.separator)

    def remove_extension(self):
        return os.path.basename(self.file_name)[:-len(self.extension)]

    def validate_name(self, name, its_name):
        if len(name) == 0:
            raise ValueError(f"{its_name} of {self.file_name} is empty")
        if name != name.strip():
            raise ValueError(f"there cannot be any spaces around {its_name} '{name}' in {self.file_name}")
        if not name[0].isupper() and not name[0].isdigit():
            raise ValueError(f"first letter of {its_name} {name} must be uppercase or digit")
        if "  " in name:
            raise ValueError(f"{its_name} {name} cannot contain two spaces next to each other")

    def transpose(self, steps=1):
        self.text.transpose(steps)
        self.text.save()

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def get_sort_key(self):
        return [czech_sort.key(c) for c in self.categories] + [czech_sort.key(self.title)]
