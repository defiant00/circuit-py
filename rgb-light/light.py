class Light:
    def draw(is31, r, g, b, mod, offset):
        color = (int(r) << 16) + (int(g) << 8) + int(b)
        for y in range(9):
            for x in range(13):
                i = y * 13 + x
                c = color if ((i + offset) % mod == 0) else 0
                is31.pixel(x, y, c)
