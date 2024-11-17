import copy
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

_trie: CharTrie | None = None


def _init_trie() -> None:
    """Initialize the trie with pinyin syllables if not already initialized.

    The trie is used for efficient prefix matching of pinyin syllables.
    Each syllable is stored with its length as the value.
    """
    global _trie
    if _trie is None:
        _trie = CharTrie()
        for syllable in _syllables:
            _trie[syllable] = len(syllable)


def split(phrase: str) -> list[list[str]]:
    """Split a pinyin phrase into all possible valid syllable combinations.

    Args:
        phrase: A string containing pinyin syllables without spaces

    Returns:
        A list of lists, where each inner list represents one possible
        way to split the phrase into valid pinyin syllables
    """
    _init_trie()

    # Convert input to lowercase for matching
    phrase_lower = phrase.lower()

    # Stack of (original, lowercase, accumulated_syllables) tuples to process
    to_process = []
    valid_splits = []

    # Initialize processing with the full phrase
    if phrase:
        to_process.append((phrase, phrase_lower, []))

    while to_process:
        # Get next phrase to process
        current, current_lower, syllables = to_process.pop()

        # Find all valid pinyin prefixes
        prefix_matches = _trie.prefixes(current_lower)

        for _, length in prefix_matches:
            # Extract the matched prefix and remaining text
            matched_syllable = current[:length].lower()
            remaining_text = current[length:]
            remaining_lower = current_lower[length:]

            # Create new list of accumulated syllables
            new_syllables = copy.deepcopy(syllables)
            new_syllables.append(matched_syllable)

            if remaining_text:
                # More text to process - add to stack
                to_process.append((remaining_text, remaining_lower, new_syllables))
            else:
                # No more text - we have a complete valid split
                valid_splits.append(new_syllables)

    return valid_splits
