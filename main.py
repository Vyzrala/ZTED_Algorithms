from FP_Growth import FPG
from datasets import test

for k, v in test.items():
    fpg = FPG()
    print('\n',k)
    fpg.minimum_support = v[1]
    clean_dataset = fpg.run(v[0])
    fpg.build_tree(clean_dataset)
    fpg.generate_cond_pattern_base()
    fpg.display_info()
    del fpg