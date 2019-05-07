import os

from scripts.settings import SONGS_DIR
from scripts.song import Song


def validate_songs():
    for song_name in os.listdir(SONGS_DIR):
        Song(song_name)


if __name__ == "__main__":
    validate_songs()
