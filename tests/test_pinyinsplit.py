import pytest

from py_pinyin_split import PinyinTokenizer


def test_benchmark_simple(benchmark):
    tokenizer = PinyinTokenizer()
    result = benchmark(tokenizer.tokenize, "xīnniánkuàilè")
    assert result == ["xīn", "nián", "kuài", "lè"]


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


def test_difficult_tone_splits():
    tokenizer = PinyinTokenizer()

    # Frequency matters
    assert tokenizer.tokenize("kěnéng") == ["kě", "néng"]
    assert tokenizer.tokenize("dàngāo") == ["dàn", "gāo"]
    assert tokenizer.tokenize("bàngōngshì") == ["bàn", "gōng", "shì"]

    # Vowel matters
    assert tokenizer.tokenize("rènào") == ["rè", "nào"]
    assert tokenizer.tokenize("shēngāo") == ["shēn", "gāo"]
    assert tokenizer.tokenize("qīněr") == ["qīn", "ěr"]

    # Test that tones help resolve ambiguity
    assert tokenizer.tokenize("xīan") == ["xī", "an"]
    assert tokenizer.tokenize("xián") == ["xián"]

    # Test apostrophe handling
    assert tokenizer.tokenize("Xī'ān") == ["Xī", "'", "ān"]
    assert tokenizer.tokenize("yī'er") == ["yī", "'", "er"]
    assert tokenizer.tokenize("wǎn'ān") == ["wǎn", "'", "ān"]


def test_invalid_pinyin():
    """Inputs with invalid pinyin throw ValueErrors"""
    tokenizer = PinyinTokenizer()

    # Single consonant should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("x")

    # Invalid pinyin should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("english")

    # Unsupported pinyin should raise ValueError
    with pytest.raises(ValueError):
        tokenizer.tokenize("ni3hao3")


def test_text_with_whitespace():
    """Test handling of longer text with whitespace"""
    tokenizer = PinyinTokenizer()

    # Simple whitespace
    assert tokenizer.tokenize("nǐ hǎo") == ["nǐ", "hǎo"]

    # Multiple words with mixed tones
    assert tokenizer.tokenize("Wǒ hěn xǐhuān Zhōngguó") == [
        "Wǒ",
        "hěn",
        "xǐ",
        "huān",
        "Zhōng",
        "guó",
    ]

    # Leading/trailing whitespace
    assert tokenizer.tokenize("  nǐ hǎo  ") == ["nǐ", "hǎo"]

    # Multiple whitespace characters
    assert tokenizer.tokenize("nǐ  hǎo\t\nma") == ["nǐ", "hǎo", "ma"]


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
