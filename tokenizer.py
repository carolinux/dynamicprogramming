from collections import defaultdict

"""Tokenize a sentece according to a dictionary. Includes an implementation of Prefix Tree"""

__author__=="Karolina Alexiou"""
__email__=="carolinegr@gmail.com"

class PrefixNode:

    #TODO a maxdepth here would optimize things

    def __init__(self, isWord=False):
        self.isWord = isWord
        self.children = {}

    def getChild(self,char):
        if char in self.children.keys():
            return self.children[char]
        else:
            return None

    def createAndGetChild(self, char):
        if char in self.children.keys():
            return self.children[char]
        else:
            self.children[char] = PrefixNode()
            return self.children[char]

    def setWord(self):
        self.isWord = True

    def hasChildren(self):
        return len(children)!=0

def searchTree(root, word, mustBeWord =True):
    """Returns a boolean whether a word or prefix is in the prefix tree or not"""
    curr_node = root
    prefix = ""
    word_idx = 0
    while(True):
        char = word[word_idx]
        #None semantics maybe not ideal FIXME
        if curr_node.getChild(char) is None:
            return False
        else:
            curr_node = curr_node.getChild(char)
            word_idx+=1
        if word_idx == len(word):
            if mustBeWord:
                return curr_node.isWord
            else:
                return True

def buildPrefixTreeFromSortedWords(words):
    pass

def buildPrefixTree(words):
    """Builds a prefix tree from an iterable of words and returns the root"""
    root = PrefixNode(isWord=False)
    for word in words:
        characters = list(word)
        curr_node = root
        for i,char in enumerate(characters):
            curr_node = curr_node.createAndGetChild(char)
            # the if is possibly inefficient because of branching FIXME
            if i == len(characters)-1:
                curr_node.setWord()

    return root

def tokenize(sentence, words):
    """sentence is a sentence without blanks or punctuation and one must exact the words"""
    tree = buildPrefixTree(words)
    max_len = max(map(len,words))
    # data structure to hold whether we have an end of word before a given index
    eow_at_index = [False for i in range(len(sentence))]
    # end of word mapping to valid starts of word
    eow_to_sow = defaultdict(list)
    for i in range(len(sentence)):
        if i>0 and not eow_at_index[i-1]:
            continue
        # find if I can have a word from i to i + something, then update dedicated data structure
        for j in range(1,max_len):
            if i+j>len(sentence):
                break
            candidate_word = sentence[i:i+j]
            found = searchTree(tree,candidate_word)
            if found == True:
                eow_at_index[i+j-1] = True
                eow_to_sow[i+j-1].append(i)

    if eow_at_index[-1] == False:
        print "Could not tokenize"
        print eow_at_index
        return None
    else:
        # rebuild the sentence
        # return one possible tokenization
        eow = len(sentence)-1
        tokens = []
        while(True):
            sow = eow_to_sow[eow][0] # here we could choose a different index (if available) to get a different tokenization
            tokens.append(sentence[sow:eow+1])
            eow = sow -1
            if eow<0:
                break
        tokens.reverse()
        return " ".join(tokens)

if __name__=="__main__":
    words = ["words","that","in","the","quick","brown","fox","jumped","over","lazy","dog","lazydog","ox","bro","lemon","lemonade","parachute","b","zebra","spider","too","pest"]
    tree = buildPrefixTree(words)
    for word in words:
        assert(searchTree(tree,word) == True)
    assert(searchTree(tree,"er") == False)
    assert(tokenize("thelemonadespidertoo",words)=="the lemonade spider too")
    assert(tokenize("jumpedoverthelazydog",words)=="jumped over the lazydog")
    assert(tokenize("wordsthatdontexistindictionary", words) is None)
