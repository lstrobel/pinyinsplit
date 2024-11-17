# pinyin-split

A Python library for splitting Hanyu Pinyin phrases into all possible valid syllable combinations. The library supports standard syllables defined in the [Pinyin Table](https://en.wikipedia.org/wiki/Pinyin_table) and optionally includes non-standard syllables.

Based originally on [pinyinsplit](https://github.com/throput/pinyinsplit) by [@tomlee](https://github.com/tomlee).

## Installation

```bash
pip install pinyin-split
```

## Usage

```python
from pinyin_split import split

# Basic splitting - but be careful! The second split here is techinically valid Hanyu Pinyin
split("nihao")
[['ni', 'hao'], ['ni', 'ha', 'o']]

# Case preservation
split("BeijingDaxue")
[['Bei', 'jing', 'Da', 'xue'], ['Bei', 'jing', 'Da', 'xu', 'e']]

# Multiple valid splits
split("xian")
[['xian'], ['xi', 'an']]

# Complex phrases
split("shediaoyingxiongchuan")
[
    ['she', 'diao', 'ying', 'xiong', 'chuan'],
    ['she', 'diao', 'ying', 'xiong', 'chu', 'an'], 
    ['she', 'di', 'ao', 'ying', 'xiong', 'chuan'], 
    ['she', 'di', 'ao', 'ying', 'xiong', 'chu', 'an'],
    ['she', 'di', 'a', 'o', 'ying', 'xiong', 'chuan'],
    ['she', 'di', 'a', 'o', 'ying', 'xiong', 'chu', 'an']
]

# Non-standard syllables (disabled by default)
split("duang")
[['du', 'ang']]

# Enable non-standard syllables
split("duang", include_nonstandard=True)
[['duang'], ['du', 'ang']]

# Invalid input returns empty list
split("xyz")
[]
```