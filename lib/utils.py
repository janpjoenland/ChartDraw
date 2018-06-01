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
    return '{:02}-{:02} {}'.format(int_part, i, zodiac_sign)


def coordinates(angle):
    "Coord relative to QBasic's intrinsic coordinates]<->['ta0' yields DESC (Cyc 1!)]"
    return (180 - angle) % 360


def preAspectCalc(target, source, ch):
    "Mutates as well as returns target"
    target[0, 0, 1:PPINT + 1] = source[ch, 1:PPINT + 1]
    return target


def aspectCalc(p):
    """Mutates as well as returns w
    Is it supposed to turn spaces at the end into a zero?"""
    r = 0
    out = [['' for _ in range(HPINT)] for __ in range(HPINT)]
    for m in range(HPINT):
        dec_str = float(p[m])
        k1 = int(dec_str)
        u1 = 0
        for y in range(HPINT):
            dec_str = float(p[y])
            k2 = int(dec_str)
            u2 = 0
            if u2 > u1:
                k1 = k1 - 1
                u1 = u1 + 60
            if k2 > k1:
                k1 = k1 + 360
            i = k1 - k2
            if i > 180:
                r = abs(60 - r)
                i = abs(360 - (i + 1))
            out[m][y] = '{:03}-{:02}'.format(i, r)
    return out


def asp(angle, orbis):
    "Second argument is size of orbis"
    aoINT = orbis
    if angle <= aoINT:
        return ':'
    aoINT = orbis // 4
    if abs(30 - angle) <= aoINT:
        return '-'
    aoINT = (orbis // 4) * 3
    if abs(60 - angle) <= aoINT:
        return '*'
    aoINT = orbis
    if abs(90 - angle) <= aoINT:
        return 'k'
    if abs(120 - angle) <= aoINT:
        return 't'
    if abs(180 - angle) <= aoINT:
        return 'o'
    return ''


def complex_to_coords(coords):
    "Maps a list of complex numbers to coordinates suitable for Tkinter"
    res = []
    for c in coords:
        res.append(c.real)
        res.append(c.imag)
    return res
