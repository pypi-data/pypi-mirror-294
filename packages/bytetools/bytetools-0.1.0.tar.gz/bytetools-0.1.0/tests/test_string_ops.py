import pytest

from bytetools import (
    InvalidByteValue,
    lower,
)


class TestByteOperations:
    def test_lower_basic_values(self):
        assert lower(0x41) == 0x61  # 'A' -> 'a'
        assert lower(0x5A) == 0x7A  # 'Z' -> 'z'
        assert lower(0x30) == 0x30  # '0' remains '0'

    def test_lower_indexing_bytearrays(self):
        test_array = bytearray(b"HeLLo, WorlD!")
        assert lower(test_array[0]) == 0x68
        assert lower(test_array[1]) == 0x65
        assert lower(test_array[5]) == 0x2c
        assert lower(test_array[6]) == 0x20
        assert lower(test_array[-1]) == 0x21
        assert lower(test_array[-2]) == 0x64

    def test_lower_indexing_bytearrays(self):
        with pytest.raises(InvalidByteValue):
            lower(256)
