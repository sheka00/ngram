import argparse
from sys import stdin

from main import NGramModel


def createParser():
    pars = argparse.ArgumentParser()
    pars.add_argument('--input-dir', nargs='?')
    pars.add_argument('--model`')
    return pars


def dir_path(path, save_path):
    model = NGramModel(path, save_path)
    model.specify_count_ngram(3)


def get_data_stdin(save_path):
    r = []
    for line in stdin:
        r.append(line.rstrip())

    model = NGramModel(" ".join(r), save_path)
    model.specify_count_ngram(3)


def read_data():
    parser = createParser()
    namespace = parser.parse_args()

    if namespace.input_dir:
        dir_path(namespace.input_dir, namespace.save_path)
    else:
        get_data_stdin(namespace.save_path)


data = read_data()
