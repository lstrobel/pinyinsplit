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

 The tokenizer expects a clean Hanyu Pinyin word as input - you'll need to preprocess text to:
- Remove punctuation and whitespace
- Convert numeric tones (pin1yin1) to tone marks (pīnyīn)
- Handle sentence boundaries

The tokenizer uses syllable frequency data to resolve ambiguous splits. It currently does not support apostrophes (sorry!) (e.g. "xi'an" will throw an error)


```python
from pinyin_split import PinyinTokenizer

tokenizer = PinyinTokenizer()

# Basic splitting
tokenizer.tokenize("nǐhǎo")  # ['nǐ', 'hǎo']
tokenizer.tokenize("Běijīng")  # ['Běi', 'jīng']

# Handles ambiguous splits using frequency data
tokenizer.tokenize("xian")  # ['xian'] not ['xi', 'an']
tokenizer.tokenize("wanan")  # ['wan', 'an'] not ['wa', 'nan']

# Tone marks help resolve ambiguity
tokenizer.tokenize("xīān")  # ['xī', 'ān']
tokenizer.tokenize("xián")  # ['xián']

# Optional support for non-standard syllables
tokenizer = PinyinTokenizer(include_nonstandard=True)
tokenizer.tokenize("duang")  # ['duang']
```

## Related Projects
- https://pypi.org/project/pinyintokenizer/
- https://pypi.org/project/pypinyin/
- https://github.com/throput/pinyinsplit