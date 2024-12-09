# py-pinyin-split

A Python library for splitting Hanyu Pinyin words into syllables. Built on [NLTK's](https://github.com/nltk/nltk) [tokenizer interface](https://www.nltk.org/api/nltk.tokenize.html), it handles standard syllables defined in the [Pinyin Table](https://en.wikipedia.org/wiki/Pinyin_table) and supports tone marks.


Based originally on [pinyinsplit](https://github.com/throput/pinyinsplit) by [@tomlee](https://github.com/tomlee).

PyPI: https://pypi.org/project/py-pinyin-split/

## Installation

```bash
pip install py-pinyin-split
```

## Usage

Instantiate a tokenizer and split away.

The tokenizer can handle standard Hanyu Pinyin with whitespaces and punctuation. However, invalid pinyin syllables will raise a `ValueError`

The tokenizer uses some basic heuristics to determine the most likely split - number of syllables, presence of vowels, and syllable frequency data.

```python
from py_pinyin_split import PinyinTokenizer

tokenizer = PinyinTokenizer()

# Basic splitting
tokenizer.tokenize("nǐhǎo")  # ['nǐ', 'hǎo']
tokenizer.tokenize("Běijīng")  # ['Běi', 'jīng']

# Handles whitespace and punctuation
tokenizer.tokenize("Nǐ hǎo ma?")  # ['Nǐ', 'hǎo', 'ma', '?']
tokenizer.tokenize("Wǒ hěn hǎo!")  # ['Wǒ', 'hěn', 'hǎo', '!']

# Handles ambiguous splits using heuristics
tokenizer.tokenize("kěnéng") == ["kě", "néng"]
tokenizer.tokenize("rènào") == ["rè", "nào"]
tokenizer.tokenize("xīan") == ["xī", "an"]
tokenizer.tokenize("xián") == ["xián"]
tokenizer.tokenize("wǎn'ān") == ["wǎn", "'", "ān"]

# Tone marks or punctuation help resolve ambiguity
tokenizer.tokenize("xīān")  # ['xī', 'ān']
tokenizer.tokenize("xián")  # ['xián']
tokenizer.tokenize("Xī'ān") # ["Xī", "'", "ān"]

# Raises ValueError for invalid pinyin
tokenizer.tokenize("hello")  # ValueError

# Optional support for non-standard syllables
tokenizer = PinyinTokenizer(include_nonstandard=True)
tokenizer.tokenize("duang")  # ['duang']
```

## Related Projects
- https://pypi.org/project/pinyintokenizer/
- https://pypi.org/project/pypinyin/
- https://github.com/throput/pinyinsplit
