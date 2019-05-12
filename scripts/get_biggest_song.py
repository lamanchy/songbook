from scripts.song import Song

if __name__ == "__main__":
    songs = Song.load_songs()

    widest = map(lambda song: f"{song.title} {song.text.width} {song.text.height}", sorted(
        songs,
        key=lambda song: song.text.width,
        reverse=True
    )[:10])
    print(f"Widest songs:  {list(widest)}")
    highest = map(lambda song: f"{song.title} {song.text.width} {song.text.height}", sorted(
        songs,
        key=lambda song: song.text.height,
        reverse=True
    )[:10])
    print(f"Highest songs: {list(highest)}")
