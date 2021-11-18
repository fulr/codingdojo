import string
import math

filename = 'dev.csv'
stopwords = 'stopwords.txt'

word_count = dict()
stopword_list = list()

word_count_per_book = dict()

with open(stopwords, 'r', encoding='utf-8') as file:
    for w in file:
        stopword_list.append(w.strip())
    stopword_list = stopword_list+[s[0].upper()+s[1:]
                                   for s in stopword_list]+['']

punct = string.punctuation+'…–'

with open(filename, 'rb') as file:
    for line in file:
        line = line.decode('utf-8').strip()
        isbn = line.split('#')[0]
        klappentext = line.split('#')[3]
        word_count_per_book[isbn] = {}
        for c in punct:
            klappentext = klappentext.replace(c, ' ')
        for word in klappentext.split(' '):
            if word in stopword_list:
                continue
            word_count.setdefault(word, 0)
            word_count[word] += 1
            word_count_per_book[isbn].setdefault(word, 0)
            word_count_per_book[isbn][word] += 1

sorted_count = sorted(word_count.items(), key=lambda x: x[1])

print(sorted_count[-10:])

b = len(word_count_per_book)

print('Gesamt B = ', b)


def df(t, b):
    c = 0
    for k, v in b.items():
        if t in v:
            c += 1
    return c


print('DF(Liebe,B) = ', df('Liebe', word_count_per_book))
print('DF(liebe,B) = ', df('liebe', word_count_per_book))


def tf(t, d):
    return d.get(t, 0)/max([v for _, v in d.items()])


def idf(t, b):
    return math.log((len(b)+1)/(df(t, b)+1))


print('TF(Liebe, 9783442376599) = ', tf(
    'Liebe', word_count_per_book['9783442376599']))

print('TF(liebe, 9783453418554) = ', tf(
    'liebe', word_count_per_book['9783453418554']))

for isbn, book in word_count_per_book.items():
    for word in book.keys():
        t = tf(word, book)
        i = idf(word, word_count_per_book)
        print(isbn, word, t, i, t*i)
    break
