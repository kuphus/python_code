vowels = ['a', 'e', 'i', 'o', 'u']
found = {}

word = input("Provide a word to search for vowels: ")

for letter in word:
    if letter in vowels:
        #if letter not in found:
        #    found[letter]=1
        #else:
        #    found[letter] += 1

        #handigere methode
        found.setdefault(letter, 0)
        found[letter] += 1


#for letter in found:
print(found)




#### version 2
word = input("Provide a word to search for vowels: ")


print(vowels.intersection(set(word)))