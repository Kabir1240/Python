def ukkonen(string: str):
    """
    uses ukkonen to first generate a trie in O(N) time, then generate a suffix array in O(N) time and finally
    generate a bwt in O(N) time for a total complexity of O(3N) --> O(N)

    Args:
        string: a string to convert into BWT

    Returns:
        a bwt string
    """

    string = string + '$'
    n = len(string)

    trie = generate_trie(string, n)
    suffix_array = trie.get_suffix_array()
    bwt = generate_bwt(string, suffix_array)
    return bwt


def generate_trie(string: str, n: int):
    """
    generates a suffix trie using ukkonen in O(N)
    Args:
        string: string to use for generating the suffix trie
        n: length of string

    Returns:
        the root node of the trie
    """
    # initialize node and global end
    root = Node(is_root=True)
    global_end = GlobalEnd()

    # set active node, length and edge for initialization
    # NOTE: Active length is implemented from the active_node and not the root
    active_length = 0
    active_node = root

    # find active edge using the first letter in the string
    index = ord(string[0]) - 36
    active_edge = active_node.edges[index]

    j = 0
    suffix_id = 0
    for i in range(n):
        # set active node to root at the start of every phase, increment global end reset prev_node
        global_end += 1
        prev_node = None
        while j < i + 1:
            # reset show stopper
            show_stopper = False

            # make a suffix string for easier comparison
            suffix_rep = (j, i)
            suffix = string[suffix_rep[0]: suffix_rep[1] + 1]

            # if the edge already exists
            if active_edge is not None:

                # create a string to represent the data inside the edge for easier representation
                edge_rep = active_edge.edge_rep
                edge_data = string[edge_rep[0]:int(edge_rep[1]) + 1]

                # checks if there was a mismatch or not
                mismatch = True

                # while loop for comparison if needed
                while edge_data[active_length] == suffix[active_length]:
                    active_length += 1

                    # rule number 3, if it already exists, exit (do nothing)
                    if active_length == len(suffix):
                        # if the suffix had already fully matched during a show stopper, still move on to the next node
                        if active_length == len(edge_data):
                            active_node = active_edge.child
                            active_edge = active_node.edges[ord(string[suffix_rep[0] + active_length]) - 36]
                            j += active_length
                            active_length = 0

                        # set show stopper to true, break the while loop comparison
                        show_stopper = True
                        mismatch = False
                        break

                    # if the suffix matches so far but the edge is not a leaf, continue comparing in the next node
                    elif active_length == len(edge_data) and not active_edge.is_leaf:
                        # change active node and edge
                        active_node = active_edge.child
                        active_edge = active_node.edges[ord(suffix[active_length]) - 36]

                        # mismatch is False, reset everything for next node
                        mismatch = False
                        j += active_length
                        active_length = 0
                        break

                # rule 2a, if there was a mismatch, create a new_node and branch 2 edges
                if mismatch:
                    # create a new node
                    new_node = Node(is_root=False, parent_edge=active_edge, link=root)

                    # create 2 new edges
                    new_edge_1 = Edge(parent=active_node, edge_rep=(edge_rep[0] + active_length, global_end),
                                      suffix_id=active_edge.id)
                    new_edge_2 = Edge(parent=active_node, edge_rep=(suffix_rep[0] + active_length, global_end),
                                      suffix_id=suffix_id)

                    # link previous node to the newly created one
                    if prev_node is not None:
                        prev_node.update_link(new_node)

                    # add the new edges to the new node
                    new_node.edges[ord(edge_data[active_length]) - 36] = new_edge_1
                    new_node.edges[ord(suffix[active_length]) - 36] = new_edge_2

                    # amend the current edges data. Change the stored edge representation, leaf data and child
                    active_edge.edge_rep = (edge_rep[0], edge_rep[0] + active_length - 1)
                    active_edge.is_leaf = False
                    active_edge.child = new_node

                    # if there a suffix link exists, jump there
                    if active_node.link is not None:
                        active_node = active_node.link
                        active_edge = active_node.edges[ord(string[suffix_rep[0]]) - 36]
                        suffix_id += 1

                    # if the suffix link is the root or there is no link, continue as normal
                    elif active_node.link is root or active_node.link is None:
                        j += 1
                        active_node = root
                        active_length = 0
                        suffix_id = j

                        # if string has not ended, move to next node
                        if j < n:
                            index = ord(string[j]) - 36
                            active_edge = active_node.edges[index]

                    # set new node to prev node
                    prev_node = new_node

            # rule 2 (base), if edge doesnt exist, create it
            elif active_edge is None:
                # create a new edge
                new_edge = Edge(parent=active_node, edge_rep=(suffix_rep[0], global_end), suffix_id=suffix_id)
                # add edge to active node
                index = ord(string[suffix_rep[0]]) - 36
                active_node.edges[index] = new_edge

                # if there a suffix link exists, jump there
                if active_node.link is not None:
                    active_node = active_node.link
                    active_edge = active_node.edges[ord(string[suffix_rep[0]]) - 36]
                    suffix_id += 1

                # if the suffix link is the root or there is no link, continue as normal
                elif active_node.link is root or active_node.link is None:
                    j += 1
                    active_node = root
                    active_length = 0
                    suffix_id = j

                # if string has not ended, move to next node
                if j < n:
                    index = ord(string[j]) - 36
                    active_edge = active_node.edges[index]

            # if show stopper is encountered at any point, stop everything and move to the next phase.
            if show_stopper:
                break
    return root


