#!/usr/bin/env python3

import sys
import argparse
parser = argparse.ArgumentParser(description="Look for words that are valid with recursive letter removal")
parser.add_argument("-v", "--verbose",    help="Print verbose trace", action="store_true")
parser.add_argument("-d", "--dictionary", help="Dictionary file", nargs='?', type=argparse.FileType('r'), default="/usr/share/dict/words")
parser.add_argument("-p", "--proof",      help="Show proof of the word breakdown", action="store_true")
parser.add_argument("-a", "--allow-all",  help="Allow all single letters - strangely all letters are a word according to the unix dictionary", action="store_true", default=False)
parser.add_argument("-n", "--names",      help="Allow names (words starting with caps other than I)", action="store_true", default=False)
parser.add_argument("words", nargs="*", help="Only check these words for pluckability")
args = parser.parse_args()

f = args.dictionary
word = {}
wordlist = []
for w in f.readlines():
    chop = w.rstrip(" \n\r")
    if len(chop) < 1:
        continue
    if len(chop) == 1:
        if not args.allow_all and chop not in ["I","a"]:
            continue
    if chop[0].isupper() and not args.names:
        if chop != "I":
            continue
    word[chop.lower()] = chop
    wordlist.append(chop)
f.close()

cache = {}
proof = {}
def pluckable(s):
    if args.verbose: print("is %s pluckable?"%(s,))
    if cache.get(s):
        if args.verbose: print("is %s pluckable? cached=%s"%(s,cache[s]))
        return cache[s]
    if len(s) < 1:
        if args.verbose: print("is %s pluckable? zero len"%(s,))
        return True
    if not word.get(s,False):
        if args.verbose: print("is %s pluckable? not a word"%(s,))
        return False
    found = False
    for i in range(0,len(s)):
        w = s[0:i]+s[i+1:]
        p = pluckable(w)
        if p and len(w) > 0:
            if not proof.get(s):
                proof[s] = []
            proof[s].append(w)
        found = found or p
    cache[s] = found
    if args.verbose: print("is %s pluckable? %s"%(s,found))
    return found

def prove(s, depth=1):
    if not proof.get(s):
        return
    for p in proof[s]:
        print("%s%s"%(" "*depth,word[p]))
        prove(p,depth+1)

words = args.words or wordlist
for w in words:
    chop = w.rstrip(" \n\r")
    if pluckable(chop.lower()):
        print(chop)
        if args.proof:
            prove(chop)
f.close()
