import os

from scripts.song import Song


def validate_songs():
    Song.load_songs()


if __name__ == "__main__":
    validate_songs()
