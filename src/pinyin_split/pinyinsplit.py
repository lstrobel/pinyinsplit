import copy
from typing import List
from pygtrie import CharTrie

# List of valid Pinyin syllables
# fmt: off
_syllables = [
    'a', 'o', 'e', 'ê', 'ai', 'ei', 'ao', 'ou', 'an', 'en', 'ang', 'eng', 'er',
    'yi', 'ya', 'yo', 'ye', 'yao', 'you', 'yan', 'yin', 'yang', 'ying',
    'wu', 'wa', 'wo', 'wai', 'wei', 'wan', 'wen', 'wang', 'weng',
    'yu', 'yue', 'yuan', 'yun', 'yong',
    
    'ba', 'bai', 'bei', 'bao', 'ban', 'ben', 'bang', 'beng',
    'bi', 'bie', 'biao', 'bian', 'bin', 'bing',
    'bu', 'bo',
    
    'pa', 'pai', 'pei', 'pao', 'pou', 'pan', 'pen', 'pang', 'peng',
    'pi', 'pie', 'piao', 'pian', 'pin', 'ping',
    'pu', 'po',
    
    'ma', 'me', 'mai', 'mei', 'mao', 'mou', 'man', 'men', 'mang', 'meng',
    'mi', 'mie', 'miao', 'miu', 'mian', 'min', 'ming',
    'mu', 'mo',
    
    'fa', 'fei', 'fou', 'fan', 'fen', 'fang', 'feng',
    'fu', 'fo',
    
    'da', 'de', 'dai', 'dei', 'dao', 'dou', 'dan', 'den', 'dang', 'deng',
    'di', 'die', 'diao', 'diu', 'dian', 'din', 'ding',
    'du', 'duo', 'dui', 'duan', 'dun', 'dong',
    
    'ta', 'te', 'tai', 'tao', 'tou', 'tan', 'tang', 'teng',
    'ti', 'tie', 'tiao', 'tian', 'ting',
    'tu', 'tuo', 'tui', 'tuan', 'tun', 'tong',
    
    'na', 'ne', 'nai', 'nei', 'nao', 'nou', 'nan', 'nen', 'nang', 'neng',
    'ni', 'nie', 'niao', 'niu', 'nian', 'nin', 'niang', 'ning',
    'nu', 'nuo', 'nuan', 'nun', 'nong',
    'nü', 'nüe',
    
    'la', 'lo', 'le', 'lai', 'lei', 'lao', 'lou', 'lan', 'lang', 'leng',
    'li', 'lie', 'liao', 'liu', 'lian', 'lin', 'liang', 'ling',
    'lu', 'luo', 'luan', 'lun', 'long',
    'lü', 'lüe',
    
    'ga', 'ge', 'gai', 'gei', 'gao', 'gou', 'gan', 'gen', 'gang', 'geng',
    'gu', 'gua', 'guo', 'guai', 'gui', 'guan', 'gun', 'guang', 'gong',
    
    'ka', 'ke', 'kai', 'kao', 'kou', 'kan', 'ken', 'kang', 'keng',
    'ku', 'kua', 'kuo', 'kuai', 'kui', 'kuan', 'kun', 'kuang', 'kong',
    
    'ha', 'he', 'hai', 'hei', 'hao', 'hou', 'han', 'hen', 'hang', 'heng',
    'hu', 'hua', 'huo', 'huai', 'hui', 'huan', 'hun', 'huang', 'hong',
    
    'ji', 'jia', 'jie', 'jiao', 'jiu', 'jian', 'jin', 'jiang', 'jing',
    'ju', 'jue', 'juan', 'jun', 'jiong',
    
    'qi', 'qia', 'qie', 'qiao', 'qiu', 'qian', 'qin', 'qiang', 'qing',
    'qu', 'que', 'quan', 'qun', 'qiong',

    'xi', 'xia', 'xie', 'xiao', 'xiu', 'xian', 'xin', 'xiang', 'xing',
    'xu', 'xue', 'xuan', 'xun', 'xiong',
    
    'zhi', 'zha', 'zhe', 'zhai', 'zhao', 'zhou', 'zhan', 'zhen', 'zhang', 'zheng',
    'zhu', 'zhua', 'zhuo', 'zhuai', 'zhui', 'zhuan', 'zhun', 'zhuang', 'zhong',

    'chi', 'cha', 'che', 'chai', 'chao', 'chou', 'chan', 'chen', 'chang', 'cheng',
    'chu', 'chua', 'chuo', 'chuai', 'chui', 'chuan', 'chun', 'chuang', 'chong',

    'shi', 'sha', 'she', 'shai', 'shei', 'shao', 'shou', 'shan', 'shen', 'shang', 'sheng',
    'shu', 'shua', 'shuo', 'shuai', 'shui', 'shuan', 'shun', 'shuang',

    'ri', 're', 'rao', 'rou', 'ran', 'ren', 'rang', 'reng',
    'ru', 'ruo', 'rui', 'ruan', 'run', 'rong',

    'zi', 'za', 'ze', 'zai', 'zei', 'zao', 'zou', 'zan', 'zen', 'zang', 'zeng',
    'zu', 'zuo', 'zui', 'zuan', 'zun', 'zong',

    'ci', 'ca', 'ce', 'cai', 'cao', 'cou', 'can', 'cen', 'cang', 'ceng',
    'cu', 'cuo', 'cui', 'cuan', 'cun', 'cong',

    'si', 'sa', 'se', 'sai', 'sao', 'sou', 'san', 'sen', 'sang', 'seng',
    'su', 'suo', 'sui', 'suan', 'sun', 'song',
]

