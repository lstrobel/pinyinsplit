# pinyin-split

A Python library for splitting Chinese Pinyin phrases into possible permutations of valid Pinyin syllables.

Based originally on [pinyinsplit](https://github.com/throput/pinyinsplit) by [@tomlee](https://github.com/tomlee).

## Installation

```bash
pip install pinyin-split
```

## Usage

```python
from pinyin_split import split

# Basic usage
split('xianggangdaxue')
[['xiang', 'gang', 'da', 'xue'], ['xiang', 'gang', 'da', 'xu', 'e'], 
 ['xi', 'ang', 'gang', 'da', 'xue'], ['xi', 'ang', 'gang', 'da', 'xu', 'e']]

# Complex example
split('shediaoyingxiongchuan')
[['she', 'diao', 'ying', 'xiong', 'chuan'], 
 ['she', 'diao', 'ying', 'xiong', 'chu', 'an'],
 ['she', 'di', 'ao', 'ying', 'xiong', 'chuan'],
 ['she', 'di', 'ao', 'ying', 'xiong', 'chu', 'an']]

# Invalid input returns empty list
split('shediaoyingxiongchuanxyz')
[]
```
