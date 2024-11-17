import copy
from pygtrie import CharTrie

# List of valid Pinyin syllables
# fmt: off
_syllables = [
    'a', 'ai', 'an', 'ang', 'ao',
    'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng',
    'bi', 'bian', 'biang', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu',
    'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen', 'ceng',
    'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng',
    'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo',
    'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo',
    'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng',
    'di', 'dia', 'dian', 'diang', 'diao', 'die', 'ding', 'diu',
    'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo',
    'e', 'ei', 'en', 'eng', 'er',
    'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fiao',
    'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang', 'gao',
    'ge', 'gei', 'gen', 'geng', 'gong', 'gou',
    'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo',
    'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng',
    'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo',
    'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun',
    'ka', 'kai', 'kan', 'kang', 'kao', 'ke', 'kei', 'ken', 'keng',
    'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun', 'kuo',
    'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng',
    'li', 'lia', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'long', 'lou',
    'lu', 'luan', 'lue', 'lun', 'luo', 'lv', 'lve', 'lvn', 'lü', 'lüe', 'lün',
    'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng',
    'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu',
    'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng',
    'ni', 'nia', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu',
    'nong', 'nou', 'nu', 'nuan', 'nue', 'nun', 'nuo', 'nv', 'nve', 'nü', 'nüe', 'ou',
    'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen', 'peng',
    'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu',
    'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie',
    'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun',
    'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou',
    'ru', 'rua', 'ruan', 'rui', 'run', 'ruo',
    'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sei', 'sen', 'seng',
    'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi',
    'shong', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo',
    'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo',
    'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'tei', 'teng',
    'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou',
    'tu', 'tuan', 'tui', 'tun', 'tuo',
    'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu',
    'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun',
    'ya', 'yai', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin', 'ying',
    'yo', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun',
    'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng',
    'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng',
    'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo',
    'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo', 'ê'
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

        for prefix, length in prefix_matches:
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
