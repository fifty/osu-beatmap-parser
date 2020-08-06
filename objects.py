from aenum import MultiValueEnum
from enum import Enum, unique
from typing import Tuple
from abc import ABC

class GeneralSettings(ABC):
    def __init__(self,
                audio_filename: str,
                audio_lead_in: int,
                preview_time: int,
                countdown: int,
                sample_set: str,
                stack_leniency: float,
                mode: int,
                letterbox_in_breaks: int,
                widescreen_storyboard: int):
        self.audio_file_name = audio_filename
        self.audio_lead_in = int(audio_lead_in)
        self.preview_time = int(preview_time)
        self.countdown = int(countdown)
        self.sample_set = sample_set
        self.stack_leniency = float(stack_leniency)
        self.mode = int(mode)
        self.letterbox_in_breaks = int(letterbox_in_breaks)
        self.widescreen_storyboard = int(widescreen_storyboard)

class EditorSettings(ABC):
    def __init__(self,
                bookmarks: int,
                distance_spacing: float,
                beat_divisor: int,
                grid_size: int,
                timeline_zoom: float):
        self.bookmarks = int(bookmarks)
        self.distance_spacing = float(distance_spacing)
        self.beat_divisor = int(beat_divisor)
        self.grid_size = int(grid_size)
        self.timeline_zoom = float(timeline_zoom)

class MetaDetaSettings(ABC):
    def __init__(self,
                title: str,
                title_unicode: str,
                artist: str,
                artist_unicode: str,
                creator: str,
                version: str,
                source: str,
                tags: str,
                beatmap_i_d: int,
                beatmap_set_i_d: int):
        self.title = title
        self.title_unicode = title_unicode
        self.artist = artist
        self.artist_unicode = artist_unicode
        self.creator = creator
        self.version = version
        self.source = source
        self.tags = tags
        self.beatmap_id = int(beatmap_i_d)
        self.beatmap_set_id = int(beatmap_set_i_d)

class DifficultySettings(ABC):
    def __init__(self,
                h_p_drain_rate: int,
                circle_size: float,
                overall_difficulty: int,
                approach_rate: float,
                slider_multiplier: float,
                slider_tick_rate: int):
        self.hp_drain_rate = int(h_p_drain_rate)
        self.circle_size = float(circle_size)
        self.overall_difficulty = int(overall_difficulty)
        self.approach_rate = float(approach_rate)
        self.slider_multiplier = float(slider_multiplier)
        self.slider_tick_rate = int(slider_tick_rate)

class TimingObject(ABC):
    def __init__(self,
                time: int,
                beat_length: float,
                meter: int,
                sample_set: int,
                sample_index: int,
                volume: int,
                uninherited: int,
                effects: int):
        self.time = int(time)
        self.beat_length = float(beat_length)
        self.meter = int(meter)
        self.sample_set = int(sample_set)
        self.sample_index = int(sample_index)
        self.volume = int(volume)
        self.uninherited = int(uninherited)
        self.effects = int(effects)

class HitObjectType(MultiValueEnum):
    CIRCLE = 1
    SLIDER = 2
    NEW_COMBO = 3
    SPINNER = 4
    COMBO_SKIP = 5, 6, 7
    MANIA_HOLD = 8

@unique
class SliderType(Enum):
    LINEAR = 'L'
    BEZIER = 'B'
    PERFECT = 'P'
    CATMUL = 'C'

class PointVector:
    def __init__(self,
                x: int,
                y: int):
        self.x = int(x)
        self.y = int(y)

class HitObject(ABC):
    def __init__(self, 
                x: int, 
                y: int, 
                time: str, 
                type: str, 
                hitsound: str, 
                extras: str=None, 
                **kwargs):
        self.point = PointVector(x, y)
        self.time = int(time)
        self.type = HitObjectType(int(type))
        self.hitsound = int(hitsound)
        self.extras = extras

class SliderObject(HitObject):
    def __init__(self,
                curve_type: str,
                slides: int,
                length: int,
                edge_sounds: str,
                edge_sets: str,
                curve_points: Tuple[dict],
                **kwargs):
        super().__init__(**kwargs)
        self.curve_type = SliderType(curve_type)
        self.curve_points = [PointVector(**coord) for coord in curve_points]
        self.slides = slides
        self.length = length
        self.edge_sounds = edge_sounds
        self.edge_sets = edge_sets

class HitCircle(HitObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SliderCircle(SliderObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TimingPoint(TimingObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class General(GeneralSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MetaData(MetaDetaSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Editor(EditorSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Difficulty(DifficultySettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)