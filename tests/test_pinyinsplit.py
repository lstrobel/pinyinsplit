from pinyin_split import split


def test_basic_splits():
    """Test basic pinyin splitting functionality"""
    assert split("nihao") == [["ni", "hao"], ["ni", "ha", "o"]]
    assert split("zhongguo") == [["zhong", "guo"], ["zhong", "gu", "o"]]
    assert split("BeijingDaxue") == [
        ["Bei", "jing", "Da", "xue"],
        ["Bei", "jing", "Da", "xu", "e"],
    ]


def test_tone_marks():
    """Test handling of tone marks"""
    assert split("nǐhǎo") == [["nǐ", "hǎo"], ["nǐ", "hǎ", "o"]]
    assert split("Běijīng") == [["Běi", "jīng"]]
    assert split("wǒmen") == [["wǒ", "men"]]
    assert split("lǜsè") == [["lǜ", "sè"]]


def test_edge_cases():
    """Test edge cases and invalid inputs"""
    assert split("") == []
    assert split(" ") == []
    assert split("x") == []  # Single consonant
    assert split("abc") == []  # Invalid pinyin
    assert split("zhei") == []  # Non-standard syllable
    assert split("zhei", include_nonstandard=True) == [
        ["zhei"]
    ]  # With non-standard enabled


def test_ambiguous_splits():
    """Test cases with multiple valid splits"""
    assert sorted(split("xian")) == sorted([["xi", "an"], ["xian"]])
    assert sorted(split("shangai")) == sorted([["shang", "ai"], ["shan", "gai"]])


def test_long_text():
    """Test a longer text string"""
    text = "Jiéguǒtāmenyíngle."  # 結果他們贏了。
    expected = [
        ["Jié", "guǒ", "tā", "men", "yíng", "le"],
        ["Jié", "gu", "ǒ", "tā", "men", "yíng", "le"],
        ["Ji", "é", "guǒ", "tā", "men", "yíng", "le"],
        ["Ji", "é", "gu", "ǒ", "tā", "men", "yíng", "le"],
    ]
    assert split(text) == expected


def test_punctuation_and_numbers():
    """Test handling of punctuation and numbers as boundaries"""
    assert split("xi'an") == [["xi", "an"]]
    assert split("bei3jing1") == [["bei", "jing"]]
    assert split("zhong1-guo2") == [["zhong", "guo"], ["zhong", "gu", "o"]]
    assert split("ni3,wo3") == [["ni", "wo"]]


def test_erhua():
    """Test handling of erhua"""
    assert split("yidianr") == []  # Flag not enabled
    assert split("yidianr", include_erhua=True) == [
        ["yi", "dian", "r"],
        ["yi", "di", "an", "r"],
    ]
