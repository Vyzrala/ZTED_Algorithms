from FP_Growth import FPG
from datasets import test

for k, v in test.items():
    fpg = FPG()
    print('\n',k)
    fpg.minimum_support = v[1]
    clean_dataset = fpg.run(v[0])
    fpg.build_tree(clean_dataset)
    fpg.display_info()
    fis = []
    fpg.mine_fis(fpg.header_table, fpg.minimum_support, set([]), fis)
    print(fis)
    del fpg