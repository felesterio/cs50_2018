import crypt
import sys


def main():
    # obligatory comments for style50
    # style50 crack.pyno arguement given
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} hash')
        return 1

    hash_ = sys.argv[1]
    salt = hash_[0:2]

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # for two letter password
    for letter1 in alphabet:
        for letter2 in alphabet:
            guess = letter1 + letter2
            check = crypt.crypt(guess, salt)
            if check == hash_:
                print(f"{guess}")
                return 0
    # for three letter password
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                guess = letter1 + letter2 + letter3
                check = crypt.crypt(guess, salt)
                if check == hash_:
                    print(f"{guess}")
                    return 0
    # for four letter passwrod
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                for letter4 in alphabet:
                    guess = letter1 + letter2 + letter3 + letter4
                    check = crypt.crypt(guess, salt)
                    if check == hash_:
                        print(f"{guess}")
                        return 0
    # for 5 letter password
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                for letter4 in alphabet:
                    for letter5 in alphabet:
                        guess = letter1 + letter2 + letter3 + letter4 + letter5
                        check = crypt.crypt(guess, salt)
                        if check == hash_:
                            print(f"{guess}")
                            return 0


if __name__ == "__main__":
    main()