from colorthief import ColorThief

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    return color_thief.get_color(quality=1)

def infer_emotion_from_color(color):
    r, g, b = color
    if r > 200 and g < 100 and b < 100:
        return "exciting or fiery"
    elif b > 180:
        return "calm or dreamy"
    elif g > 180:
        return "fresh or joyful"
    else:
        return "mysterious or adventurous"
