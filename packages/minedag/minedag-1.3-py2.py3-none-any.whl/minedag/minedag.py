from collections import defaultdict, deque
from typing import Generic, Hashable, TypeVar

T = TypeVar('T', bound=Hashable)


class MineDag(Generic[T]):
    def __init__(self) -> None:
        # src -> set[dst]
        self._src_dst_map = defaultdict(set)  # type: dict[T, set[T]]
        # dst -> set[src]
        self._dst_src_map = defaultdict(set)  # type: dict[T, set[T]]

        # (src, dst) -> float
        self._weights = {}  # type: dict[tuple[T, T], float]

    def add_node(self, obj: T) -> None:
        if obj not in self._src_dst_map:
            self._src_dst_map[obj] = set()

        if obj not in self._dst_src_map:
            self._dst_src_map[obj] = set()

    def add_edge(self, src: T, dst: T, weight: float = 1) -> None:
        if src in self._src_dst_map[dst] or dst in self._dst_src_map[src]:
            raise ValueError('got circle: {src} -> {dst}')

        self._src_dst_map[src].add(dst)
        self._dst_src_map[dst].add(src)
        self._weights[(src, dst)] = weight

    def get_all_roots(self) -> set[T]:
        """
        get all nodes without edges in them
        """
        return {
            obj
            for obj in self._src_dst_map
            if len(self._dst_src_map[obj]) == 0
        }

    def get_leaves(self) -> set[T]:
        """
        get all nodes without edges from them
        """
        return {
            dst
            for dst in self._dst_src_map
            if len(self._src_dst_map[dst]) == 0
        }

    def _get_all_srcs(self, obj: T) -> set[T]:
        result = set()
        queue = deque()  # type: deque[T]
        queue.append(obj)
        while len(queue) > 0:
            _obj = queue.popleft()
            for _src in self._dst_src_map[_obj]:
                queue.append(_src)
                result.add(_src)

        return result

    def get_all_srcs(self, obj: T) -> list[T]:
        """
        return up flow in topological order
        """
        result = []  # type: list[T]
        in_result = set()  # type: set[T]

        _left_for_result = self._get_all_srcs(obj)

        _depencies_cached = defaultdict(set)  # type: dict[T, set[T]]

        while len(_left_for_result) > 0:
            for _obj in list(_left_for_result):

                if _obj not in _depencies_cached:
                    _depencies_cached[_obj] = self._get_all_srcs(_obj)

                depencies = _depencies_cached[_obj]
                if len(depencies - in_result) == 0:
                    if _obj not in in_result:
                        result.append(_obj)
                        in_result.add(_obj)
                    _left_for_result.remove(_obj)

        return result[::-1]

    def _get_all_depencies(self, obj: T) -> set[T]:
        result = set()
        queue = deque()  # type: deque[T]
        queue.append(obj)
        while len(queue) > 0:
            _obj = queue.popleft()
            for _dst in self._src_dst_map[_obj]:
                queue.append(_dst)
                result.add(_dst)

        return result

    def get_all_dsts(self, obj: T) -> list[T]:
        """
        return down flow in topological order
        """

        result = []  # type: list[T]
        in_result = set()  # type: set[T]

        _left_for_result = self._get_all_depencies(obj)

        _depencies_cached = defaultdict(set)  # type: dict[T, set[T]]

        while len(_left_for_result) > 0:
            for _obj in list(_left_for_result):

                if _obj not in _depencies_cached:
                    _depencies_cached[_obj] = self._get_all_depencies(_obj)

                depencies = _depencies_cached[_obj]
                if len(depencies - in_result) == 0:
                    if _obj not in in_result:
                        result.append(_obj)
                        in_result.add(_obj)
                    _left_for_result.remove(_obj)

        return result[::-1]

    def find_shortest_way_to_any_leaf(self, obj: T) -> tuple[float, list[T]]:
        obj_leaves = self.get_leaves() & set(self.get_all_dsts(obj))
        if not obj_leaves:
            return 0, []
        way_map = self._build_way_map(obj, min_way=True)
        return min((way_map[leaf] for leaf in obj_leaves), key=lambda x: x[0])

    def find_shortest_way_to_farthest_leaf(self, obj: T) -> tuple[float, list[T]]:
        obj_leaves = self.get_leaves() & set(self.get_all_dsts(obj))
        if not obj_leaves:
            return 0, []
        way_map = self._build_way_map(obj, min_way=True)
        return max((way_map[leaf] for leaf in obj_leaves), key=lambda x: x[0])

    def find_longest_way_to_any_leaf(self, obj: T) -> tuple[float, list[T]]:
        obj_leaves = self.get_leaves() & set(self.get_all_dsts(obj))
        if not obj_leaves:
            return 0, []
        way_map = self._build_way_map(obj, min_way=False)
        return max((way_map[leaf] for leaf in obj_leaves), key=lambda x: x[0])

    def find_longest_way_to_farthest_leaf(self, obj: T) -> tuple[float, list[T]]:
        obj_leaves = self.get_leaves() & set(self.get_all_dsts(obj))
        if not obj_leaves:
            return 0, []
        way_map = self._build_way_map(obj, min_way=False)
        return max((way_map[leaf] for leaf in obj_leaves), key=lambda x: x[0])

    def _build_way_map(self, obj: T, min_way: bool = True) -> dict[T, tuple[float, list[T]]]:
        comp_func = min if min_way else max

        count_map = {}  # type: dict[T, tuple[float, list[T]]]
        for _obj in self.get_all_dsts(obj):
            candidates = []

            for src in self._dst_src_map[_obj]:
                if src in count_map:
                    weight, way = count_map[src]
                else:
                    weight, way = 0, list()

                weight = weight + self._weights[(src, _obj)]
                way = list(way)
                way.append(_obj)
                candidates.append((weight, way))

            count_map[_obj] = comp_func(candidates, key=lambda x: x[0])

        return count_map

    def get_reachable(self, objs: set[T]) -> set[T]:
        """
        pass as params set of nodes, u have already reached,
        method will return layer; layer contains objects, u can reach on next iteration
        """
        in_result = set(objs)  # type: set[T]

        next_lvl = set()

        for dst, srcs in self._dst_src_map.items():
            if dst not in in_result:
                if (srcs & in_result) and len(srcs - in_result) == 0:
                    next_lvl.add(dst)

        return next_lvl

    def get_layer_iterations(self, objs: set[T]) -> list[set[T]]:
        """
        pass as params set of nodes, u have already reached,
        method will return list of layers; each layer contains objects, u can reach on i's iteration
        """
        result = [set(objs)]  # type: list[set[T]]
        in_result = set(objs)  # type: set[T]

        while next_lvl := self.get_reachable(in_result):
            result.append(next_lvl)
            in_result.update(next_lvl)
        return result
