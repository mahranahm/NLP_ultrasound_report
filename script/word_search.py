import os

report = open("115O.txt")
report = report.read()
sentences_list = []
sentences_list = report.split(".")
word_search = "cecum"
word_sentence_dictionary = {"cecum":[]}
sentences_with_word = []


for word in word_search:
    sentences_with_word =[]
    for sentence in sentences_list:
        if sentence.count(word_search)>0:
            sentences_with_word.append(sentence)
        word_sentence_dictionary[word_search]= sentences_with_word

print (sentences_with_word)
