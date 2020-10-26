from typing import List, Dict, Tuple
from collections import Counter


class Node:
    def __init__(self, **kwargs) -> None:
        self.key = kwargs.get('key', None)
        self.counter = kwargs.get('counter', None)
        self.parent = kwargs.get('parent', None)
        self.childs = {}
        self.link = None
    
    def display(self, index: int=0):
        print("{} [{}: {}]\n".format(" -"*(index), self.key, self.counter))
        for child in self.childs.values():
            child.display(index+1)


class FPG:
    def __init__(self, minimum_support: int=2) -> None:
        self.support_table = {}
        self.header_table = {}
        self.conditional_patter_bases = {}
        self.root_node = None
        self.support_threshold = minimum_support
        self.dataset = []
        self.support_dataset = []
        self.conditional_patter_bases = {}
        self.fis = {}

    def create_tree(self, dataset: list) -> None:
        if self.support_threshold:
            self.preprocessing(dataset)

            # Tree building
            self.root_node = Node(key='NULL', counter=0)
            for transaction, increment in self.support_dataset:
                self.build_tree(transaction, self.root_node, increment)
            
            # Linking nodes
            for val in self.header_table.values():
                if len(val['nodes']) > 1:
                    for index in range(len(val['nodes'])-1):
                        val['nodes'][index].link = val['nodes'][index+1]
            
            return self.header_table

    def preprocessing(self, dataset) -> None:
        # Support
        for transaction, i in dataset:
            for item in transaction:
                self.support_table[item] = self.support_table.get(item, 0) + i
        
        # Support filtering and sorting
        self.support_table = filter(lambda x:x[1]>=self.support_threshold, self.support_table.items())
        self.support_table = dict(sorted(list(self.support_table), key=lambda x: x[0]))
        self.support_table = dict(sorted(self.support_table.items(), key=lambda x: x[1], reverse=True))
        mask = list(self.support_table.keys())
        
        clean_dataset = []
        for transaction, i in dataset:
            tr = list(filter(lambda x: x in mask, transaction))
            tr.sort(key=lambda x: mask.index(x))
            clean_dataset.append((tr, i))
        self.support_dataset = clean_dataset

        # Header
        for key in self.support_table.keys():
            self.header_table[key] = {'support': self.support_table[key], 'nodes': []}
    
    def build_tree(self, transaction: List[str], node: Node, increment) -> Node:
        if len(transaction) < 1: return
        key = transaction[0]
        if key in node.childs.keys():
            node.childs[key].counter += increment
        else:
            node.childs[key] = Node(key=key, counter=increment, parent=node)
            self.header_table[key]['nodes'].append(node.childs[key])
        
        if len(transaction) > 1:
            self.build_tree(transaction[1:], node.childs[key], increment)
    
    def mine_tree(self, header, prefix, fis) -> None:
        rhk = list(header.keys())[::-1]
        for key in rhk:
            new_fis = prefix.copy()
            new_fis.add(key)
            fis.append(new_fis)

            cpb = self.get_prefixes(key)
            self.conditional_patter_bases[key] = cpb

            sub_fpg = FPG(self.support_threshold)
            sub_fpg.create_tree(cpb)

            if sub_fpg.header_table != {}:
                sub_fpg.mine_tree(sub_fpg.header_table, new_fis, fis)

        self.fis = fis
        
        # cpb = self.get_CPBes()
        # for key, dataset in cpb.items():

        #     new_fis = prefix.copy()
        #     new_fis.add(key)
        #     fis.append(new_fis)

        #     tmp_fpg = FPG(self.support_threshold)
        #     ht = tmp_fpg.create_tree(dataset)
        #     tmp_fpg.display()

        #     if ht != {} and ht != None:
        #         tmp_fpg.mine_tree(new_fis, fis)
        #     # self.fis[key] = fis

    def get_CPBes(self):
        reversed_header_keys = list(self.header_table.keys())[::-1]
        conditional_patter_bases = {}
        for key in reversed_header_keys:
            if len(self.header_table[key]['nodes']) > 0:
                conditional_patter_bases[key] = self.get_prefixes(self.header_table[key]['nodes'][0])
        
        self.conditional_patter_bases = conditional_patter_bases
        return conditional_patter_bases
    
    def get_prefixes(self, key: str) -> List[list]:
        if len(self.header_table[key]['nodes']) < 1: return []
        node = self.header_table[key]['nodes'][0]
        cnt = node.counter
        paths = []
        while node:
            single_path = self.traverse_root(node)
            if len(single_path) > 1:
                paths.append((single_path[1:], cnt))
            node = node.link

        self.conditional_patter_bases[key] = paths
        return paths
        # else:
        #     return []

    # def get_prefixes(self, node: Node) -> List[tuple]:
    #     paths = []
    #     tmp = node
    #     cnt = node.counter
    #     while tmp:
    #         single_path = self.traverse_root(tmp)
    #         if len(single_path) > 1:
    #             paths.append((single_path[1:], cnt))
    #         tmp = tmp.link
    #     return paths
    
    def traverse_root(self, node: Node) -> List[str]:
        path = []
        tmp = node
        while tmp is not self.root_node:
            path.append(tmp.key)
            tmp = tmp.parent
        return path
    
    def modify_dataset(self, dataset: List[list]) -> List[tuple]:
        for transaction in dataset:
            self.support_dataset.append((transaction, 1))
        return self.support_dataset

    def display(self) -> None:
        if self.root_node:
            print("Tree")
            self.root_node.display()

        if self.header_table:
            print("Header table:")
            print(*self.header_table.items(), sep='\n')

        elif self.support_table:
            print("Support table:")
            print(*self.support_table.items(), sep='\n')
        
        if self.conditional_patter_bases:
            print("Conditional pattern bases (CPB):")
            print(*self.conditional_patter_bases.items(), sep='\n')
            # print("Initial dataset")
            # print(*self.support_dataset, sep='\n')
        
        if self.fis:
            print("Frequnt item sets: ({})".format(len(self.fis)))
            print(*self.fis, sep='\n')
