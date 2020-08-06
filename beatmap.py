from objects import General, MetaData, Editor, Difficulty, HitCircle, TimingPoint, HitObject, TimingObject, SliderCircle
from typing import Union

class Beatmap():
    def __init__(self, beatmap: dict):
        self.general_settings = General(**beatmap['General'])
        self.editor_settings = Editor(**beatmap['Editor'])
        self.meta_data = MetaData(**beatmap['Metadata'])
        self.difficult_settings = Difficulty(**beatmap['Difficulty'])
        self.hit_objects = list(map(hitCircleType, beatmap['HitObjects']))
        self.timing_objects = [TimingPoint(**tp) for tp in beatmap['TimingPoints']]

def hitCircleType(obj) -> Union[SliderCircle, HitCircle]:
    if 'curve_type' in obj:
        return SliderCircle(**obj)
    else:
        return HitCircle(**obj)