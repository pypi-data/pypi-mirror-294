from enum import Enum
import os

class Voices(Enum):
    SILVAN = os.path.join(os.path.dirname(__file__), "voices", "silvan.voicex")
    GABBY = os.path.join(os.path.dirname(__file__), "voices", "gabby.voicex")
    GRANNY = os.path.join(os.path.dirname(__file__), "voices", "granny.voicex")
    KIMBERLY = os.path.join(os.path.dirname(__file__), "voices", "kimberly.voicex")
    ELISABETH = os.path.join(os.path.dirname(__file__), "voices", "drw_female_1.voicex")
    LISA = os.path.join(os.path.dirname(__file__), "voices", "lisa_old.voicex")
    DRW_FEMALE_1 = os.path.join(os.path.dirname(__file__), "voices", "drw_female_1.voicex")
    DRW_FEMALE_2 = os.path.join(os.path.dirname(__file__), "voices", "drw_female_2.voicex")
    DRW_FEMALE_3 = os.path.join(os.path.dirname(__file__), "voices", "drw_female_3.voicex")
    MALE_DEPRESSED = os.path.join(os.path.dirname(__file__), "voices", "male_depressed.voicex")
    MALE_SHY_1 = os.path.join(os.path.dirname(__file__), "voices", "male_shy_1.voicex")
    MALE_SHY_2 = os.path.join(os.path.dirname(__file__), "voices", "male_shy_2.voicex")
    LENNY = os.path.join(os.path.dirname(__file__), "voices", "lenny.voicex")
    ANDREA = os.path.join(os.path.dirname(__file__), "voices", "andrea.voicex")
