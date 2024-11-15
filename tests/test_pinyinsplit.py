from pinyin_split import split


def test_basic_splits():
    """Test basic pinyin splitting cases"""
    assert split("nihao") == [["ni", "hao"]]
    assert split("beijing") == [["bei", "jing"]]
    assert split("zhongguo") == [["zhong", "guo"]]


def test_single_syllables():
    """Test single syllable cases"""
    assert split("a") == [["a"]]
    assert split("ai") == [["ai"]]
    assert split("an") == [["an"]]


def test_ambiguous_splits():
    """Test cases where multiple valid splits are possible"""
    assert sorted(split("xian")) == sorted([["xi", "an"], ["xian"]])
    assert sorted(split("yingying")) == sorted([["ying", "ying"]])


def test_case_sensitivity():
    """Test that splitting works regardless of case"""
    # The current implementation preserves case
    assert split("NIHAO") == [["ni", "hao"]]
    assert split("BeIJinG") == [["bei", "jing"]]
    assert split("ZhongGuo") == [["zhong", "guo"]]


def test_edge_cases():
    """Test edge cases and invalid inputs"""
    assert split("") == []
    assert split(" ") == []
    assert split("x") == []  # Single consonant isn't valid pinyin
    assert split("abc") == []  # Invalid pinyin sequence


def test_complex_combinations():
    """Test more complex and challenging combinations"""
    assert sorted(split("zhongguoren")) == sorted([["zhong", "guo", "ren"]])
    assert sorted(split("meiguoxing")) == sorted([["mei", "guo", "xing"]])
    # The current implementation finds multiple valid splits
    assert sorted(split("xiaolongbao")) == sorted(
        [["xiao", "long", "bao"], ["xi", "ao", "long", "bao"]]
    )


def test_special_syllables():
    """Test special pinyin syllables and combinations"""
    # The current implementation finds all valid splits
    assert sorted(split("lüe")) == sorted([["lüe"], ["lü", "e"]])
    assert sorted(split("lue")) == sorted([["lue"], ["lu", "e"]])
    assert sorted(split("nüe")) == sorted([["nüe"], ["nü", "e"]])
    assert sorted(split("nue")) == sorted([["nue"], ["nu", "e"]])


def test_overlapping_possibilities():
    """Test cases where syllables could overlap"""
    # The current implementation finds all valid splits
    assert sorted(split("shangai")) == sorted([["shang", "ai"], ["shan", "gai"]])
    assert sorted(split("haixian")) == sorted([["hai", "xian"], ["hai", "xi", "an"]])
