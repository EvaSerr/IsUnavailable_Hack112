from PyDictionary import PyDictionary
dictionary = PyDictionary()

from pattern.en import conjugate, lemma, lexeme

import string, nltk, random
from pluralizer import Pluralizer
pluralizer = Pluralizer()
# from nltk import word_tokenizei
nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')

from nltk import pos_tag

def GETSIMP(pos):
    if pos[0:2] == 'NN': # is noun?
        simpPos = 'NN'
        plural = False
        cap = False
        if 'S' in pos:
            plural = True
        if 'P' in pos:
            cap = True
        return simpPos, plural, cap
    elif pos[0:2] == 'JJ': # is adjective?
        simpPos = 'JJ'
        comp = False
        sup = False
        if 'R' in pos:
            comp = True
        if 'S' in pos:
            sup = True
        return simpPos, comp, sup
    
def posAdjustment(word, classification):
    simpPos = classification[0]
    if simpPos == 'NN':
        plural, cap = classification[1], classification[2]
        if plural:
            word = pluralizer.pluralize(word)
        if cap:
            word = word[0].upper() + word[1:]
    elif simpPos == 'JJ':
        comp, sup = classification[1], classification[2]
        if comp:
            word += 'er'
        if sup:
            word += 'est'
    return word

def verbConjugation(pos, word):
    if pos == 'VB':
        return word
    elif pos == 'VBD': 
        conjWord = conjugate(word, tense='past')
    elif pos == 'VBG':
        conjWord = conjugate(word, tense='present', aspect='progressive')
    elif pos == 'VBN':
        conjWord = conjugate(word, tense='past', aspect='progressive')
    elif pos == 'VBP':
        conjWord = conjugate(word, tense='present', person='1', number='sg')
    elif pos == 'VBZ':
        conjWord = conjugate(word, tense='present', person='3', number='sg')
    return conjWord

def crayonify(s):
    inp = s
    inp = inp.split()
    taggedInp = pos_tag(inp)
    resultString = ''
    isPunc = False
    punc = ''
    for word, pos in taggedInp:
        inpWord = word
        for char in word:
            if char in string.punctuation:
                isPunc = True
                punc = char
        if pos[0:2] == 'VB':
            inpWord = lemma(word)
        allSyns = dictionary.synonym(inpWord)
        if allSyns:
            allSynsPos = pos_tag(allSyns)
            syns = []
            if pos[0:2] == 'VB':
                simpPos = pos[0:2]
            elif pos[0:2] not in {'JJ', 'NN'}:
                simpPos = pos
            else:
                classification = GETSIMP(pos)
                simpPos = classification[0]
            if simpPos != None:
                refPos = simpPos
            for synWord, synPos in allSynsPos:
                if refPos in synPos:
                    syns.append(synWord)
            if refPos == 'VB':
                syn = syns[random.randint(0, len(syns)-1)]
                syn = verbConjugation(pos, syn)
                if syn == None:
                    syn = syns[random.randint(0, len(syns)-1)]
                    syn = conjugate(syn, tag='vbp')
            elif refPos not in {'JJ', 'NN'} or len(syns) == 0:
                syn = word
            else:
                syn = syns[random.randint(0, len(syns)-1)]
        else:
            syn = word

        resultString += syn + punc + ' '
        
    print(resultString.strip())
    return resultString.strip()

'''
    JJ	adjective	'big'
    JJR	adjective, comparative	'bigger'
    JJS	adjective, superlative	'biggest'
    NN	noun, singular 'desk'
    NNS	noun plural	'desks'
    NNP	proper noun, singular	'Harrison'
    NNPS	proper noun, plural	'Americans'
    VB	verb, base form	take
    VBD	verb, past tense	took
    VBG	verb, gerund/present participle	taking
    VBN	verb, past participle	taken
    VBP	verb, sing. present, non-3d	take
    VBZ	verb, 3rd person sing. present	takes
    PRP$ possessive pronoun	my, his, hers
'''

'''
user inputs text

translate:

dictionary translation:
    -separate into words
    -determine part of speech
    -find synonyms for words (if not proper noun (NNP, NNPS)
                                **if no plural syn in library**
                                    find singular syn and then DIY pluralize
                                        (add 's'))
        -make sure it's the same part of speech
    -re-construct phrase with synonyms


Output:

convert text into images - makea dictionary mapping each char to each image?
depending on how long the new text is:
    -cell size
    -maybe edit cell size according to input length
        -whitespace
split it up into mulitple lines
output the image    
'''