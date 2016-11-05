import gensim

model = gensim.models.Word2Vec.load_word2vec_format('../yelp/GoogleNews-vectors-negative300.bin', binary=True)
unique_words = list(model.vocab)
print unique_words

with open("../../data/unique_words.txt", "w+") as f:
    for word in unique_words:
        f.write( word.encode('utf8') + "\n")


model.save_word2vec_format('./GoogleNews-vectors-negative300.txt', binary=False)

