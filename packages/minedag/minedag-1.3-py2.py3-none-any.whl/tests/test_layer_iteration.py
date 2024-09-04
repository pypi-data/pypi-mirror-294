

def test_get_reachable(dag_1):
    assert dag_1.get_reachable({1}) == {2, 3}
    assert dag_1.get_reachable({2}) == set()
    assert dag_1.get_reachable({3}) == set()
    assert dag_1.get_reachable({2, 3}) == {4}
    assert dag_1.get_reachable({1, 5, 6}) == {2, 3, 7}


def test_layer_iteration(dag_1):
    assert dag_1.get_layer_iterations({1}) == [{1}, {2, 3}, {4}, {5, 6}, {7}, {8}]
    assert dag_1.get_layer_iterations({2, 3}) == [{2, 3}, {4}, {5, 6}, {7}, {8}]
    assert dag_1.get_layer_iterations({4, 3}) == [{3, 4}, {5, 6}, {7}, {8}]
    assert dag_1.get_layer_iterations({1, 13}) == [{1, 13}, {2, 3, 14, 15}, {4}, {5, 6}, {7}, {8}]
