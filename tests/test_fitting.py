#!/usr/bin/python

from trap_dc import fitting

def test_linearindex():
    lidx = fitting.LinearIndices((2,))
    assert len(lidx) == 2
    assert lidx[0] == 0
    assert lidx[1] == 1
    assert list(lidx) == [0, 1]
    assert list(reversed(lidx)) == [1, 0]

    lidx = fitting.LinearIndices((2, 4))
    assert len(lidx) == 8
    for i in range(8):
        assert lidx[i] == i
    for i in range(2):
        for j in range(4):
            assert lidx[i, j] == i * 4 + j
    assert list(lidx) == list(range(8))
    assert list(reversed(lidx)) == list(reversed(range(8)))

    lidx = fitting.LinearIndices((2, 3, 4))
    assert len(lidx) == 24
    for i in range(24):
        assert lidx[i] == i
    for i in range(2):
        for j in range(3):
            for k in range(4):
                assert lidx[i, j, k] == i * 3 * 4 + j * 4 + k
    assert list(lidx) == list(range(24))
    assert list(reversed(lidx)) == list(reversed(range(24)))

def test_cartesianindex():
    cidx = fitting.CartesianIndices((2,))
    assert len(cidx) == 2
    assert cidx[0] == (0,)
    assert cidx[1] == (1,)
    assert list(cidx) == [(0,), (1,)]
    assert list(reversed(cidx)) == [(1,), (0,)]

    cidx = fitting.CartesianIndices((2, 4))
    assert len(cidx) == 8
    expected = []
    for i in range(2):
        for j in range(4):
            expected.append((i, j))
            assert cidx[i * 4 + j] == (i, j)
            assert cidx[i, j] == (i, j)
    assert list(cidx) == expected
    assert list(reversed(cidx)) == list(reversed(expected))

    cidx = fitting.CartesianIndices((2, 3, 4))
    assert len(cidx) == 24
    expected = []
    for i in range(2):
        for j in range(3):
            for k in range(4):
                expected.append((i, j, k))
                assert cidx[i * 3 * 4 + j * 4 + k] == (i, j, k)
                assert cidx[i, j, k] == (i, j, k)
    assert list(cidx) == expected
    assert list(reversed(cidx)) == list(reversed(expected))
