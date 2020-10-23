from Apriori import Apriori
from datasets import test, translation

if __name__ == "__main__":
    print("\nRunning example session...")

    for k, v in test.items():
        print("\n\nDataset {}, minimum support = {}:\n".format(k, v[1]))
        print(*v[0], sep='\n', end='\n\n')
        last_L = Apriori(v[1]).run(v[0])

        print("Translation:")
        for k in last_L:
            print(list(map(lambda x:translation.get(x, x), k)))

    print("\n\nEnd session...\n")
