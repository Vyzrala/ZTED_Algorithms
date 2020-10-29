import AprioriS


class AprioriS:
    def __init__(self, min_support: int) -> None:
        self.minimum_support  = min_support
        self.dataset = None

    def run(self, dataset: list) -> None:
        self.dataset = dataset
        ls = self.get_frequent_pages(1)
        k = 2
        while ls:
            print('LS{}: # = {} {}'.format(k-1, len(ls), ls))
            fp = self.get_frequent_pages(k)
            print('FP{}: # = {} {}'.format(k, len(fp), fp))
            cs = self.get_candidate_sets(ls, fp)
            print('CS{}: # = {} {}'.format(k, len(cs), cs))
            if not fp or not cs: break
            ls = self.filter_candidates(cs)
            k += 1
            print()
        
    def get_frequent_pages(self, column: int) -> list:  # get FP
        if column > 0:
            frequent_pages = {}
            for row in self.dataset:
                if len(row) >= column:
                    key = row[column-1]
                    frequent_pages[key] = frequent_pages.get(key, 0) + 1

            frequent_pages = dict(filter(lambda x: x[1] >= self.minimum_support, frequent_pages.items()))
            return [[item] for item in frequent_pages.keys()]

    def get_candidate_sets(self, ls: list, fp: list) -> list:  # get CS
        candidates = []
        for seq in ls:
            for page in fp:
                if seq[-1] != page[0]:
                    candidates.append(seq + page)

        return candidates

    def filter_candidates(self, candidates: list) -> list:  # get LS
        outfiltered_cands = {}
        candidate_size = len(candidates[0])
        for row in self.dataset:
            for candidate in candidates:
                if candidate == row[:candidate_size]:
                    tmp_key = ''.join(candidate)
                    counter = outfiltered_cands.get(tmp_key, [0])[0]
                    outfiltered_cands[tmp_key] = [counter + 1, candidate]
        outfiltered_cands = dict(filter(lambda x:x[1][0]>=self.minimum_support, outfiltered_cands.items()))

        return [v for k, v in outfiltered_cands.values()]