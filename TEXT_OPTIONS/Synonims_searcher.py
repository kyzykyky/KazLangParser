import pickle
import time


word_base = pickle.load(open('word_base.dict', 'rb'))
abbreviation_base = pickle.load(open('abbreviation_base.dict', 'rb'))


def synonyms_searcher(word, word_base):
    synonims_block = []
    c = False
    for w in word_base:
        for ww in word_base[w]:
            if ww == word:  # Mod Req
                c = True
                synonims_block.append(word_base[w])
    if c:
        return synonims_block
    return 'Совпадений нет'


def abbreviation_searcher(word, word_base):
    abbreviation_block = []
    c = False
    for w in word_base:
        for ww in word_base[w]:
            if ww.lower() == word or ww.lower() == w.lower():  # Mod Req
                c = True
                t = word_base[w].copy()
                t.append(w)
                abbreviation_block.append(t)
    if c:
        return abbreviation_block
    return 'Совпадений нет'


word = input('Enter word: ')
start = time.monotonic()

syns = synonyms_searcher(word=word.lower(), word_base=word_base)
abb = abbreviation_searcher(word=word.lower(), word_base=abbreviation_base)

end = time.monotonic()

print('Найденные синонимы:', syns)
print('Найденные аббревиатуры:', abb)
print("Исполнения команды заняло:", end - start)
