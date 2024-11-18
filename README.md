# pinyin-split

A Python library for splitting Hanyu Pinyin phrases into all possible valid syllable combinations. The library supports standard syllables defined in the [Pinyin Table](https://en.wikipedia.org/wiki/Pinyin_table), handles tone marks, and optionally includes non-standard syllables.

Based originally on [pinyinsplit](https://github.com/throput/pinyinsplit) by [@tomlee](https://github.com/tomlee).

## Installation

```bash
pip install pinyin-split
```

## Usage

```python
from pinyin_split import split

# Basic splitting - the below is a valid split. Consider filtering by number of syllables if you want to avoid the unlikely second output
split("nihao")
[['ni', 'hao'], ['ni', 'ha', 'o']]

# Tone marks are fully supported
split("nǐhǎo")
[['nǐ', 'hǎo'], ['nǐ', 'hǎ', 'o']]

split("Běijīng")
[['Běi', 'jīng']]

# Case preservation
split("BeijingDaxue")
[['Bei', 'jing', 'Da', 'xue'], ['Bei', 'jing', 'Da', 'xu', 'e']]

# Multiple valid splits
split("xian")  # Could be 先 or 西安
[['xian'], ['xi', 'an']]

# Punctuation and numbers are handled as boundaries
split("xi'an")
[['xi', 'an']]

split("bei3jing1")
[['bei', 'jing']]

# Complex phrases
split("Jiéguǒtāmenyíngle")
[
    ['Jié', 'guǒ', 'tā', 'men', 'yíng', 'le'],
    ['Jié', 'gu', 'ǒ', 'tā', 'men', 'yíng', 'le'],
    ['Ji', 'é', 'guǒ', 'tā', 'men', 'yíng', 'le'],
    ['Ji', 'é', 'gu', 'ǒ', 'tā', 'men', 'yíng', 'le']
]

# Non-standard syllables (disabled by default)
split("duang")
[['du', 'ang']]

# Enable non-standard syllables
split("duang", include_nonstandard=True)
[['duang'], ['du', 'ang']]

# Enable erhua support
split("yidianr", include_erhua=True) 
[["yi", "dian", "r"], ["yi", "di", "an", "r"]]

# Invalid input returns empty list
split("xyz")
[]
```
