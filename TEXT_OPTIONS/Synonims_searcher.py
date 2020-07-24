import pickle
import time


word_base = pickle.load(open('word_base.dict', 'rb'))


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


word = input('Enter word: ')
start = time.monotonic()

syns = synonyms_searcher(word=word.lower(), word_base=word_base)
end = time.monotonic()

print('Найденные синонимы:', syns)
print("Исполнения команды заняло:", end - start)
