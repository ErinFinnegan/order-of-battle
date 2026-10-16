"""Draws the phone app's home-screen icons (a yellow star on olive) as PNGs, standard library only."""
import math, struct, zlib, sys, os

def star(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def inside(x, y, poly):
    c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def png(size, path):
    bg, fg = (0x4A, 0x5A, 0x26), (0xFF, 0xC6, 0x29)
    poly = star(size / 2, size * 0.53, size * 0.30, size * 0.12)   # inside the maskable safe zone
    rows = bytearray()
    for y in range(size):
        rows.append(0)
        for x in range(size):
            # 2x2 supersampling for smooth edges
            hits = sum(inside(x + dx, y + dy, poly) for dx in (0.25, 0.75) for dy in (0.25, 0.75)) / 4
            rows += bytes(round(b + (f - b) * hits) for b, f in zip(bg, fg))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)

out = sys.argv[1]
for s in (192, 512):
    png(s, os.path.join(out, f"icon-{s}.png"))
png(180, os.path.join(out, "apple-touch-icon.png"))
print("icons written")
