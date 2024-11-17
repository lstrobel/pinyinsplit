from pinyin_split import split


def test_basic_splits():
    """Test basic pinyin splitting cases"""
    assert split("mingzi") == [["ming", "zi"]]
    assert split("Zhongguo") == [
        ["Zhong", "guo"],
        ["Zhong", "gu", "o"],
    ]  # Strangely correct behavior


def test_single_syllables():
    """Test single syllable cases"""
    assert split("a") == [["a"]]
    assert split("ai") == [["ai"]]
    assert split("jiong") == [["jiong"]]


def test_ambiguous_splits():
    """Test cases where multiple valid splits are possible"""
    assert sorted(split("xian")) == sorted([["xi", "an"], ["xian"]])
    assert sorted(split("yingying")) == sorted([["ying", "ying"]])


def test_case_sensitivity():
    """Test that splitting preserves original case"""
    assert split("NIHaO") == [["NI", "HaO"], ["NI", "Ha", "O"]]
    assert split("BeIJinG") == [["BeI", "JinG"]]
    assert split("kaiCHE") == [["kai", "CHE"]]


def test_edge_cases():
    """Test edge cases and invalid inputs"""
    assert split("") == []
    assert split(" ") == []
    assert split("x") == []  # Single consonant isn't valid pinyin
    assert split("abc") == []  # Invalid pinyin sequence


def test_complex_combinations():
    """Test more complex and challenging combinations"""
    assert sorted(split("meiguanxi")) == sorted(
        [["mei", "guan", "xi"], ["mei", "gu", "an", "xi"]]
    )
    # The current implementation finds multiple valid splits
    assert sorted(split("xiaolongbao")) == sorted(
        [
            ["xiao", "long", "bao"],
            ["xi", "ao", "long", "bao"],
            ["xia", "o", "long", "bao"],
            ["xi", "a", "o", "long", "bao"],
            ["xiao", "long", "ba", "o"],
            ["xi", "ao", "long", "ba", "o"],
            ["xia", "o", "long", "ba", "o"],
            ["xi", "a", "o", "long", "ba", "o"],
        ]
    )


def test_special_syllables():
    """Test special pinyin syllables and combinations"""
    # The current implementation finds all valid splits
    assert sorted(split("lüe")) == sorted([["lüe"], ["lü", "e"]])
    assert sorted(split("nüe")) == sorted([["nüe"], ["nü", "e"]])


def test_rare_syllables():
    """Test rare/non-standard syllables with include_rare parameter"""
    # Should not match rare syllables by default
    assert split("zhei") == []
    assert split("duang") == [["du", "ang"]]

    # Should match rare syllables when include_rare=True
    assert split("zhei", include_nonstandard=True) == [["zhei"]]
    assert sorted(split("duang", include_nonstandard=True)) == sorted(
        [["du", "ang"], ["duang"]]
    )


def test_overlapping_possibilities():
    """Test cases where syllables could overlap"""
    # The current implementation finds all valid splits
    assert sorted(split("shangai")) == sorted([["shang", "ai"], ["shan", "gai"]])
    assert sorted(split("haixian")) == sorted([["hai", "xian"], ["hai", "xi", "an"]])
