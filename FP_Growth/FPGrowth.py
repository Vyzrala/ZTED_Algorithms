from typing import List, Dict, Tuple
from collections import Counter
from datasets import translation


class Node:
    def __init__(self, key: str, counter: int, parent_node) -> None:
        self.key = key
        self.counter = counter
        self.parent = parent_node
        self.childs: Dict[str, Node] = {}
        self.link = None

    def increment_counter(self):
        pass


    def display(self, index: int=0) -> None:
        # print("{} [{}: {}]\n".format(" -"*(index), translation.get(self.key, self.key), self.counter))
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
        self.supp_set = False
        self.minimum_support = min_support
        self.root_node = None
        self.support = None
        self.clean_dataset = None
        self.header_table: Dict[str, list] = {}
        self.conditional_pattern_base = {}
        self.fis = None
    
    def run(self, dataset: List[list], supp_set: list=None) -> Tuple[List[list], Dict[frozenset, int]]:
        self.initial_dataset = dataset
        wset = self.initial_dataset
        wset = [list(set(transaction)) for transaction in wset]  # Make sure that items in transaction are uniqe
        ui = self.get_unique_items(wset)
        self.support = self.get_support(wset, ui)
        self.clean_dataset = self.preprocess_dataset(wset)

        return self.clean_dataset
    

    def display_info(self) -> None:
        # print("Initial dataset (minimum support = {}):".format(self.minimum_support), *self.initial_dataset, sep='\n')
        # print("Support:", *{list(k)[0]:v for k,v in self.support.items()}.items(), sep='\n')
        print("Cleaned and sorted dataset:", *self.clean_dataset, sep='\n')
        # print("Support table:")
        # print(*self.support.items(), sep='\n')

        print("\nTree:")
        self.print_tree()

        if self.header_table != {}:
            print("Header Table:")
            print(*self.header_table.items(), sep='\n')

        # print("Linked nodes:")
        # for v in self.header_table.values():
        #     v['nodes'][0].display_linked()

        if self.conditional_pattern_base != {}:
            print("Conditional pattern base:")
            print(*self.conditional_pattern_base.items(), sep='\n')
        
        if self.fis:
            print("Frequent item sets:", len(self.fis))
            print(*self.fis, sep='\n')
    
    def print_tree(self) -> None:
        try:
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
        for k in self.support: 
            self.header_table[k] = {'support': self.support[k], 'nodes': []}

        self.root_node = Node('NULL', 0, None)
        for transaction in dataset:
            self.insert_transaction(transaction, self.root_node)
        
        # Linking nodes
        for v in self.header_table.values():
            if len(v['nodes']) > 1:
                for i in range(len(v['nodes'])-1):
                    v['nodes'][i].link = v['nodes'][i+1]
        
    def insert_transaction(self, transaction: List[str], node: Node) -> None:
        if len(transaction) < 1: return
        key = transaction[0]

        if key in node.childs.keys():
            node.childs[key].counter += 1 ################################################## increment by support 
        else:
            node.childs[key] = Node(key, 1, node)
            self.header_table[key]['nodes'].append(node.childs[key])

        if len(transaction) > 1:
            self.insert_transaction(transaction[1:], node.childs[key])

    def get_prefix(self, node: Node):
        paths = []
        while node:
            path = self.traverse_root(node)
            if len(path) > 1:
                paths.append([path[1:], node.counter])
            node = node.link
        return paths

    def traverse_root(self, node: Node) -> list:
        tmp = node
        path = []
        while tmp is not self.root_node:
            path.append(tmp.key)
            tmp = tmp.parent
        return path

    def get_CPB(self, key:str) -> List[list]:
        start_node = self.header_table[key]['nodes'][0]
        paths = self.get_prefix(start_node)
        dataset = []
        supp_set = []
        for item in paths:
            dataset.append(item[0])
            supp_set.append(item[1])
        self.conditional_pattern_base[key] = dataset
        return dataset, supp_set
    
    def mine_fis(self, index, header_parent, prefix, fis):
        reverse_header_keys = list(header_parent.keys())[::-1]
        for key in reverse_header_keys:
            new_fis = prefix.copy()
            new_fis.add(key)
            fis.append(new_fis)
            CPB, supp_set = self.get_CPB(key)

            # Generate sub-tree
            tmp_fpg = FPG(self.minimum_support)
            tmp_clean_dataset = tmp_fpg.run(CPB, supp_set)
            tmp_fpg.build_tree(tmp_clean_dataset)
            # print("CPB:", CPB)
            # print("SUPP SET:", supp_set)
            # print("tmp supp:", tmp_fpg.support)
            # print("\nStats for {} key".format(key))
            # tmp_fpg.display_info()
            if tmp_fpg.header_table != {}:
                self.mine_fis(index+1, tmp_fpg.header_table, new_fis, fis)
        
        self.fis = fis
