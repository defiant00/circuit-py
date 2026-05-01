class Pattern:
    def __init__(self, hour, minute, every, r, g, b):
        self.minute = hour * 60 + minute
        self.every = every
        self.r = r
        self.g = g
        self.b = b

    def scaled_color(self, scale):
        return (self.r * scale, self.g * scale, self.b * scale)

    def is_on(self, minute, offset):
        return (minute + offset) % self.every == 0

    def offset(self, hour):
        return Pattern(hour, self.minute, self.every, self.r, self.g, self.b)


class Light:
    def __init__(self):
        self.patterns = [
            Pattern(8, 0, 2, 0, 100, 150),
            Pattern(8, 15, 2, 10, 0, 0),
            Pattern(8, 30, 2, 80, 0, 0),
            Pattern(9, 0, 2, 120, 60, 0),
            Pattern(9, 30, 2, 120, 60, 0),
            Pattern(10, 0, 1, 0, 0, 0),
            Pattern(16, 0, 1, 0, 0, 0),
            Pattern(16, 30, 2, 0, 100, 150),
        ]

        first = self.patterns[-1].offset(-24)
        last = self.patterns[0].offset(24)

        self.patterns.insert(0, first)
        self.patterns.append(last)

    def draw(self, is31, minute):
        idx = 0
        for i in range(len(self.patterns)):
            if self.patterns[i].minute >= minute:
                idx = i - 1
                break

        p1 = self.patterns[idx]
        p2 = self.patterns[idx + 1]
        min_total = p2.minute - p1.minute
        r1 = (min_total - (minute - p1.minute)) / min_total
        r2 = (min_total - (p2.minute - minute)) / min_total

        sc1 = p1.scaled_color(r1)
        sc2 = p2.scaled_color(r2)
        scb = (sc1[0] + sc2[0], sc1[1] + sc2[1], sc1[2] + sc2[2])

        c1 = (int(sc1[0]) << 16) + (int(sc1[1]) << 8) + int(sc1[2])
        c2 = (int(sc2[0]) << 16) + (int(sc2[1]) << 8) + int(sc2[2])
        cb = (int(scb[0]) << 16) + (int(scb[1]) << 8) + int(scb[2])

        for y in range(8):
            for x in range(13):
                c = 0
                o = y * 13 + x
                on1 = p1.is_on(minute, o)
                on2 = p2.is_on(minute, o)
                if on1 and on2:
                    c = cb
                elif on1:
                    c = c1
                elif on2:
                    c = c2
                is31.pixel(x, y + 1, c)