_non_standard_syllables = [
    'yai', 'ong', 
    'biang', 
    'pia', 'pun',
    'fai', 'fiao',
    'dia', 'diang', 'duang',
    'tei', 
    'nia', 'nui',
    'len', 'lia',
    'lüan', 'lün',
    'gin', 'ging', 
    'kei', 'kiu', 'kiang',
    'zhei',
    'rua',
    'cei',
    'sei'
]

# Mapping of base vowels to their tone variants
_tone_marks = {
    'a': 'āáǎà', 'A': 'ĀÁǍÀ',
    'e': 'ēéěè', 'E': 'ĒÉĚÈ',
    'i': 'īíǐì', 'I': 'ĪÍǏÌ',
    'o': 'ōóǒò', 'O': 'ŌÓǑÒ',
    'u': 'ūúǔù', 'U': 'ŪÚǓÙ',
    'ü': 'ǖǘǚǜ', 'Ü': 'ǕǗǙǛ',
}
# fmt: on


def _add_tone_variants(syllable: str) -> list[str]:
    """Generate all valid tone variants for a syllable."""
    variants = [syllable]  # Include toneless variant

    # Find the vowels in the syllable (both upper and lower case)
    vowels = [c for c in syllable if c.lower() in "aeiouü"]
    if not vowels:
        return variants

    # Determine which vowel gets the tone mark
    tone_vowel = None
    # Preserve case when finding the tone vowel
    if any(v.lower() == "a" for v in vowels):
        tone_vowel = next(v for v in vowels if v.lower() == "a")
    elif any(v.lower() == "e" for v in vowels):
        tone_vowel = next(v for v in vowels if v.lower() == "e")
    elif any(v.lower() == "o" for v in vowels):
        tone_vowel = next(v for v in vowels if v.lower() == "o")
    else:
        tone_vowel = vowels[-1]

    # Generate variants with each tone mark
    for i in range(4):
        variant = syllable.replace(tone_vowel, _tone_marks[tone_vowel][i])
        variants.append(variant)

    return variants


def split(
    phrase: str, include_nonstandard: bool = False, include_erhua=False
) -> List[List[str]]:
    """Split a pinyin phrase into valid syllable combinations.

    Handles both toned and toneless pinyin input. Punctuation and numbers will not be
    preserved in the output, but do influence syllable boundaries.

    Args:
        phrase: A string containing pinyin syllables, optionally with punctuation/numbers
        include_nonstandard: Whether to include nonstandard syllables in matching

    Returns:
        A list of lists, where each inner list represents one possible
        way to split the phrase into valid pinyin syllables
    """
    trie = CharTrie()

    # Add standard syllables and their tone variants
    for syllable in _syllables:
        for variant in _add_tone_variants(syllable):
            trie[variant] = len(variant)

    # Add non-standard syllables if requested
    if include_nonstandard:
        for syllable in _non_standard_syllables:
            for variant in _add_tone_variants(syllable):
                trie[variant] = len(variant)

    # Add erhua if requested
    if include_erhua:
        trie["r"] = 1

    # Find positions of punctuation and numbers
    boundaries = []
    non_pinyin_chars = []
    for i, char in enumerate(phrase):
        if not char.isalpha():
            boundaries.append(i)
            non_pinyin_chars.append(char)

    # Split the phrase at boundaries
    if not boundaries:
        segments = [phrase]
    else:
        segments = []
        prev = 0
        for pos in boundaries:
            if pos > prev:
                segments.append(phrase[prev:pos])
            segments.append(phrase[pos : pos + 1])
            prev = pos + 1
        if prev < len(phrase):
            segments.append(phrase[prev:])

    # Process each segment
    result = [[]]
    for segment in segments:
        if not segment.isalpha():
            # Skip non-pinyin characters
            continue

        # Process pinyin segment
        to_process = [(0, [])]
        segment_splits = []

        while to_process:
            start_pos, split_points = to_process.pop()
            current = segment[start_pos:].lower()

            prefix_matches = trie.prefixes(current)

            for _, length in prefix_matches:
                new_splits = copy.deepcopy(split_points)
                new_splits.append(start_pos + length)

                if start_pos + length < len(segment):
                    to_process.append((start_pos + length, new_splits))
                else:
                    parts = []
                    prev = 0
                    for pos in new_splits:
                        parts.append(segment[prev:pos])
                        prev = pos
                    segment_splits.append(parts)

        if not segment_splits:
            return []

        # Combine with existing results
        new_result = []
        for existing in result:
            for split_option in segment_splits:
                new_result.append(existing + split_option)
        result = new_result

    return result if result != [[]] else []
