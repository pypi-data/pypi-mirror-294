
import pytest

from minedag import MineDag


@pytest.fixture(scope='function')
def dag_1():
    r"""
        1      9     11   12         13
       / \     |              w2->  /  \  <- w3
      2   3    10                  14   15
w3->  | / |
      4   | <- w5
w2->  | \ |
      5   6
      \  /
       7
       |
       8
    """
    dag = MineDag()
    dag.add_edge(1, 2)
    dag.add_edge(1, 3)
    dag.add_edge(2, 4, weight=3)
    dag.add_edge(3, 4)
    dag.add_edge(4, 5, weight=2)
    dag.add_edge(3, 6, weight=5)
    dag.add_edge(4, 6)
    dag.add_edge(5, 7)
    dag.add_edge(6, 7)
    dag.add_edge(7, 8)
    dag.add_edge(9, 10)

    dag.add_edge(13, 14, weight=2)
    dag.add_edge(13, 15, weight=3)

    dag.add_node(11)
    dag.add_node(12)
    return dag
