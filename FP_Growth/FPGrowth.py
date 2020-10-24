from typing import List, Dict, Tuple
from collections import Counter


class Node:
    def __init__(self, key: str, counter: int, parent_node) -> None:
        self.key = key
        self.counter = counter
        self.parent = parent_node
        self.childs: Dict[str, Node] = {}
        self.link = None

    def display(self, index: int=0) -> None:
        print("{} [{}: {}]\n".format(" -"*(index), self.key, self.counter))
        for child in self.childs.values():
            child.display(index+1)
        
    def display_linked(self):
        current_node = self
        while current_node != None:
            print("[Key = {}]".format(current_node.key), end='')
            if current_node.link: print(" => ", end='')
            current_node = current_node.link
        print()
 

class FPG:
    def __init__(self, min_support: int=2) -> None:
        self.minimum_support = min_support
        self.root_node = None
        self.support = None
        self.clean_dataset = None
        self.header_table: Dict[str, list] = {}
        self.frequent_patterns = {}
        self.conditional_pattern_base = {}
    
    def run(self, dataset: List[list]) -> Tuple[List[list], Dict[frozenset, int]]:
        self.initial_dataset = dataset
        wset = self.initial_dataset
        wset = [list(set(transaction)) for transaction in wset]  # Make sure that items in transaction are uniqe
        ui = None
        # ui = self.get_unique_items(wset)
        self.support = self.get_support(wset, ui)
        self.clean_dataset = self.preprocess_dataset(wset)

        return self.clean_dataset
    
    def display_info(self) -> None:
        # print("Initial dataset (minimum support = {}):".format(self.minimum_support), *self.initial_dataset, sep='\n')
        # print("Support:", *{list(k)[0]:v for k,v in self.support.items()}.items(), sep='\n')
        # print("Cleaned and sorted dataset:", *self.clean_dataset, sep='\n')
        self.print_tree()
        # print("Support table:")
        # print(*self.support.items(), sep='\n')
        print("Header Table:")
        print(*self.header_table.items(), sep='\n')

        # print("Linked nodes:")
        # for v in self.header_table.values():
        #     v['first_node'].display_linked()
        print("Conditional pattern base:")
        print(*self.conditional_pattern_base.items(), sep='\n')
    
    def print_tree(self) -> None:
        try:
            print("\nPrinting tree:\n")
            self.root_node.display()
        except:
            print("\tNo root node.\n")

    def get_unique_items(self, wset: List[list]) -> List[set]:
        unique_items = list(set(sum(wset, [])))
        return [frozenset([x]) for x in unique_items]

    def get_support(self, dataset: List[list], candidates: List[frozenset]) -> Dict[frozenset, int]:
        #     support = {}
        #     for transaction in dataset:
        #         for item in candidates:
        #             if item.issubset(transaction):
        #                 sub = frozenset(item)
        #                 if sub in support.keys():
        #                     support[sub] += 1
        #                 else:
        #                     support[sub] = 1

        #     support = sorted(support.items(), key=lambda x: x[1], reverse=True)  # Sorting by value
        #     support = {k:v for k, v in support if v >= self.minimum_support}  # Filtering by minimum support value

        support = Counter(item for item in sum(dataset, []))
        support = filter(lambda item: item[1]>=self.minimum_support, support.items())
        support = sorted(support, key=lambda x:x[0])
        support = sorted(support, key=lambda x:x[1], reverse=True)
        # support = {frozenset([k]):v for k,v in support}
        support = dict(support)
        return support

    def preprocess_dataset(self, dataset: List[list]) -> List[list]:
        # Cleaning and sorting dataset
        clean_dataset = []
        # mask = [x for x in list(self.support)]
        mask = list(self.support.keys())
        for transaction in dataset:
            clean_dataset.append(list(filter(lambda item: item in mask, transaction)))
            clean_dataset[-1].sort(key=lambda i: mask.index(i))

        return clean_dataset
    
    def build_tree(self, dataset: List[list]) -> None:
        self.root_node = Node('NULL', 0, None)
        for k in self.support: 
            self.header_table[k] = {'support': self.support[k], 'first_node': None}

        for transaction in dataset:
            self.insert_transaction(transaction, self.root_node)
        
    def insert_transaction(self, transaction: List[str], node: Node) -> None:
        key = transaction[0]
        if key in node.childs.keys():
            node.childs[key].counter += 1
        else:
            node.childs[key] = Node(key, 1, node)
            if self.header_table[key]['first_node'] is None:
                self.header_table[key]['first_node'] = node.childs[key]
            else:
                tmp = self.header_table[key]['first_node']
                while tmp.link: tmp = tmp.link
                tmp.link = node.childs[key]

        if len(transaction) > 1:
            self.insert_transaction(transaction[1:], node.childs[key])

    def generate_frequent_patterns(self) -> None:
        for k, v in self.header_table.items():
            tmp = self.get_condidtional_pattern_base(k, v['first_node'])
            self.conditional_pattern_base[k] = tmp
            # self.header_table[k]['cpb'] = tmp
        
    def get_condidtional_pattern_base(self, k: str, node: Node):
        # print("nk = {}, np = {}".format(node.key, node.parent.key))
        if node.parent is not self.root_node:
            paths = self.traverse_side(node)
            return paths
            
    def traverse_up(self, node: Node) -> list:  # Creates single path
        path = []
        cnt = node.counter
        while node is not self.root_node:
            path.append(node.key)
            node = node.parent
        
        if len(path) > 1: 
            return [path[1:], cnt]

    def traverse_side(self, node: Node) -> list:  # Create all path for given node
        paths = []
        while node:
            path = self.traverse_up(node)
            if path is not None: 
                path[0].sort()
                paths.append(path)
            node = node.link
        return paths
