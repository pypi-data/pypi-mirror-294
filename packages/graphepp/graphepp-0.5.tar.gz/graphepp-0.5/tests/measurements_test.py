""" Unittest File for verification of the Pauli measurements

"""


import graphepp as gg


def test_PauliZ():
    test_state = gg.Graph(3, ((0, 1), (1, 0), (1, 2), (2, 0)))
    test_state_expectation = gg.Graph(3, ((2, 0),))
    test_state_measured = gg.measure_Z(test_state, n=1)

    assert test_state_measured == test_state_expectation


def test_PauliY():
    test_state = gg.Graph(3, ((0, 1), (1, 0), (1, 2), (2, 0)))
    test_state_expectation = gg.Graph(3, ((),))
    test_state_measured = gg.measure_Y(test_state, n=1)

    assert test_state_measured == test_state_expectation


def test_PauliX():
    test_state = gg.Graph(5, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 3)))
    test_state_expectation = gg.Graph(5, ((1, 3), (0, 3), (3, 4), (0, 4)))
    test_state_expectation_2 = gg.Graph(5, ((0, 3), (0, 4), (1, 3), (3, 4)))

    test_state_measured = gg.measure_X(test_state, n=2, neighbor=1)

    test_state_measured_no_neighbor = gg.measure_X(test_state, n=2)

    gg.measure_X(test_state, n=2)

    assert test_state_measured == test_state_expectation
    assert (
        test_state_measured_no_neighbor == test_state_expectation
        or test_state_measured_no_neighbor == test_state_expectation_2
    )
