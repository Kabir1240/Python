def ukkonen_naive(string: str):
    """
    uses a naive ukkonen to create a suffix trie. O(n^3) complexity
    Args:
        string: string to create a suffix trie

    Returns:
        a list of all suffixes added
    """

    suffix_trie = SuffixTrie()
    suffix_trie.construct(string)
    # return suffix_trie.find_suffixes()


class Edge:
    def __init__(self, parent, data: str):
        """
        Initialize Edge class for SuffixTrie
        Args:
            parent: parent Node
            data: data contained by edge
        """

        self.parent = parent
        self.data = data
        self.child = None
        self.is_leaf = True


class Node:
    def __init__(self, is_root: bool, parent_edge=None):
        """
        Initialize Node class for SuffixTrie
        Args:
            is_root: bool for if the Node is a root or not
            parent_edge: if the Node is not a root, parent_edge is the edge that connects Node with its parent node
        """

        # if the Node is a root, it cannot have a parent edge or node
        if is_root:
            self.is_root = True
            self.parent_edge = None

        # if the root is not a root, set parent_edge
        if not is_root:
            self.is_root = False
            self.parent_edge = parent_edge

        # keep in mind ord('$') -> 36, at index 0 since we subtract 36 when using ord
        self.edges = [None] * 90

    def add_connection(self, suffix: str):
        """
        Adds edge connections to the Node if the suffix doesnt already exist
        Args:
            suffix: suffix to add

        Returns:
            None
        """

        # finds the connecting edge using the first letter of the suffix (can be None)
        index = ord(suffix[0]) - 36
        curr_edge = self.edges[index]

        # if edge exists
        if curr_edge is not None:
            # traverse through connections and compare suffix with pre-existing data
            data = curr_edge.data
            k = 0
            while data[k] == suffix[k]:
                k += 1
                # rule number 3, if it already exists, exit (do nothing)
                # this also prevents adding a leaf or going to next node if all of suffix matches with data
                if k == len(suffix):
                    # print("3")
                    break

                # rule 1, if the suffix matches and the edge is a leaf, extend the edge by one letter
                elif k == len(data) and curr_edge.is_leaf:
                    # print("1")
                    curr_edge.data += suffix[-1]
                    break

                # if the suffix matches so far but the edge is not a leaf, continue comparing in the next node
                elif k == len(data) and not curr_edge.is_leaf:
                    remaining_suffix = suffix[k:]
                    next_node = curr_edge.child
                    next_node.add_connection(remaining_suffix)
                    break

            # rule 2a, if there was a mismatch, create a new_node and branch 2 edges
            if (k != len(data)) and k != len(suffix):
                # print("2")
                # create new node and add the new edges
                new_node = Node(is_root=False, parent_edge=curr_edge)
                new_node.add_connection(data[k:])
                new_node.add_connection(suffix[k:])

                # amend the current edges data
                curr_edge.data = data[:k]
                curr_edge.is_leaf = False
                curr_edge.child = new_node

        # rule 2 (base), if edge doesnt exist, create it
        elif curr_edge is None:
            # print("2, base")
            new_edge = Edge(parent=self, data=suffix)
            self.edges[index] = new_edge

    def traversal(self):
        ret_val = []
        for i in self.edges:
            if i is not None:
                if i.is_leaf:
                    ret_val.append(i.data)
                elif not i.is_leaf:
                    suffixes = i.child.traversal()
                    for j in suffixes:
                        ret_val.append(i.data + j)
        return ret_val


class SuffixTrie:
    def __init__(self):
        self.root = Node(is_root=True)

    def construct(self, string):
        n = len(string)

        for i in range(n):
            # set active node to root at the start of every phase
            curr_node = self.root
            # print("PHASE i: ", i+1)
            for j in range(i + 1):
                suffix = string[j:i + 1]
                curr_node.add_connection(suffix)

    def find_suffixes(self):
        return self.root.traversal()


string = "abcabxabcyab$"
# string = ""
print(ukkonen_naive(string))

