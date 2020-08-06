from errors import CouldNotParseBeatmapException
from typing import Tuple, Union
import objects
import json
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

class BeatmapParser:
    def __parse_timing_objects(self, line: str, sector: str, beatmap_dict: dict):
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
        beatmap_dict[sector].append(point)

    def __parse_hit_objects(self, line: str, sector: str, beatmap_dict: dict):
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
        beatmap_dict[sector].append(point)

    def __parse_line(self, line: str, sector: str, beatmap_dict: dict):
        if sector == "TimingPoints":
            if sector not in beatmap_dict:
                beatmap_dict[sector] = []
            if "," not in line:
                return
            self.__parse_timing_objects(line, sector, beatmap_dict)
        elif sector == "HitObjects":
            if sector not in beatmap_dict:
                beatmap_dict[sector] = []
            if "," not in line:
                return
            self.__parse_hit_objects(line, sector, beatmap_dict)
        else:
            if sector not in beatmap_dict:
                beatmap_dict[sector] = {}
            if ":" not in line:
                return
            item = line.split(":")
            value = item[1].replace('\n', '')
            key = "_".join(re.sub(r"([A-Z])", r" \1", item[0]).lower().split())
            beatmap_dict[sector][key] = value


    def __check_for_header(self, line: str) -> Union[str, None]:
        for section in _SECTION_TYPES:
            if section in line:
                return section
        return None

    def parse(self, osu_beatmap_path: str) -> dict:
        try:
            file = open(osu_beatmap_path, 'r+', encoding="utf8").readlines()
            current_sector = None
            beatmap_dict = {}
            for line in file:
                if line == '' or line=='\n':
                    continue
                callback = self.__check_for_header(line)
                if callback is not None:
                    current_sector = callback
                if current_sector is not None:
                    self.__parse_line(line, current_sector, beatmap_dict)
            return beatmap_dict
        except:
            raise CouldNotParseBeatmapException()
                
    def dump(self, beatmap_dict: dict):
        try:
            output = json.dumps(beatmap_dict).replace('\n','')
            with open(beatmap_dict['Metadata']['title'].rstrip() + '.json', 'w') as file:
                file.write(output)
            print(beatmap_dict['Metadata']['title'].rstrip()+'.json has been successfully written.')
        except Exception as e:
            print(e)