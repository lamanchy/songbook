import sys

from scripts.song import Song

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise RuntimeError("You have to specify file name (starting with is enough) and num of transposition")
    # for song in [Song.load_song("Stairway")]:
    # for song in Song.load_songs():
    #     song.transpose(1)
    # for i in range(12):
    #     song.transpose(1)

    Song.transpose(Song(sys.argv[1], []), int(sys.argv[2]))
