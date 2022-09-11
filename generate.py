
import argparse
from sys import stdin

from main import NGramModel


def createParser():
    pars = argparse.ArgumentParser()
    pars.add_argument('--model')
    pars.add_argument('--prefix', nargs='?')
    pars.add_argument('--length')
    return pars





def get_data_stdin():
    r = []
    for line in stdin:
        r.append(line.rstrip())

    model = NGramModel(" ".join(r))
    model.specify_count_ngram(3)


def read_data():
    parser = createParser()
    namespace = parser.parse_args()

    if namespace.input_dir:



data = read_data()











#model.fit()
#print(model.generate(3))