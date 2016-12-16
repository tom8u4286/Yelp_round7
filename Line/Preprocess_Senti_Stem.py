import sys, re
import time
from nltk.stem.snowball import SnowballStemmer

start_time = time.time()

"""load the review file. backend_reviews/restaurant_1.txt"""
review_f = open(sys.argv[1])
review_list = [review for review in review_f]
review_list_length = len(review_list)

"""load the lexiconfile. lexicon/stanfer/positive.txt"""
pos_f = open("../data/lexicon/stanfer/positive.txt")

pos_list = [word.strip("\n") for word in pos_f]

bi_words = []
uni_words = []
for word in pos_list:
    if "_" in word or "-" in word:
        bi_words.append(word)
    else:
        uni_words.append(word)
bi_words_length = len(bi_words)
uni_words_length = len(uni_words)



matched_cnt = 0
print "----------Bi-words and Uni-words----------"
print "Start processing bi-words..."
cnt_review = 1
review_list_bi = []
for review in review_list:
    new_review = ""
    """e.g. bi_word == 'well-crafted', bi_word_space == 'well crafted', bi_word_senti =='well-crafted_senti' """
    cnt_word = 1

    new_review = review
    for bi_word in bi_words:
        bi_word_space = ""
        if "-" in bi_word:
            bi_word_space = bi_word.replace("-"," ")
        else:
            bi_word_space = bi_word.replace("_"," ")
        bi_word_senti = " "+bi_word + "_senti "
        new_review = re.sub(" "+bi_word_space+" ", bi_word_senti, review)

        if review != new_review:
            #print "review:"+review
            #print "new:"+new_review
            matched_cnt += 1

        sys.stdout.write("\rtotally matched: %s, reviews: %s / %s, bi_words: %s / %s  "%(matched_cnt, cnt_review, review_list_length,cnt_word, bi_words_length))
        sys.stdout.flush()
        cnt_word += 1
    review_list_bi.append(new_review)
    cnt_review += 1

print "\nStart processing uni_words..."
review_list_bi_length = len(review_list_bi)
cnt_review = 1
new_review_list = []
for review in review_list_bi:
    new_review = ""
    cnt_word = 1
    new_review = review
    for uni_word in uni_words:
        uni_word_senti = " "+uni_word + "_senti "
        new_review = re.sub(" "+uni_word+" ", uni_word_senti, review)

        if review != new_review:
            print "review: "+review
            print "new: "+new_review
            matched_cnt +=1
        sys.stdout.write("\rtotally matched: %s, reviews: %s / %s, uni_words: %s / %s  "%(matched_cnt, cnt_review, review_list_bi_length,cnt_word, uni_words_length))
        sys.stdout.flush()
        cnt_word += 1

    new_review_list.append(new_review)
    cnt_review += 1

print "\nmatched count: %s"%matched_cnt

"""Write the new list to file."""
print "Start writing file..."
rest_num = re.search('[0-9]+',sys.argv[1]).group(0)
new_f = open("../data/backend_reviews_senti_stemmed/restaurant_%s_senti_stemmed.txt"%rest_num, 'w+')
for item in new_review_list:
    new_f.write("%s"%item)
new_f.close()

print "Total time: %s"%(time.time()- start_time)
print "Done."