def generate_bwt(string: str, suffix_array: list[int]):
    """
    generates the burrows wheeler transform string using the suffix array in O(N) time
    Args:
        string: string to convert into BWT
        suffix_array: suffix array of the string
    Returns:
        bwt string
    """

    bwt = ""
    for i in suffix_array:
        if i == 0:
            bwt += '$'
        else:
            bwt += string[i-1]

    return bwt


class Node:
    def __init__(self, is_root: bool, parent_edge=None, link=None):
        """
        Initializes Node class. Cases for root and non-root nodes
        Args:
            is_root: boolean to determine if Node is root or not
            parent_edge: parent edge if any
            link: suffix link if any
        """

        # if the Node is a root, it cannot have a parent edge or node
        if is_root:
            self.is_root = True
            self.parent_edge = None
            self.link = None

        # if the root is not a root, set parent_edge
        if not is_root:
            self.is_root = False
            self.parent_edge = parent_edge
            self.link = link

        # keep in mind ord('$') -> 36, at index 0 since we subtract 36 when using ord
        self.edges = [None] * 90

    def update_link(self, node):
        """
        updates the suffix link
        Args:
            node: new suffix link connection
        Returns:
            None
        """
        self.link = node

    def get_suffix_array(self):
        """
        generates suffix array using recursion through connected nodes and edges using DFS in O(N) time
        Returns: a suffix array, list of numbers
        """

        ret_val = []
        for i in self.edges:
            if i is not None:
                if i.is_leaf:
                    ret_val.append(i.id)
                else:
                    ret_val += i.child.get_suffix_array()
        return ret_val


class Edge:
    def __init__(self, parent, edge_rep: tuple, suffix_id):
        """
        initialize Edge Class
        Args:
            parent: parent node of edge
            edge_rep: the edge representation used to store indices
            suffix_id: id for leaf edges
        """

        self.parent = parent
        self.edge_rep = edge_rep
        self.child = None
        self.is_leaf = True
        self.id = suffix_id


class GlobalEnd:
    def __init__(self):
        """
        Initializes the global end class
        """

        self.global_end = -1

    def __iadd__(self, other: int):
        """
        Implement the in-place addition operation
        Args:
            other: a number to add into the global end
        Returns:
            global end after the process
        """

        # Implement the in-place addition operation
        if isinstance(other, int):
            self.global_end += other
        else:
            raise TypeError("Unsupported operand type for +=: {}".format(type(other)))
        return self

    def __add__(self, other: int):
        """
        Implement the addition operation
        Args:
            other: a number to add into the global end
        Returns:
            global end after the process
        """

        # Implement the addition operation
        if isinstance(other, int):
            self.global_end += other
        else:
            raise TypeError("Unsupported operand type for +=: {}".format(type(other)))
        return self

    def __int__(self):
        """
        Returns: an instance of global end as an integer
        """
        return self.global_end
