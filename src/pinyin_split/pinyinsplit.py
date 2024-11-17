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
# fmt: on


def split(phrase: str, include_nonstandard: bool = False) -> List[List[str]]:
    """Split a pinyin phrase into all possible valid syllable combinations.

    Args:
        phrase: A string containing pinyin syllables without spaces
        include_nonstandard: Whether to include nonstandard syllables in matching

    Returns:
        A list of lists, where each inner list represents one possible
        way to split the phrase into valid pinyin syllables
    """
    # Create trie and populate with syllables
    trie = CharTrie()
    for syllable in _syllables:
        trie[syllable] = len(syllable)

    if include_nonstandard:
        for syllable in _non_standard_syllables:
            trie[syllable] = len(syllable)

    # Convert input to lowercase for matching
    phrase_lower = phrase.lower()

    # Stack of (start_pos, accumulated_splits) tuples to process
    to_process = []
    valid_splits = []

    # Initialize processing with starting position
    if phrase:
        to_process.append((0, []))

    while to_process:
        # Get next position to process
        start_pos, split_points = to_process.pop()

        # Get remaining text to process
        current_lower = phrase_lower[start_pos:]

        # Find all valid pinyin prefixes
        prefix_matches = trie.prefixes(current_lower)

        for _, length in prefix_matches:
            # Create new list of split points
            new_splits = copy.deepcopy(split_points)
            new_splits.append(start_pos + length)

            if start_pos + length < len(phrase):
                # More text to process - add to stack
                to_process.append((start_pos + length, new_splits))
            else:
                # No more text - we have a complete valid split
                # Convert split points to actual phrase segments
                segments = []
                prev = 0
                for pos in new_splits:
                    segments.append(phrase[prev:pos])
                    prev = pos
                valid_splits.append(segments)

    return valid_splits
