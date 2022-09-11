import os
import re
import string
import random
import argparse


class NGramModel:
    def __init__(self, filepath, save_path):
        self.filepath = filepath
        self.save_path = save_path
        self.ngram_dict_count = {}
        self.ngram_precedings_count = {}
        self.ngram_prob = {}
        self.sentences = self.load_sentences()


    def __init__(self, text, save_path):
        self.ngram_dict_count = {}
        self.save_path = save_path
        self.ngram_precedings_count = {}
        self.ngram_prob = {}
        self.sentences = self.load_sentences1(text)

    def specify_count_ngram(self, n):
        self.n = n

    def get_ngram(self, sentence, n):
        sentence = (n - 1) * ["<s>"] + sentence.split()
        ngrams = []
        precedings = []
        for i in range(n - 1, len(sentence)):
            prec = tuple(sentence[(i - n + 1):i])
            ngram = tuple([prec, sentence[i]])
            precedings.append(prec)
            ngrams.append(ngram)

        return ngrams, precedings

    def preprocess(self, sentence):
        r = re.compile("[а-яА-Я]+")
        sent = " ".join([s.translate(str.maketrans('', '', string.punctuation)) for s in sentence.split()])
        sent = sent.lower()
        sent = " ".join([w for w in filter(r.match, sent.split())])
        return sent

    def load_sentences1(self, text):
        corpus = ""
        corpus += text

        sentences = corpus.split('.')
        for i, sentence in enumerate(sentences):
            sentences[i] = self.preprocess(sentence)
        return sentences

    def load_sentences(self):
        corpus = ""
        if os.path.isfile(self.filepath):
            for f in os.listdir(self.filepath):
                if f.endswith("txt"):
                    with open(self.filepath) as f:
                        corpus += f.read().replace('\n', ' ').strip()
            sentences = corpus.split('.')
            for i, sentence in enumerate(sentences):
                sentences[i] = self.preprocess(sentence)
            return sentences

        else:
            raise argparse.ArgumentTypeError(f"readable_dir:{self.filepath} is not a valid path")

    def fit(self):
        ngram_dict_count = {}
        ngram_precedings_count = {}
        ngram_prob = {}

        for sentence in self.sentences:

            ngrams, precedings = self.get_ngram(sentence, n=self.n)

            for i in range(len(ngrams)):
                ngram = ngrams[i]
                prec = precedings[i]

                if ngram in ngram_dict_count:
                    ngram_dict_count[ngram] += 1
                else:
                    ngram_dict_count[ngram] = 1

                if prec in ngram_precedings_count:
                    ngram_precedings_count[prec] += 1
                else:
                    ngram_precedings_count[prec] = 1

        for ngram in ngram_dict_count.keys():
            prec = ngram[0]
            word = ngram[1]

            prob = ngram_dict_count[ngram] / ngram_precedings_count[ngram[0]]
            if prec in ngram_prob:
                ngram_prob[prec]['word'].append(word)
                ngram_prob[prec]['prob'].append(prob)

            else:
                ngram_prob[prec] = {'word': [word], 'prob': [prob]}

        self.ngram_dict_count = ngram_dict_count
        self.ngram_precedings_count = ngram_precedings_count
        self.ngram_prob = ngram_prob



    def generate(self, length):
        first_word_choice = self.ngram_prob[tuple((self.n - 1) * ["<s>"])]
        self.ngram_dict_count = {}
        self.ngram_precedings_count = {}
        self.ngram_prob = {}
        word_list = (self.n - 1) * ["<s>"] + [random.choices(first_word_choice['word'], first_word_choice['prob'])[0]]

        i = 1
        while i < length + self.n - 1:
            try:
                prec = word_list[i: self.n + i]
                word_choice = self.ngram_prob[tuple(prec)]
                generated_word = random.choices(word_choice['word'], word_choice['prob'])[0]
                word_list.append(generated_word)
                i += 1
            except:
                i += 1

        return " ".join(word_list[self.n - 1:])
