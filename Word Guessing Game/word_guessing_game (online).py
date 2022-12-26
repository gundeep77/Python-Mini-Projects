import random
import pyrebase
from config import config

start = pyrebase.initialize_app(config)
rdb = start.database()
data = rdb.get()
data_to_dict = dict(data.val())
words = set(data_to_dict.keys())

print("\n\n\n\n\t\t\t********** WORD GUESSING GAME **********\n")
print("\t\t\tYou have 10 guesses to fill the following blanks to make a meaningful word.\n")

while True:
    hangman = random.choice(list(words))
    attempts = 10
    lst = ['_']*len(hangman)
    used = []
    print("\t\t\t" + " ".join(lst) + '\n')
    while attempts != 0:
        inp = input("\t\t\tGuess a letter: ")
        if inp.isalpha() and len(inp) == 1:
            if inp in used:
                print("\t\t\tYou have already tried this letter!\n")
                continue
            if inp in hangman:
                for i in range(len(hangman)):
                    if hangman[i] == inp:
                        lst[i] = inp
                print("\t\t\t" + " ".join(lst) + '\n')
                used.append(inp)
                if "_" not in lst:
                    break
            else:
                attempts -= 1
                print("\t\t\tWrong!")
                print(f"\t\t\tAttempts remaining: {attempts}")
                print("\t\t\t" + " ".join(lst) + '\n')
                used.append(inp)
        else:
            print("\t\t\tYou can enter only a single letter!\n")

    if "".join(lst) == hangman:
        print("\t\t\tCongrats, you did it!!")
    else:
        print("\t\t\tSorry! Better luck next time!")
        print(f"\t\t\tThe word is '{hangman}'")

    print(f"\t\t\tYou took {10-attempts} out of 10 attempts.\n")

    more = input("\t\t\tWanna play more?(y/n): ")
    if more == 'y':
        print()
        continue
    else:
        print()
        print("\t\t\tThanks for playing!")
        x = input("\t\t\tPress enter to exit...\n")
        break