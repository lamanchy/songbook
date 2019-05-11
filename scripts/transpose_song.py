import sys

from scripts.song import Song

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise RuntimeError("You have to specify file name (starting with is enough)")
    Song.transpose(Song.load_song(sys.argv[1]))
