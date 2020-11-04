from typing import List, Dict

class AprioriAll:
    def __init__(self, threshold :int= 0.25) -> None:
        self.threshold = threshold
        self.map = None
    
    def run(self, raw_dataset: List[list]) -> None:
        ds = {}
        for row in raw_dataset:
            key = row[0]
            ds[key] = ds.get(key, []) + [tuple(row[-1])]
        self.ds = ds
        
        
        c = self.get_unique()
        k = 1
        sets = []
        while c:
            l = self.get_l(c)
            sets.append(l)
            print('C{}: {} # = {}'.format(k, c, len(c)))
            print('L{}: {} # = {}'.format(k, l, len(l)))
            print()
            c = self.get_c(l)
            k += 1
            
        mapping, nds = self.map_values(sets)
        print('Mapping:')
        for k, v in nds.items():
            print('{}: {}'.format(k, v))
        print('Mapping legend:', mapping)
        sequences = self.sequencing(nds)
        print('Sequences:')
        for k, v in sequences.items():
            print('{}: {}'.format(k, v))
        unmapped = self.unmap(sequences, mapping)
        print('Unmapping:')
        for k, v in unmapped:
            print('{}: {}'.format(k, v))
        
    def get_unique(self) -> List[str]:
        ui = []
        for values in self.ds.values():
            for seq in values:
                for item in seq:
                    key = item
                    if key not in ui:
                        ui.append(key)
        return ui
    
    def get_l(self, c:list) -> list:
        support = self.get_frequences(c)
        support = {k:v/len(self.ds) for k, v in support.items()}
        support = {k:v for k, v in support.items() if v>=self.threshold}
        return list(support.keys())
    
    def get_frequences(self, cands):
        frequencies = {}
        for v in self.ds.values():
            for seq in v:
                for cand in cands:
                    if set(cand).issubset(seq):
                        cval = frequencies.get(cand, 0)
                        if cval < len(self.ds):
                            frequencies[cand] = cval + 1 
        
        return frequencies
    
    def get_c(self, l: list) -> List[tuple]:
        candidates = []
        l_size = len(l)
        for i in range(l_size):
            for j in range(i+1, l_size):
                candidates.append(tuple([l[i], l[j]]))
        
        return candidates
    
    def map_values(self, sets):
        flat_set = [item for s in sets for item in s]
        mapper = {}
        for iterator, (k, v) in enumerate(self.get_frequences(flat_set).items()):
            mapper[k] = iterator + 1

        nds = {}
        for k, v in self.ds.items():
            nseq = []
            for seq in v:
                t = []
                for key in mapper.keys():
                    if set((key)).issubset(seq):
                        t.append(mapper.get(key, None))
                if t:
                    nseq.append(tuple(t))
            nds[k] = nseq
        return mapper, nds
    
    
    def sequencing(self, ds):
        def eliminate(pair, seq):
            if len(seq) < len(pair): 
                return False
            p1 = False
            p2 = False
            slc = 0
            for i in range(len(seq)):
                if pair[0] in seq[i]:
                    p1 = True
                    slc = i
                    break
            if p1:
                for i in range(slc+1, len(seq)):
                    if pair[1] in seq[i]:
                        p2  = True
                        break
            return p1 and p2

        ds_keys = list(ds.keys())
        ds_len = len(ds_keys)
        sequences = {}

        for i in range(ds_len):
            for j in range(ds_len):
                pair = (int(ds_keys[i]), int(ds_keys[j]))
                for k, v in ds.items():
                    if eliminate(pair, v):
                        sequences[pair] = sequences.get(pair, 0) + 1
        
        sequences = {k:v/ds_len for k, v in sequences.items()}
        sequences = {k:v for k, v in sequences.items() if v>=self.threshold}
        return sequences

    def unmap(self, sequences: List[tuple], mapper: dict) -> List[tuple]:
        unmapper = {v:k for k, v in mapper.items()}
        return [((unmapper.get(k[0], k[0]), unmapper.get(k[1], k[1])) , v) for k, v in sequences.items()]
        
        