from reader import BeatmapParser
from beatmap import Beatmap
import os 

if __name__ == "__main__":
    reader = BeatmapParser()

    songs_path = "./songs"
    osu_songs = os.listdir(songs_path)
    
    all_beatmaps = {}
    for song in osu_songs:
        path = os.path.join(songs_path, song)
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith(".osu"):
                    song_path = os.path.join(path, file)
                    if song not in all_beatmaps:
                        all_beatmaps[song] = []
                    all_beatmaps[song].append(Beatmap(reader.parse(song_path))) 

    print(all_beatmaps)
