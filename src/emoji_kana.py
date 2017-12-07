from collections import OrderedDict
from emoji_dicts import *

emoji_dict = {}
emoji_dict.update(smiley_dict)
emoji_dict.update(person_dict)
emoji_dict.update(role_dict)
emoji_dict.update(fantasy_dict)
emoji_dict.update(gesture_activity_dict)
emoji_dict.update(sport_dict)
emoji_dict.update(family_dict)
emoji_dict.update(skintone_body_dict)
emoji_dict.update(emotion_clothing_dict)
emoji_dict.update(emotion_clothing_dict)
emoji_dict.update(food_drink_dict)
emoji_dict.update(travel_place_dict)
emoji_dict.update(activity_dict)
emoji_dict.update(object_dict)
emoji_dict.update(symbol_dict)
emoji_dict.update(flag_dict)

EMOJI_SORTED_BY_LENGTH = sorted(emoji_dict.keys(), key=len, reverse=True)

def replace(node):
    surface = node.surface
    feature = node.feature.split(',')
    for key in EMOJI_SORTED_BY_LENGTH:
        #複数変換候補がある場合，とりあえず今は最初の候補に変換
        value = emoji_dict[key].split('|')[0]
        text_copy = text_copy.replace(key, value)
    return text_copy, text!=text_copy
