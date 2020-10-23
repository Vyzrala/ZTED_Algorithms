from Apriori import Apriori

if __name__ == "__main__":

    translation = {
        'i1':'chleb',
        'i2':'piwo',
        'i3':'paluszki',
        'i4':'śledź',
        'i5':'chipsy',
        'i6':'masło',
        'M':'Mango',
        'O':'Onion',
        'N':'Nintendo',
        'K':'Key-chain',
        'E':'Eggs',
        'Y':'Yo-yo',
        'D':'Doll',
        'A':'Apple',
        'U':'Umbrella',
        'C':'Corn',
        'I':'Ice-cream',
    }

    set1 = [  
        ['i2','i3','i4'],
        ['i1','i2','i5'],
        ['i2','i3','i5'],
        ['i1','i2','i4'],
        ['i2','i3','i5','i6'],
        ['i2','i4','i6'],
        ['i1','i4','i5'],
        ['i2','i3','i5'],
        ['i1','i2','i6'],
        ['i2','i4','i6'],
        ['i3','i5','i6']
    ]

    set2 = [  
        ['i1','i2','i5'],
        ['i2','i4'],
        ['i2','i3'],
        ['i1','i2','i4'],
        ['i1','i3'],
        ['i2','i3'],
        ['i1','i3'],
        ['i1','i2','i3','i5'],
        ['i1','i2','i3']
    ]
    
    set3 = [
        ['M', 'O', 'N', 'K', 'E', 'Y'],
        ['D', 'O', 'N', 'K', 'E', 'Y'],
        ['M', 'A', 'K', 'E'],
        ['M', 'U', 'C', 'K', 'Y'],
        ['C', 'O', 'O', 'K', 'I', 'E']
    ]

    #  Dict structure:
    #  'set name' : ['specific set', 'minimum support level']
    sets = {  
        'set1':[set1, 2],
        'set2':[set2, 2],
        'set3':[set3, 3],
    }
    
    print("\nRunning example session...")

    for k, v in sets.items():
        print("\n\nDataset {}, minimum support = {}:\n".format(k, v[1]))
        print(*v[0], sep='\n', end='\n\n')
        last_L = Apriori(v[1]).run(v[0])

        print("Translation:")
        for k in last_L:
            print(list(map(lambda x:translation.get(x, x), k)))

    print("\n\nEnd session...\n")
