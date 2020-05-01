def symbol_counter(text):
    char_count = 0
    word_count = 0
    for word in text:
        word_count += 1
        for char in word:
            char_count += 1
    print('Words:', word_count)
    print('Chars:', char_count)


f = open('FullMedicineBlock.txt', 'r', encoding='utf-8')
print('This text has:')
symbol_counter(f)
f.close()
