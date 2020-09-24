import nltk
#nltk.download('punkt')
import sys
from nltk.tokenize import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP| S Conj S | S NP| S VP | S NP NP | S NP NP

NP -> N | Det N | Det AD N | PP N | AD N | Det N PP | N VP | COJ N | N Adv | N VP

VP -> V | V  NP | V ADV | V AD | V NP PP | V PP | P V | V NP NP | Conj V

PP -> P | P NP | NP P |P Det | PP

AD -> Adj | Det Adj | Det Adj Adj | Det Adj Adj Adj | Adj Conj Adj

ADV -> Adv | NP Adv | adv NP

CONJ -> Conj | Conj Det | Conj P | Conj Adv | Conj S
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    print()
    print(sentence)


    token_sentence = word_tokenize(sentence)

    print(f"token_sentence: {token_sentence} \n")

    tokenized_word_list = []

    for char in token_sentence:
        if char.isalpha():
            char = char.lower()
            tokenized_word_list.append(char)


    print(f"tokenized_word_list: {tokenized_word_list} \n")

    return tokenized_word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """



    #print(tree.label())
    print()
    #subtrees = tree.subtrees(lambda t)
    np_chunks = []

    #filter subtrees for lables with NP
    for subtree in tree.subtrees(lambda subtree: subtree.label() == "NP"):

        # if no subtrees that also have label NP then append
        if not has_np(subtree):
            np_chunks.append(subtree)

    return np_chunks

def has_np(subtree):
    for subsubtree in subtree.subtrees():
        if subsubtree == subtree:
            continue
        elif subsubtree.label() == "NP":
            return True

    return False

if __name__ == "__main__":
    main()
