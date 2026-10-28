from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
source = root / 'resources' / 'hajala-icon.png'
res = root / 'android' / 'app' / 'src' / 'main' / 'res'
im = Image.open(source).convert('RGBA')
# Legacy launcher icons for older Android launchers.
for density, size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    folder = res / f'mipmap-{density}'
    folder.mkdir(parents=True, exist_ok=True)
    im.resize((size,size), Image.Resampling.LANCZOS).save(folder / 'ic_launcher.png', optimize=True)
# Adaptive icon foreground/background for Android 8+.
for density, size in [('mdpi',108),('hdpi',162),('xhdpi',216),('xxhdpi',324),('xxxhdpi',432)]:
    folder = res / f'mipmap-{density}'
    folder.mkdir(parents=True, exist_ok=True)
    im.resize((size,size), Image.Resampling.LANCZOS).save(folder / 'ic_launcher_foreground.png', optimize=True)
anydpi = res / 'mipmap-anydpi-v26'
anydpi.mkdir(parents=True, exist_ok=True)
(anydpi / 'ic_launcher.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@color/hajala_icon_background" />\n    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n</adaptive-icon>\n''', encoding='utf-8')
values = res / 'values'
values.mkdir(parents=True, exist_ok=True)
colors = values / 'hajala_icon_colors.xml'
colors.write_text('''<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="hajala_icon_background">#210018</color>\n</resources>\n''', encoding='utf-8')
# Keep app launcher label in Arabic.
manifest = root / 'android' / 'app' / 'src' / 'main' / 'AndroidManifest.xml'
if manifest.exists():
    text = manifest.read_text(encoding='utf-8')
    import re
    text = re.sub(r'\s+android:roundIcon="[^"]*"', '', text)
    text = text.replace('android:icon="@mipmap/ic_launcher"', 'android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher"')
    manifest.write_text(text, encoding='utf-8')
print('Hajala launcher icons installed.')
