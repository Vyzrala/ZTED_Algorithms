from AprioriAll import AprioriAll
from datasets import aprioriAll_sets


def main():
    appAll = AprioriAll(0.25)
    appAll.run(aprioriAll_sets[0][0])
    del appAll


if __name__ == "__main__":
    main()

