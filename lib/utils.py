"""Functions used by aq_draw"""

ZODIAC_SIGNS = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir',
                'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Psc']

PPINT = 13
HPINT = 12


def truncate_rounding(angle):
    """Sub TruncateRounding"""
    if type(angle) == str:
        angle = float(angle)
    int_part = int(angle)
    decimal_part = angle - int_part
    zodiac_sign = ZODIAC_SIGNS[int_part // 30]
    int_part = int_part % 30
    i = round(decimal_part * 60)
    if i > 59:
        i -= 60
        int_part += 1
    return "{:02}° {:02}' {}".format(int_part, i, zodiac_sign)


def dms_to_deg(degrees, minutes, seconds):
    "Convert a DMS angle to decimal degrees"
    if minutes < 0 or minutes >= 60:
        raise ValueError('Minutes must be 0 <= m < 60')
    if seconds < 0 or seconds >= 60:
        raise ValueError('Seconds must be 0 <= s < 60')
    return degrees + (minutes * 60 + seconds) / 3600


def mirror_angle(angle):
    "Mirrors the angle: 0 deg to the left, going clockwise"
    return (180 - angle) % 360


def asp(a, b, orbis=8):
    "Second argument is size of orbis"
    angle = min(abs(a - b), 360 - abs(a - b))
    aspects = [0, 30, 60, 90, 120, 180]
    for aspect in aspects:
        orbis_factor = 1
        if aspect == 30:
            orbis_factor = 0.25
        elif aspect == 60:
            orbis_factor = 0.75
        
        if abs(aspect - angle) <= (orbis * orbis_factor):
            return aspect, 1 - abs(aspect - angle) / (orbis * orbis_factor)
    return None, None


def dist(a, b):
    "Closest angular distance between points a and b, in degrees"
    return min(abs(a - b), 360 - abs(a - b))


def is_sorted(a, b):
    "return true if a' is the clockwise-most angle"
    return (b - a) % 360 == dist(a, b)


def complex_to_coords(coords):
    "Maps a list of complex numbers to coordinates suitable for Tkinter"
    res = []
    for c in coords:
        res.append(c.real)
        res.append(c.imag)
    return res


def harmonics(angles, harmonic):
    return [(harmonic * angle) % 360 for angle in angles]
