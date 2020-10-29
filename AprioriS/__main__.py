from AprioriS import AprioriS
from datasets import aprioriS_sets

if __name__ == '__main__':

    for dataset, sup in aprioriS_sets:
        print('\nStart:')
        aprs = AprioriS(sup)
        aprs.run(dataset)
        print('End\n')
