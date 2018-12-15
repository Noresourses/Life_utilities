import csv
import unidecode
from string import ascii_lowercase
# The possible accents
ACCENTS = {
    u'ά': u'α', u'Ά': u'Α',
    u'έ': u'ε', u'Έ': u'Ε',
    u'ή': u'η', u'Ή': u'Η',
    u'ί': u'ι', u'Ί': u'Ι',
    u'ϊ':u'ι',u'`':u'',
    u'ύ': u'υ', u'Ύ': u'Υ',
    u'ό': u'ο', u'Ό': u'Ο',
    u'ώ': u'ω', u'Ώ': u'Ω',
}

Gr_dict = {
	u'α':0,
	u'β':1,
	u'γ':2,
	u'δ':3,
	u'ε':4,
	u'ζ':5,
	u'η':6,
	u'θ':7,
	u'ι':8,
	u'κ':9,
	u'λ':10,
	u'μ':11,
	u'ν':12,
	u'ξ':13,
	u'ο':14,
	u'π':15,
	u'ρ':16,
	u'σ':17,
    u'ς':17,
	u'τ':18,
	u'υ':19,
	u'φ':20,
	u'χ':21,
	u'ψ':22,
	u'ω':23,
}

def remove_accent_chars(word):
    for accent_char in ACCENTS:
        word = word.replace(accent_char, ACCENTS[accent_char])
    return word


LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=0)}

def alphabet_position(text):
    text = text.lower()

    numbers = [int(LETTERS[character]) for character in text if character in LETTERS]

    return numbers

with open('gr_eng.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # skip the headers
    for row in reader:
        try: # skip the english to english
            # Remove the accents
            gr = remove_accent_chars(row[0])
            # Alphabet to number
            eng = unidecode.unidecode(row[1])
            # Encode the words to vectors

            gr_enc = [str(gr.count(ch)) for ch in Gr_dict.keys()]
            #gr_enc = ['0' if i not in  [Gr_dict[ch.lower()] for ch in gr] else '1' for i in range(0, 24)]
            eng_enc = [str(eng.count(ch)) for ch in list(ascii_lowercase)]

            #eng_enc = ['0' if i not in alphabet_position(eng) else '1' for i in range(0, 26)]
            # Write the vectors to the new csv
            with open('vectors.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', )
                writer.writerow([''.join(gr_enc),''.join(eng_enc)])
        except KeyError:
            continue



