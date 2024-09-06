import collections
import itertools
from functools import partial
from typing import List, Tuple, Dict, Callable, Optional, Sequence, TextIO

import numpy as np
import torch
from numpy.typing import ArrayLike
from torch.nn import Module


class Hierarchy:
    """Hierarchy of nodes 0, ..., n-1."""

    def __init__(self, parents):
        n = len(parents)
        assert np.all(parents[1:] < np.arange(1, n))
        self._parents = parents

    def num_nodes(self) -> int:
        return len(self._parents)

    def edges(self) -> List[Tuple[int, int]]:
        return list(zip(self._parents[1:], itertools.count(1)))

    def parents(self, root_loop: bool = False) -> np.ndarray:
        if root_loop:
            return np.where(
                self._parents >= 0, self._parents, np.arange(len(self._parents))
            )
        else:
            return np.array(self._parents)

    def children(self) -> Dict[int, np.ndarray]:
        result = collections.defaultdict(list)
        for i, j in self.edges():
            result[i].append(j)
        return {k: np.array(v, dtype=int) for k, v in result.items()}

    def num_children(self) -> np.ndarray:
        n = len(self._parents)
        unique, counts = np.unique(self._parents[1:], return_counts=True)
        result = np.zeros([n], dtype=int)
        result[unique] = counts
        return result

    def leaf_mask(self) -> np.ndarray:
        return self.num_children() == 0

    def leaf_subset(self) -> np.ndarray:
        (index,) = self.leaf_mask().nonzero()
        return index

    def internal_subset(self) -> np.ndarray:
        (index,) = np.logical_not(self.leaf_mask()).nonzero()
        return index

    def num_leaf_nodes(self) -> int:
        return np.count_nonzero(self.leaf_mask())

    def num_internal_nodes(self) -> int:
        return np.count_nonzero(np.logical_not(self.leaf_mask()))

    def num_conditionals(self) -> int:
        return np.count_nonzero(self.num_children() > 1)

    def depths(self) -> np.ndarray:
        # n = len(self._parents)
        # d = np.zeros([n], dtype=int)
        # for i, j in self.edges():
        #     assert i < j, 'require edges in topological order'
        #     d[j] = d[i] + 1
        # return d
        return self.accumulate_ancestors(np.add, (self._parents >= 0).astype(int))

    def num_leaf_descendants(self) -> np.ndarray:
        # c = self.leaf_mask().astype(int)
        # for i, j in reversed(self.edges()):
        #     assert i < j, 'require edges in topological order'
        #     c[i] += c[j]
        # return c
        return self.accumulate_descendants(np.add, self.leaf_mask().astype(int))

    def max_heights(self) -> np.ndarray:
        heights = np.zeros_like(self.depths())
        # for i, j in reversed(self.edges()):
        #     heights[i] = max(heights[i], heights[j] + 1)
        # return heights
        return self.accumulate_descendants(lambda u, v: max(u, v + 1), heights)

    def min_heights(self) -> np.ndarray:
        # Initialize leaf nodes to zero, internal nodes to upper bound.
        #   height + depth <= max_depth
        #   height <= max_depth - depth
        depths = self.depths()
        heights = np.where(self.leaf_mask(), 0, depths.max() - depths)
        # for i, j in reversed(self.edges()):
        #     heights[i] = min(heights[i], heights[j] + 1)
        # return heights
        return self.accumulate_descendants(lambda u, v: min(u, v + 1), heights)

    # def accumulate_ancestors_inplace(self, func: Callable, values: MutableSequence):
    #     # Start from root and move down.
    #     for i, j in self.edges():
    #         values[j] = func(values[i], values[j])

    # def accumulate_descendants_inplace(self, func: Callable, values: MutableSequence):
    #     # Start from leaves and move up.
    #     for i, j in reversed(self.edges()):
    #         values[i] = func(values[i], values[j])

    def accumulate_ancestors(self, func: Callable, values: ArrayLike) -> np.ndarray:
        # Start from root and move down.
        partials = np.array(values)
        for i, j in self.edges():
            partials[j] = func(partials[i], partials[j])
        return partials

    def accumulate_descendants(self, func: Callable, values: ArrayLike) -> np.ndarray:
        # Start from leaves and move up.
        partials = np.array(values)
        for i, j in reversed(self.edges()):
            partials[i] = func(partials[i], partials[j])
        return partials

    def ancestor_mask(self, strict=False) -> np.ndarray:
        n = len(self._parents)
        # If path exists i, ..., j then i < j and is_ancestor[i, j] is True.
        # Work with is_descendant instead to use consecutive blocks of memory.
        # Note that is_ancestor[i, j] == is_descendant[j, i].
        is_descendant = np.zeros([n, n], dtype=bool)
        if not strict:
            is_descendant[0, 0] = 1
        for i, j in self.edges():
            # Node i is parent of node j.
            assert i < j, "require edges in topological order"
            is_descendant[j, :] = is_descendant[i, :]
            if strict:
                is_descendant[j, i] = 1
            else:
                is_descendant[j, j] = 1
        is_ancestor = is_descendant.T
        return is_ancestor

    def paths(
        self,
        exclude_root: bool = False,
        exclude_self: bool = False,
    ) -> List[np.ndarray]:
        # TODO: Could avoid potential high memory usage here using parents.
        is_descendant = self.ancestor_mask(strict=exclude_self).T
        if exclude_root:
            paths = [np.flatnonzero(mask) + 1 for mask in is_descendant[:, 1:]]
        else:
            paths = [np.flatnonzero(mask) for mask in is_descendant]
        return paths

    def paths_padded(
        self, pad_value=-1, method: str = "constant", **kwargs
    ) -> np.ndarray:
        n = self.num_nodes()
        paths = self.paths(**kwargs)
        path_lens = list(map(len, paths))
        max_len = max(path_lens)
        if method == "constant":
            padded = np.full((n, max_len), pad_value, dtype=int)
        elif method == "self":
            padded = np.tile(np.arange(n)[:, None], max_len)
        else:
            raise ValueError("unknown pad method", method)
        row_index = np.concatenate([np.full(n, i) for i, n in enumerate(path_lens)])
        col_index = np.concatenate([np.arange(n) for n in path_lens])
        padded[row_index, col_index] = np.concatenate(paths)
        return padded

    def __str__(self, node_names: Optional[List[str]] = None) -> str:
        return format_tree(self, node_names)


