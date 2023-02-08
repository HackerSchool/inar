import spacy

# ---------------- Pre-processing ---------------
#https://pyspellchecker.readthedocs.io/en/latest/

from spellchecker import SpellChecker

spell = SpellChecker()

def correct_text(text):
    corrected_text = []
    phrase = text.split()
    for word in phrase:
        print(word)
        corrected_word = spell.correction(word)
        print(corrected_word)
        corrected_text.append(corrected_word)
    return " ".join(corrected_text)

#testing
phrase = "hell my neme is Rita. I am portgese"
print(correct_text(phrase))

# ------------------ Correct words according to context --------

#https://spacy.io/usage/spacy-101

nlp = spacy.load("en_core_web_sm")

def answer_generate(user_input):
    doc = nlp(user_input)

    for token in doc:
        #print(token.text, token.pos_, token.dep_)
        if token.text.lower() in ("hello"):
            print("Hi there!")


answer_generate("Apple is looking at buying U.K. startup for $1 billion")
answer_generate("Hello there! My name is Rita")