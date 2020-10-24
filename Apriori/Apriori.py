from typing import List, Dict

class Apriori:
    """
        Class performing task of apriori algorithm.
    """
    def __init__(self, minimum_support: int=2):
        """
            Initialization method. You can specify minimum support level for your dataset.
            
            Parameters
            ----------
                minimum_support : int
                    Minimum support level. Minimum number of occurances of specific item in datase.
        """
        self.minimum_support = minimum_support

    def run(self, dataset: List[list]) -> List[frozenset]:
        """
            Main method responsible for running algorithm in correct way.

            Parameters
            ----------
            dataset : list of lists
                The dataset of transaction that you want to process.
            
            Returns
            -------
                L : list of frozensets
                    Apriori algorithm output.
        """
        wset = dataset
        k = 1
        C = self.unique_items(wset)
        L = None
        while C:
            L = self.get_L(wset, C, self.minimum_support)
            # print("C{}: {} # = {}".format(k, list(map(set, C)), len(C)))
            # print("L{}: {} # = {}\n".format(k, list(map(set, L)), len(L)))
            k += 1
            C = self.create_candidates(L, k)
        
        print("C: {} # = {}".format(C, len(C)))
        print("L: {} # = {}\n".format(list(map(set, L)), len(L)))

        return L

    def unique_items(self, wset: List[set]) -> List[frozenset]:
        """
            Generates list of unique items that occured in dataset.

            Parameters
            ----------
                wset : List of sets
                    Initial dataset that has to be processed.
            
            Returns
            -------
                List unique items occured in dataset each wrapped in frozenset.
        """
        unique = set()
        for ss in wset:
            unique.update(ss)

        return [frozenset([x]) for x in unique]

    def get_support(self, dataset: List[set], candidates: List[set]) -> Dict[frozenset, int]:
        """
            Method calculating support for each set of items in dataset.
            
            Parameters
            ----------
                dataset : (Initial) List of sets.
                    Initial dataset
                candidates: List of sets
                    List of sets of items that possibly could occur in transations.
            
            Returns
            -------
                occurances : Dictionary 
                    Dictionary where key is a set of items and value is number of occurances in dataset.
        """
        occurances = {}
        for transaction in dataset:
            for items in candidates:
                if items.issubset(transaction):
                    sub = frozenset(items)
                    if sub in occurances.keys():
                        occurances[sub] += 1
                    else:
                        occurances[sub] = 1
        
        return occurances

    def create_candidates(self, L: List[frozenset], k: int) -> List[frozenset]:
        """
            Method creates list of set of possible combination of k items.

            Parameters
            ----------
                L : List of frozensets
                    List of sets that has to be transformed in list of sets with k ( k > len(L[0]) ) elements.
                k : int
                    Required number of items in one set.
            
            Returns
            -------
                candidates : list of sets
                    List of sets where each set has k items.
        """
        candidates = []
        len_L = len(L)
        for i in range(len_L):
            for j in range(i+1, len_L):
                L1, L2 = list(L[i])[:k-2], list(L[j])[:k-2]
                L1.sort()
                L2.sort()
                if L1==L2:
                    candidates.append(L[i] | L[j])
            
        return candidates

    def get_L(self, dataset: List[frozenset], candidates: List[frozenset], minimum_support: int) -> List[frozenset]:
        """
            Method filtering candidates by the minimum support in dataset.
            
            Parameters
            ----------
                dataset : List of frozensets
                    Initial dataset used to get support data.
                candidates : List of sets
                    List of possible sets of items.
                minimum_support : int
                    Minimal number of occurances of candidate in dataset.
            
            Returns
            -------
                L : List of frozensets
                    List of itemsets that occured minimum_support times in dataset.
        """
        L = []
        support = self.get_support(dataset, candidates)
        for candidate in candidates:
            if support.get(candidate, -1) >= minimum_support:
                L.append(candidate)

        return L
