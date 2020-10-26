from FP_Growth.FPGrowth import FPG as FPG1
from FP_Growth.FPGrowth2 import FPG as FPG2
from datasets import test


if __name__ == "__main__":

    # for k, v in test.items():
    #     fpg = FPG1()
    #     print('\n',k)
    #     fpg.minimum_support = v[1]
    #     clean_dataset = fpg.run(v[0])
    #     fpg.build_tree(clean_dataset)
    #     fis = []
    #     fpg.mine_fis(fpg.header_table, set([]), fis)
    #     print(fis)
    #     fpg.display_info()
    #     del fpg

    for k, v in test.items():
        print("\n", k)
        fpg2 = FPG2(2)
        fpg2.create_tree(fpg2.modify_dataset(v[0]))
        fpg2.mine_tree(set([]), [])
        fpg2.display()