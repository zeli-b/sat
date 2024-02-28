from math import atan2, hypot, sin, cos, pi

size = 250
padding = 125


def draw_part(edges, id_, x, y):
    if id_ & 0b1000:
        edges.append((size*x, size*y, size, 0))

    if id_ & 0b0100:
        edges.append((size*(x+1), size*y, 0, size))

    if id_ & 0b0010:
        edges.append((size*x, size*y, 0, size))

    if id_ & 0b0001:
        edges.append((size*x, size*(y+1), size, 0))


def is_mass(edges, point):
    for i in range(len(edges)):
        edge = edges[i]

        if edge[0] == point[0] and edge[1] == point[1]:
            return i, 1

        if edge[0] + edge[2] == point[0] and edge[1] + edge[3] == point[1]:
            return i, 2

    return -1, 0


def equal_point(point1, point2):
    return point1[0] == point2[0] and point1[1] == point2[1]


def is_connected(edges, point1, point2, beens = None):
    if equal_point(point1, point2):
        return True

    if beens is None:
        beens = list()

    # check been
    for i in range(len(beens)):
        if equal_point(beens[i], point1):
            return False

    # dfs
    beens.append(point1)
    for i in range(len(edges)):
        edge = edges[i];

        start = (edge[0], edge[1])
        end = (edge[0] + edge[2], edge[1] + edge[3])

        if equal_point(point1, start) \
                and is_connected(edges, end, point2, beens):
            return True

        if equal_point(point1, end) \
                and is_connected(edges, start, point2, beens):
            return True

    return False


def index_of_edge(edges, other):
    for i in range(len(edges)):
        edge = edges[i]

        if edge[0] == other[0] \
                and edge[1] == other[1] \
                and edge[0] + edge[2] == other[0] + other[2] \
                and edge[1] + edge[3] == other[1] + other[3]:
            return i

        if edge[0] == other[0] + other[2] \
                and edge[1] == other[1] + other[3] \
                and edge[0] + edge[2] == other[0] \
                and edge[1] + edge[3] == other[1]:
            return i

    return -1


def remove_node(edges, node):
    index = index_of_edge(edges, node)

    if index == -1:
        return edges

    edges.pop(index)
    return edges


def draw(letter):
    char_code = ord(letter)

    # -- lines
    edges = list()

    draw_part(edges, (char_code >> 12) & 0xff, 1, 0);
    draw_part(edges, (char_code >> 8) & 0xff, 2, 1);
    draw_part(edges, (char_code >> 4) & 0xff, 0, 1);
    draw_part(edges, (char_code >> 0) & 0xff, 1, 2);

    # -- add extra points
    extra = list()
    for i in range(4):
        x = size * i
        px = size * (i+1)

        for j in range(4):
            y = size * j
            py = size * (j+1)

            r_edge = [x, y, size, 0]
            d_edge = [x, y, 0, size]

            if is_mass(edges, [x, y])[0] != -1:
                continue

            added = False
            if i < 3 and is_mass(edges, [px, y])[0] == -1:
                extra.append(r_edge)
                added = True
            if j < 3 and is_mass(edges, [x, py])[0] == -1:
                extra.append(d_edge)
                added = True

            if not added:
                extra.append([x, y, 0, 0])

    for i in range(len(extra)):
        edges.append(extra[i])

    # join connected lines
    while True:
        changed = False
        i = 0
        while i < len(edges):
            x1 = edges[i][0]
            y1 = edges[i][1]
            x2 = x1 + edges[i][2]
            y2 = y1 + edges[i][3]
            direction1 = atan2(y2-y1, x2-x1)

            j = 0
            while j < len(edges):
                if i == j:
                    j += 1
                    continue

                x3 = edges[j][0]
                y3 = edges[j][1]
                x4 = x3 + edges[j][2]
                y4 = y3 + edges[j][3]
                direction2 = atan2(y4-y3, x4-x3)

                distance = hypot(x2-x3, y2-y3)
                direction_delta = direction2 - direction1

                if distance < 0.1 and abs(direction_delta) < 0.1:
                    if j > i:
                        edges.pop(j)
                        edges.pop(i)
                    else:
                        edges.pop(i)
                        edges.pop(j)
                    edges.append((x1, y1, x4-x1, y4-y1))
                    changed = True

                j += 1
            i += 1

        if not changed:
            break

    paths = []
    for i in range(len(edges)):
        x1 = edges[i][0]
        y1 = edges[i][1]
        dx = edges[i][2]
        dy = edges[i][3]

        paths.append(((x1, y1), (dx, dy)))

    return paths


d = size/8
# size/8: regular
# size/4: bold
enlongate = d
offset_y = 1000 - size

def create_path(point, delta):
    x, y = point
    dx, dy = delta

    y = offset_y - y
    dy = -dy

    theta = atan2(dy, dx)

    x -= enlongate * cos(theta)
    y -= enlongate * sin(theta)
    dx += 2*enlongate * cos(theta)
    dy += 2*enlongate * sin(theta)

    xa = x + d * cos(theta + pi / 2)
    ya = y + d * sin(theta + pi / 2)
    xb = x + d * cos(theta - pi / 2)
    yb = y + d * sin(theta - pi / 2)
    xq = x + dx + d * cos(theta - pi / 2)
    yq = y + dy + d * sin(theta - pi / 2)
    xr = x + dx + d * cos(theta + pi / 2)
    yr = y + dy + d * sin(theta + pi / 2)

    dots = []
    dots.append((xa, ya))
    dots.append((xb, yb))
    dots.append((xq, yq))
    dots.append((xr, yr))

    return dots


def create_glyph(char, font):
    glyph = font.createChar(ord(char))

    pen = glyph.glyphPen()

    paths = draw(char)
    for point, delta in paths:
        dots = create_path(point, delta)

        for i, dot in enumerate(dots):
            if i == 0:
                pen.moveTo(dot)
            else:
                pen.lineTo(dot)
        pen.closePath()

    pen = None


def main():
    font = fontforge.fonts()[0]

    # ascii
    for i in range(ord(' '), 0xff + 1):
        create_glyph(chr(i), font)

    # hangul-jamo
    for i in range(0x1100, 0x11ff + 1):
        create_glyph(chr(i), font)
    for i in range(0x3130, 0x318f + 1):
        create_glyph(chr(i), font)

    # hangul
    for i in range(ord('가'), ord('힣') + 1):
        create_glyph(chr(i), font)

    # hanja
    for i in range(0x4e00, 0x9fff + 1):
        create_glyph(chr(i), font)



if __name__ == '__main__':
    main()