def make_hierarchy_from_edges(
    pairs: Sequence[Tuple[str, str]],
) -> Tuple[Hierarchy, List[str]]:
    """Creates a hierarchy from a list of name pairs.

    The order of the edges determines the order of the nodes.
    (Each node except the root appears once as a child.)
    The root is placed first in the order.
    """
    num_edges = len(pairs)
    num_nodes = num_edges + 1

    # Data structures to populate from list of pairs.
    parents = np.full([num_nodes], -1, dtype=int)

    names = [""] * num_nodes
    name_to_index = {}
    # Set name of root from first pair.
    root, _ = pairs[0]
    names[0] = root
    name_to_index[root] = 0
    # index_count = collections.defaultdict(int)

    for r, (u, v) in enumerate(pairs):
        if v in name_to_index:
            raise ValueError("has multiple parents", v)
        i = name_to_index[u]
        j = r + 1
        parents[j] = i
        names[j] = v
        name_to_index[v] = j
    return Hierarchy(parents), names


def load_edges(f: TextIO, delimiter=",") -> List[Tuple[str, str]]:
    """Load from file containing (parent, node) pairs."""
    import csv

    reader = csv.reader(f)
    pairs = []
    for row in reader:
        if not row:
            continue
        if len(row) != 2:
            raise ValueError("invalid row", row)
        pairs.append(tuple(row))
    return pairs


def rooted_subtree(tree: Hierarchy, nodes: np.ndarray) -> Hierarchy:
    """Finds the subtree that contains a subset of nodes."""
    # Check that root is present in subset.
    assert nodes[0] == 0
    # Construct a new list of parents.
    reindex = np.full([tree.num_nodes()], -1)
    reindex[nodes] = np.arange(len(nodes))
    parents = tree.parents()
    subtree_parents = np.where(parents[nodes] >= 0, reindex[parents[nodes]], -1)
    assert np.all(subtree_parents[1:] >= 0), "parent not in subset"
    # Ensure that parent appears before child.
    assert np.all(subtree_parents < np.arange(len(nodes)))
    return Hierarchy(subtree_parents)


def rooted_subtree_spanning(
    tree: Hierarchy, nodes: np.ndarray
) -> Tuple[Hierarchy, np.ndarray]:
    nodes = ancestors_union(tree, nodes)
    subtree = rooted_subtree(tree, nodes)
    return subtree, nodes


def ancestors_union(tree: Hierarchy, node_subset: np.ndarray) -> np.ndarray:
    """Returns union of ancestors of nodes."""
    paths = tree.paths_padded(-1)
    paths = paths[node_subset]
    return np.unique(paths[paths >= 0])


def format_tree(
    tree: Hierarchy, node_names: Optional[List[str]] = None, include_size: bool = False
) -> str:
    if node_names is None:
        node_names = [str(i) for i in range(tree.num_nodes())]

    node_to_children = tree.children()
    node_sizes = tree.num_leaf_descendants()

    # def subtree(node, prefix, is_last):
    #     yield prefix + ('└── ' if is_last else '├── ') + node_names[node] + '\n'
    #     children = node_to_children.get(node, ())
    #     child_prefix = prefix + ('    ' if is_last else '│   ')
    #     for i, child in enumerate(children):
    #         child_is_last = (i == len(children) - 1)
    #         yield from subtree(child, child_prefix, child_is_last)

    def subtree(node, node_prefix, desc_prefix):
        name = node_names[node]
        size = node_sizes[node]
        text = f"{name} ({size})" if include_size and size > 1 else name
        yield node_prefix + text + "\n"
        children = node_to_children.get(node, ())
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            yield from subtree(
                child,
                node_prefix=desc_prefix + ("└── " if is_last else "├── "),
                desc_prefix=desc_prefix + ("    " if is_last else "│   "),
            )

    return "".join(subtree(0, "", ""))


