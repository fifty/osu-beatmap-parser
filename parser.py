import json
from typing import Tuple
import objects
import re

_SECTION_TYPES = [
    'General', 
    'Editor', 
    'Metadata', 
    'Difficulty', 
    'Events', 
    'TimingPoints', 
    'Colours', 
    'HitObjects'
]
_SLIDER_TYPES = ['C','L','P','B']

class BeatmapParser():
    def __init__(self):
        self.beatmap = {}

    def __parse_line(self, line: str, sector: str):
        if sector == "TimingPoints":
            if "," in line:
                item = line.split(',')
                point = {
                    'time': item[0],
                    'beat_length': item[1],
                    'meter': item[2],
                    'sample_set': item[3],
                    'sample_index': item[4],
                    'volume': item[5],
                    'uninherited': item[6],
                    'effects': item[7]
                }
                if sector not in self.beatmap:
                    self.beatmap[sector] = []
                self.beatmap[sector].append(point)
        elif sector == "HitObjects":
            if "," in line:
                item = line.split(',')
                point = {
                    'x': item[0],
                    'y': item[1],
                    'time': item[2],
                    'type': item[3],
                    'hitsound': item[4]
                }
                if item[5]: 
                    if not any(curve_type in item[5] for curve_type in _SLIDER_TYPES):
                        point['extras'] = item[5]
                    else:
                        try:
                            ct_cp = item[5].split("|")
                            point['curve_type'] = ct_cp[0]
                            point['curve_points'] = tuple([{'x': params.split(':')[0], 'y': params.split(':')[1]} for params in ct_cp[1:]])
                            point['slides'] = item[6]
                            point['length'] = item[7]
                            point['edge_sounds'] = item[8]
                            point['edge_sets'] = item[9]
                        except:
                            pass
                if sector not in self.beatmap:
                    self.beatmap[sector] = []
                self.beatmap[sector].append(point)
        else:
            if ":" in line:
                item = line.split(":")
                if sector not in self.beatmap:
                    self.beatmap[sector] = {}
                value = item[1].replace('\n', '')
                key = "_".join(re.sub(r"([A-Z])", r" \1", item[0]).lower().split())
                self.beatmap[sector][key] = value


    def __check_for_header(self, line: str) -> str:
        for section in _SECTION_TYPES:
            if section in line:
                return section
        return None

    def parse(self, osu_beatmap_path: str):
        file = open(osu_beatmap_path, 'r+', encoding="utf8").readlines()
        current_sector = None
        for line in file:
            if line == '' or line=='\n':
                continue
            callback = self.__check_for_header(line)
            if callback is not None:
                current_sector = callback
            if current_sector is not None:
                self.__parse_line(line, current_sector)
                
    def dump(self):
        output = json.dumps(self.beatmap).replace('\n','')
        with open(self.beatmap['Metadata']['title'].rstrip() + '.json', 'w') as file:
            file.write(output)
        print(self.beatmap['Metadata']['title'].rstrip()+'.json written successfully')