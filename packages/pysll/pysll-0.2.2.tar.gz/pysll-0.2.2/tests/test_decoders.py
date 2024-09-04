import os

import pytest

from pysll.decoders import decode


@pytest.fixture(params=["on", "off"])
def _use_numpy(request):
    os.environ["PYSLL_USE_NUMPY"] = request.param
    yield
    del os.environ["PYSLL_USE_NUMPY"]


@pytest.mark.parametrize(
    "encoded,decoded",
    [
        # fmt:off
        ("1:eJxTTMoPymQAAgALRAGu", "0"),
        ("1:eJxTTMoPymRhYGAAAAtUAbI=", "4"),
        ("1:eJxTTMoPytRiYGAAAAvsAdg=", "42"),
        ("1:eJxTTMoP8pRlYGCwNDA2sTC1NLAAUpYGpiAukLIwMLawNDEFAJVXB6k=", "90348590834890590349058038945"),
        ("1:eJxTTMoPKmIAAwEHABKtAgc=", "4.0"),
        ("1:eJxTTMoPKlLeX9fBW8btAAAgJgRt", "3.432643"),
        ("1:eJxTTMoPCuZkYGDwyFQIyUgtSlUEACgoBIs=", "Hi There!"),
        ("1:eJxTTMoPSmMAgmIWIOGTWVwCACIoA74=", "List[]"),
        ("1:eJxTTMoPKmZlYGDwyU/PzAMAGegDtg==", "Login"),
        ("1:eJxTTMoPSmMAgmIWIOGTWVwCACIoA74=", "List[]"),
        ("1:eJxTTMoPSmNiYGAoZgESPpnFJZmMQEYmSAgATfoElQ==", "List[1, 2]"),
        ("1:eJxTTMoPCoplYGAwNDLWA2IgMjE2MTQyAhEIDEFwHrI4ggljJZgb6xlYGhgbW5oZmRgbGpgYAQAiwxSF", "123.12312343412233"),
        (
            "1:eJxNwakBgDAQBMC0Qgeb3O0Tj8FSAg3Qv8MyczzvfZ1jjEDMNKexu+LQU4JKoRplaZsrm2A3klp2VuPnA2uVD6k=",
            "80658175170943878571660636856403766975289505440883277824000000000000"
        ),
        ("1:eJxTTMoPCmZlYGAw1jM0SQAAFg0Cww==", "3.14`"),
        ("1:eJxTTMoPCmZnYGAw1jM0STA0AAAcOwMm", "3.14`10"),
        ("1:eJxTTMoPSmNkYGAoZgESHvk5KRAeJ5BwS0wuyS/KTMzJNAHyALLoCL8=", "Hold[Factorial[52]]"),
        ("1:eJxTTMoPCmZlYGDISM3JyQcAGSIDsQ==", "hello"),
        ("1:eJxTTMoPKmZlYGDISM3JyQcAGmID0Q==", "hello"),  # sus, this is the symbol...
        ("1:eJxTTMoPKmZhYGDwSE1MAQAV6wMu", "Head"),
        ("1:eJxTTMoPCmZhYGDwSE1MAQAUywMO", "Head"),
        ("1:eJxTTMoPSmNmYGAoZgESPpnFJZmMQEYmE4gAiQMAZxgFAg==", "List[1, 2, 3]"),
        ("1:eJxTTMoPSmNkYGAoZgESPpnFJWnMyLxMkFwmE5Aokm99HbhDjtMBAPuoCoE=", "List[List[1, 2, 3.14]]"),
        (
            "1:eJxTTMoPSmNhYGAo5gYSwQWJRcWpjkVFiZXFnEC+Y2lJfm5iSWZyGhNICUidT2ZxiScjkGEMITOBBEMaM7J0JkgCVQfEChT9BmDSCMksE1RVaYwYegyxiBljETPCqg7TDYYQe5FdAgCqsisv",  # noqa: E501
            "SparseArray[Automatic, List[3, 3], 0, List[1, List[List[0, 2, 3, 4], List[List[1], List[3], List[2], List[3]]], List[1, 4, 2, 3]]]"  # noqa: E501
        ),
        ("1:eJxTTMoPSmNkYGAo5gYSjsXF+cmZiSWZ+XlpTCBBFiARVJqTWswMZKTl54PppMQiAF7SDIM=", "Association[Rule[foo, bar]]"),
        ("1:eJxTTMoPCmJnYGAw0jNMMDTSAwAcSwMg", "2.1"),
        (
            "1:eJxTTMoPSmNkYGAo5gUSgaWJeSWZJZWORUWJlWlMIGE5IBFcUlSaXFJalJoClkhA8F0SSxIh6liAhE9mcYknyDAjMGmcxowsg6oOVQ6s3hC3XrCYCZg0BZNmwewgh6Um5+elFKOZzIjMywTx0IRAygHNhzCH",  # noqa: E501
            "QuantityArray[StructuredArray`StructuredData[List[2, 3], List[List[List[1, 2, 3], List[4, 5, 6]], Seconds, List[List[1], List[2]]]]]"  # noqa: E501
        )
        # fmt:on
    ],
)
def test_decode(_use_numpy, encoded, decoded):
    assert decode(encoded) == decoded


def test_large_matrix_decoder():
    """Large matrices of real numbers get compresed into a special format,
    which we test here."""
    with open("tests/decompress-large-matrix.dat", "r") as handle:
        decoded = decode(handle.read())

    from pysll.models import VariableUnitValue

    parsed = VariableUnitValue.parse_mathematica_expression(decoded)

    assert len(parsed) == 361

    first, last = parsed[0], parsed[-1]

    x, y = first
    assert (x.value, x.unit) == (0.0, "Minutes")
    assert (y.value, y.unit) == (-87.528984, "IndependentUnit[Lsus]")

    x, y = last
    assert (x.value, x.unit) == (6.0, "Minutes")
    assert (y.value, y.unit) == (1009.098328, "IndependentUnit[Lsus]")