def find_lca(tree: Hierarchy, inds_a: np.ndarray, inds_b: np.ndarray) -> np.ndarray:
    """Returns the index of the LCA node.

    Supports multi-dimensional index arrays.
    For example, to obtain an exhaustive table:
        n = tree.num_nodes()
        find_lca(tree, np.arange(n)[:, np.newaxis], np.arange(n)[np.newaxis, :])
    """
    paths = tree.paths_padded(exclude_root=False)
    paths_a = paths[inds_a]
    paths_b = paths[inds_b]
    num_common = np.count_nonzero(
        ((paths_a == paths_b) & (paths_a >= 0) & (paths_b >= 0)), axis=-1
    )
    return paths[inds_a, num_common - 1]


class FindLCA:
    def __init__(self, tree: Hierarchy):
        self.paths = tree.paths_padded(exclude_root=False)

    def __call__(self, inds_a: np.ndarray, inds_b: np.ndarray) -> np.ndarray:
        paths = self.paths
        paths_a = paths[inds_a]
        paths_b = paths[inds_b]
        num_common = np.count_nonzero(
            ((paths_a == paths_b) & (paths_a >= 0) & (paths_b >= 0)), axis=-1
        )
        return paths[inds_a, num_common - 1]


# Used in validation
def truncate_given_lca(gt: np.ndarray, pr: np.ndarray, lca: np.ndarray) -> np.ndarray:
    """Truncates the prediction if a descendant of the ground-truth."""
    return np.where(gt == lca, gt, pr)


def find_projection(tree: Hierarchy, node_subset: np.ndarray) -> np.ndarray:
    """Finds projection to nearest ancestor in subtree."""
    # TODO: Only works for rooted sub-trees?
    # Use paths rather than ancestor_mask to avoid large memory usage.
    assert np.all(node_subset >= 0)
    paths = tree.paths_padded(-1)
    # Find index in subset.
    reindex = np.full([tree.num_nodes()], -1)
    reindex[node_subset] = np.arange(len(node_subset))
    subset_paths = np.where(paths >= 0, reindex[paths], -1)
    deepest = _last_nonzero(subset_paths >= 0, axis=1)
    # Check that all ancestors are present.
    # TODO: Could consider removing for non-rooted sub-trees?
    assert np.all(np.count_nonzero(subset_paths >= 0, axis=1) - 1 == deepest)
    return subset_paths[np.arange(tree.num_nodes()), deepest]


def _last_nonzero(x, axis):
    x = np.asarray(x, bool)
    assert np.all(np.any(x, axis=axis)), "at least one must be nonzero"
    # Find last element that is true.
    # (First element that is true in reversed array.)
    n = x.shape[axis]
    return (n - 1) - np.argmax(np.flip(x, axis), axis=axis)


def uniform_leaf(tree: Hierarchy) -> np.ndarray:
    """Returns a uniform distribution over leaf nodes."""
    is_ancestor = tree.ancestor_mask(strict=False)
    is_leaf = tree.leaf_mask()
    num_leaf_descendants = is_ancestor[:, is_leaf].sum(axis=1)
    return num_leaf_descendants / is_leaf.sum()


class Sum(Module):
    """Implements sum_xxx as an object. Avoids re-computation."""

    def __init__(
        self,
        tree: Hierarchy,
        transpose: bool,
        subset: Optional[np.ndarray] = None,
        # leaf_only: bool = False,
        exclude_root: bool = False,
        strict: bool = False,
    ):
        super().__init__()
        # The value matrix[i, j] is true if i is an ancestor of j.
        # Take transpose for sum over descendants.
        matrix = tree.ancestor_mask(strict=strict)
        if subset is not None:
            matrix = matrix[:, subset]
        if exclude_root:
            matrix = matrix[1:, :]
        if transpose:
            matrix = matrix.T
        matrix = torch.from_numpy(matrix).type(torch.get_default_dtype())
        self.matrix = matrix

    def _apply(self, fn):
        super()._apply(fn)
        self.matrix = fn(self.matrix)
        return self

    def forward(self, values: torch.Tensor, dim: int = -1) -> torch.Tensor:
        # TODO: Re-order dimensions to make this work with dim != -1.
        assert dim in (-1, values.ndim - 1)
        return torch.tensordot(values, self.matrix, dims=1)


SumAncestors = partial(Sum, transpose=False)
SumDescendants = partial(Sum, transpose=True)
