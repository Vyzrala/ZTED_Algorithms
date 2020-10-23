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
        self.header_table: Dict[str, list] = {}
    
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
        print("Header Table:")
        # print(*self.header_table.items(), sep='\n')
        for k, v in self.header_table.items():
            print("Key: {} | Support = {} | Nodes: {}".format(k, v['support'], len(v['nodes'])))
            # print("Key: {} | Support = {} | Nodes: [".format(k, v['support']), end='')
            # for n in v['nodes']:
            #     print(" {}".format(n.key), end="")
            # print(" ]")

        print("Linked nodes:")
        for v in self.header_table.values():
            v['nodes'][0].display_linked()

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
            # self.header_table[list(k)[0]] = [self.support[k], None]
            self.header_table[k] = {'support': self.support[k], 'nodes': []}

        for transaction in dataset:
            self.update_tree(transaction, self.root_node)
        
        # Linking nodes
        for v in self.header_table.values():
            if len(v['nodes']) > 1:
                for i in range(len(v['nodes'])-1):
                    v['nodes'][i].link = v['nodes'][i+1]

    def update_tree(self, transaction: List[str], node: Node) -> None:
        key = transaction[0]
        if key in node.childs:
            node.childs[key].counter += 1
        else:
            node.childs[key] = Node(key, 1, node)
            self.header_table[key]['nodes'].append(node.childs[key])
        if len(transaction) > 1:
            self.update_tree(transaction[1:], node.childs[key])
 
    def get_nodes(self, token: str) -> List[Node]:
        node_list = self.header_table.get(token, None)
        if node_list:
            return node_list.get('nodes', None)
        return None

    def print_tree(self) -> None:
        try:
            print("\nPrinting tree:\n")
            self.root_node.display()
        except:
            print("\tNo root node.\n")
    