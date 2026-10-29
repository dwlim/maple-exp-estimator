#!/usr/bin/env python3
"""Download OSMS map renders and extract platform/rope geometry without shipping images."""
import concurrent.futures
import json, re, struct, subprocess, sys, tempfile, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEOMETRY_JS = ROOT / 'map-geometry.js'
OUT = ROOT / 'map-geometry.js'

def png_pixels(path):
    data = Path(path).read_bytes(); pos = 8; chunks = []; width = height = color_type = None
    while pos < len(data):
        size = struct.unpack('>I', data[pos:pos+4])[0]; kind = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+size]; pos += size + 12
        if kind == b'IHDR': width, height, depth, color_type, _, _, _ = struct.unpack('>IIBBBBB', chunk)
        elif kind == b'IDAT': chunks.append(chunk)
    if depth != 8 or color_type not in (2, 6): raise ValueError(f'unsupported PNG format {depth}/{color_type}')
    import zlib
    raw = zlib.decompress(b''.join(chunks)); channels = 4 if color_type == 6 else 3; stride = width * channels
    rows = []; previous = [0] * stride; at = 0
    for _ in range(height):
        mode = raw[at]; at += 1; row = list(raw[at:at+stride]); at += stride
        for i, value in enumerate(row):
            left = row[i-channels] if i >= channels else 0; up = previous[i]; upper_left = previous[i-channels] if i >= channels else 0
            if mode == 1: value += left
            elif mode == 2: value += up
            elif mode == 3: value += (left + up) // 2
            elif mode == 4:
                p = left + up - upper_left; pa = abs(p-left); pb = abs(p-up); pc = abs(p-upper_left)
                value += left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
            row[i] = value & 255
        rows.append([tuple(row[i:i+channels]) for i in range(0, stride, channels)]); previous = row
    return width, height, rows

def opaque(pixel): return pixel[-1] > 40 if len(pixel) == 4 else True

def green(pixel):
    r, g, b = pixel[:3]
    return opaque(pixel) and g > 55 and g > r * 1.08 and g > b * 1.03

def runs(values, minimum):
    result = []; start = None
    for i, yes in enumerate(values + [False]):
        if yes and start is None: start = i
        elif not yes and start is not None:
            if i - start >= minimum: result.append([start, i - 1])
            start = None
    return result

def extract(path):
    width, height, pixels = png_pixels(path)
    # Grass/platform tops are long green horizontal runs. Merge adjacent scanlines.
    raw_platforms = []
    for y, row in enumerate(pixels):
        for x1, x2 in runs([green(p) for p in row], 28):
            raw_platforms.append((x1, x2, y))
    platforms = []
    for x1, x2, y in raw_platforms:
        match = next((p for p in platforms if abs(p[2] - y) <= 8 and x1 <= p[1] + 18 and x2 >= p[0] - 18), None)
        if match:
            match[0] = min(match[0], x1); match[1] = max(match[1], x2); match[2] = round((match[2] + y) / 2)
        else: platforms.append([x1, x2, y])
    platforms = [[x1, x2, y] for x1, x2, y in platforms if x2 - x1 >= 45]
    # Ropes/vines are narrow vertical green structures with substantial vertical continuity.
    rope_columns = []
    for x in range(width):
        ys = [green(p) for p in (pixels[y][x] for y in range(height))]
        for y1, y2 in runs(ys, 45):
            if y2 - y1 >= 65: rope_columns.append([x, y1, y2])
    ropes = []
    for x, y1, y2 in rope_columns:
        match = next((r for r in ropes if abs(r[0] - x) <= 12 and y1 <= r[2] + 25 and y2 >= r[1] - 25), None)
        if match:
            match[0] = round((match[0] + x) / 2); match[1] = min(match[1], y1); match[2] = max(match[2], y2)
        else: ropes.append([x, y1, y2])
    ropes = [[x, y1, y2] for x, y1, y2 in ropes if y2-y1 >= 80]
    return {'width': width, 'height': height, 'platforms': platforms, 'ropes': ropes}

def load_sources():
    text = GEOMETRY_JS.read_text()
    return json.loads(text[text.index('{'):text.rindex('}')+1])

def parse_one(item):
    map_id, source, tmp = item
    url = source.get('renderUrl')
    if not url: return map_id, source
    webp = Path(tmp) / f'{map_id}.webp'; png = Path(tmp) / f'{map_id}.png'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webp.write_bytes(urllib.request.urlopen(request, timeout=30).read())
        subprocess.run(['sips', '-s', 'format', 'png', str(webp), '--out', str(png)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return map_id, {**source, **extract(png)}
    except Exception as exc:
        print(f'skipping {map_id}: {exc}', file=sys.stderr)
        return map_id, source

def main():
    sources = load_sources()
    requested = set(sys.argv[1:])
    if requested: sources = {key: value for key, value in sources.items() if key in requested}
    result = {}
    with tempfile.TemporaryDirectory() as tmp:
        items = [(map_id, source, tmp) for map_id, source in sources.items()]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(parse_one, item) for item in items]
            for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
                map_id, parsed = future.result(); result[map_id] = parsed
                print(f'{index}/{len(items)} {map_id}: {len(parsed.get("platforms", []))} platforms, {len(parsed.get("ropes", []))} ropes', file=sys.stderr)
    ordered = {map_id: result[map_id] for map_id in sources if map_id in result}
    OUT.write_text('const OSMS_MAP_GEOMETRY = ' + json.dumps(ordered, separators=(',', ':')) + ';\n')

if __name__ == '__main__': main()
