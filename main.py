from FP_Growth import FPG
from FP_Growth.FPGrowth2 import FPG as FPG2
from datasets import test

for k, v in test.items():
    fpg2 = FPG2(2)
    fpg2.create_tree(v[0])
    fis = []
    fpg2.mine_tree(set([]), fis)
    fpg2.display()
# for k, v in test.items():
#     fpg = FPG()
#     print('\n',k)
#     fpg.minimum_support = v[1]
#     clean_dataset = fpg.run(v[0])
#     fpg.build_tree(clean_dataset)
#     fis = []
#     fpg.mine_fis(1, fpg.header_table, set([]), fis)
#     # fpg.get_CPB("S")
#     # print(fis)
#     fpg.display_info()
#     del fpg
