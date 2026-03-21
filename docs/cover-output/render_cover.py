from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

root = Path('docs/cover-output')
root.mkdir(parents=True, exist_ok=True)
md_path = Path('docs/00-COVER.md')
text = md_path.read_text(encoding='utf-8')

W, H = 1600, 2560
img = Image.new('RGB', (W, H), '#f7f1e6')
draw = ImageDraw.Draw(img)

# soft vertical gradient
for y in range(H):
    t = y / (H - 1)
    r = int(247 + (216 - 247) * t)
    g = int(241 + (202 - 241) * t)
    b = int(230 + (180 - 230) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

font_candidates = [
    'C:/Windows/Fonts/yumin.ttf',
    'C:/Windows/Fonts/YuGothM.ttc',
    'C:/Windows/Fonts/meiryo.ttc',
]

def load_font(size):
    for p in font_candidates:
        fp = Path(p)
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size=size)
            except Exception:
                continue
    return ImageFont.load_default()

f_h1 = load_font(76)
f_h2 = load_font(46)
f_h3 = load_font(36)
f_body = load_font(34)

x = 120
y = 140
max_w = W - 240
line_gap = 14


def draw_wrapped(line: str, font, fill=(26, 26, 26), bullet=False):
    global y
    prefix = '• ' if bullet else ''
    content = prefix + line
    avg_char_w = max(14, int(draw.textlength('あ', font=font)))
    wrap_width = max(8, max_w // avg_char_w)
    wrapped = textwrap.wrap(content, width=wrap_width, break_long_words=False, break_on_hyphens=False)
    if not wrapped:
        y += int(font.size * 0.6)
        return
    for wline in wrapped:
        draw.text((x, y), wline, font=font, fill=fill)
        y += int(font.size + line_gap)

for raw in text.splitlines():
    s = raw.strip()
    if not s:
        y += 14
        continue
    if s == '---':
        draw.line([(x, y + 8), (W - 120, y + 8)], fill=(80, 80, 80), width=2)
        y += 34
        continue
    if s.startswith('# '):
        draw_wrapped(s[2:].strip(), f_h1)
        y += 12
        continue
    if s.startswith('## '):
        draw_wrapped(s[3:].strip(), f_h2)
        y += 8
        continue
    if s.startswith('### '):
        draw_wrapped(s[4:].strip(), f_h3)
        y += 6
        continue
    if s.startswith('- '):
        draw_wrapped(s[2:].strip(), f_body, bullet=True)
        continue
    draw_wrapped(s, f_body)

png_path = root / '00-COVER.png'
jpg_path = root / '00-COVER.jpg'
tif_path = root / '00-COVER.tif'
tiff_path = root / '00-COVER.tiff'

img.save(png_path, format='PNG')
img.save(jpg_path, format='JPEG', quality=92, optimize=True)
img.save(tif_path, format='TIFF', compression='tiff_deflate')
img.save(tiff_path, format='TIFF', compression='tiff_deflate')

print('CREATED', png_path)
print('CREATED', jpg_path)
print('CREATED', tif_path)
print('CREATED', tiff_path)
