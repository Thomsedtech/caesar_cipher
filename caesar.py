# Caesar cipher project
"""
Converts text to Caesar enciphered text, in all caps.
Takes CSV as input: -i cleartext.csv
Outputs 2 CSV files, 1 with cipher text (cleartext_cipher.csv), and an index with solutions and key (cleartext_cheat)
Options:
-k specify key (1-25)
-b produce cipher in blocks of 5 letters

"""
import argparse
import random
import csv

parser = argparse.ArgumentParser(description='Creates Caesar ciphers. [-k] specify key')
parser.add_argument('-k', type=int,  help='add key - if absent, random key is generated')
parser.add_argument('-b', default=False, action="store_true", help='blocks ciphertext in groups of 5 characters')
parser.add_argument('-i', required=True, type=str, help='name of input file')
args = parser.parse_args()


def main():
    # get message

    message = "This message to be encrypted."
    infile = args.i
    outfile = args.i
    cheat = args.i
    outfile = outfile.replace(".csv", "")+"_cipher.csv"
    cheat = cheat.replace(".csv", "")+"_cheat.csv"
    with open(infile, newline='') as input, open(outfile, "w", encoding='utf-8') as output, open(cheat, "w", encoding='utf-8') as teacher:
        clear = csv.reader(input, delimiter ="|")
        cipher = csv.writer(output, delimiter =",", quoting=csv.QUOTE_MINIMAL)
        cheat = csv.writer(teacher, delimiter =",", quoting=csv.QUOTE_MINIMAL)
        for index, line in enumerate(clear):
            key = getKey()
            strIndex = str(index)
            cipher_answer = [str(index)]+[caesar(line,key)]
            cheat_answer = [str(index)] + [cleanup(str(line))] + [str(key)]
            cipher.writerow(cipher_answer)
            cheat.writerow(cheat_answer)

def getKey():
    if args.k:
        key = args.k
    else:
        key = random.randint(1,25)
    return key

def cleanup(message):
    message = str(message).upper()
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    cleaned = ''
    for char in message:
        if char in SYMBOLS:
            cleaned += char
    return cleaned

def caesar(message,key):
    caesared = ''
    message = str(message).upper()
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for symbol in message:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            # Encrypt character
            caesaredIndex = symbolIndex + key
            if caesaredIndex >= len(SYMBOLS):
                caesaredIndex = caesaredIndex - len(SYMBOLS)
                # print("trans Index" + str(caesaredIndex))
            elif caesaredIndex < 0:
                caesaredIndex = caesaredIndex + len(SYMBOLS)
                # print("trans Index" + str(caesaredIndex))
            caesared = caesared + SYMBOLS[caesaredIndex]
        else:
            # Keep symbols not in SYMBOLS
            caesared = caesared + symbol
    if args.b:
        caesared = blocked(caesared)
    return caesared

def blocked(s):
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    noSpace = s.replace(" ","")
    blocked = ''
    i = 1
    for char in noSpace:
        if i % 5 == 0:
            blocked = blocked + char + ' '
            i += 1
        elif char not in SYMBOLS:
            continue
        else:
            blocked = blocked +char
            i += 1
    return blocked

if __name__ == "__main__":
    main()

"""
Credits:
Structure for translate() function inspired by Al Sweigart's code,
found in Cracking Codes with Python.

"""
