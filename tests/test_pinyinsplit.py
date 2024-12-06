import pytest  # type: ignore
from pinyin_split.pinyinsplit import PinyinTokenizer


def test_no_tone_splits():
    """We can split pinyin without tones"""
    tokenizer = PinyinTokenizer()
    assert tokenizer.tokenize("nihao") == ["ni", "hao"]
    assert tokenizer.tokenize("zhongguo") == ["zhong", "guo"]
    assert tokenizer.tokenize("beijing") == ["bei", "jing"]


def test_tone_splits():
    """Test handling of tone marks"""
    tokenizer = PinyinTokenizer()
    assert tokenizer.tokenize("nǐhǎo") == ["nǐ", "hǎo"]
    assert tokenizer.tokenize("Běijīng") == ["Běi", "jīng"]
    assert tokenizer.tokenize("WǑMEN") == ["WǑ", "MEN"]
    assert tokenizer.tokenize("lǜsè") == ["lǜ", "sè"]
    assert tokenizer.tokenize("lvse") == ["lv", "se"]
    assert tokenizer.tokenize("xīnniánkuàilè") == ["xīn", "nián", "kuài", "lè"]
    assert tokenizer.tokenize("màn") == ["màn"]


def test_edge_cases():
    """Test edge cases and invalid inputs"""
    tokenizer = PinyinTokenizer()

    # Empty string should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("")

    # Invalid characters should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("hello!")

    # Single consonant should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("x")

    # Invalid pinyin should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("english")

    # Unsupported pinyin should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("ni3hao3")


def test_nonstandard_syllables():
    """Test handling of non-standard syllables"""
    standard_tokenizer = PinyinTokenizer(include_nonstandard=False)
    nonstandard_tokenizer = PinyinTokenizer(include_nonstandard=True)

    # Should fail with standard tokenizer
    with pytest.raises(ValueError):
        standard_tokenizer.tokenize("zhèige")

    # Should work with non-standard tokenizer
    assert nonstandard_tokenizer.tokenize("zhèige") == ["zhèi", "ge"]


def test_span_tokenize():
    """Test span_tokenize method returns correct character indices"""
    tokenizer = PinyinTokenizer()

    # Basic case
    assert list(tokenizer.span_tokenize("nihao")) == [(0, 2), (2, 5)]

    # With tone marks
    assert list(tokenizer.span_tokenize("nǐhǎo")) == [(0, 2), (2, 5)]

    # Mixed case
    assert list(tokenizer.span_tokenize("NiHao")) == [(0, 2), (2, 5)]

    # Multi-character syllables
    assert list(tokenizer.span_tokenize("zhōngguó")) == [(0, 5), (5, 8)]

    # Test preservation of original text slices
    text = "Nǐhǎo"
    spans = list(tokenizer.span_tokenize(text))
    assert [text[start:end] for start, end in spans] == ["Nǐ", "hǎo"]


def test_erhua():
    """Test handling of erhua"""
    tokenizer = PinyinTokenizer()

    # Test standalone er syllable
    assert tokenizer.tokenize("er") == ["er"]
    assert tokenizer.tokenize("ér") == ["ér"]

    # Test common erhua words
    assert tokenizer.tokenize("erzi") == ["er", "zi"]
    assert tokenizer.tokenize("yidiǎnr") == ["yi", "diǎn", "r"]
    assert tokenizer.tokenize("wánr") == ["wán", "r"]


def test_ambiguous_splits():
    """Test handling of ambiguous syllable boundaries"""
    tokenizer = PinyinTokenizer()

    # Test cases where multiple valid splits exist
    # Should use frequency data to pick most likely split
    assert tokenizer.tokenize("wǎnān") == ["wǎn", "ān"]  # Not wa nan
    assert tokenizer.tokenize("xian") == ["xian"]  # Not xi an

    # Test that tones help resolve ambiguity
    assert tokenizer.tokenize("xīan") == ["xī", "an"]
    assert tokenizer.tokenize("xián") == ["xián"]
