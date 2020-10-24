from FP_Growth.FPGrowth import FPG
from datasets import test


if __name__ == "__main__":

    for k, v in test.items():
        fpg = FPG()
        print('\n',k)
        fpg.minimum_support = v[1]
        clean_dataset = fpg.run(v[0])
        fpg.build_tree(clean_dataset)
        fpg.generate_frequent_patterns()
        fpg.display_info()
        del fpg

