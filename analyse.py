import codecs
import string
import time

import feedparser
import matplotlib.pyplot as plt
import numpy as np
import tamil.utf8 as utf8
from tabulate import tabulate

tabulate.WIDE_CHARS_MODE = False


def column(matrix, i):
    return [row[i] for row in matrix]


def parseXML(feedURL):
    data = feedparser.parse(feedURL)
    return [post.title for post in data.entries]


def tamilAnalyse(titles):
    detailsTable = []
    for title in titles:
        letters = utf8.get_letters(title)
        words = utf8.get_words(letters)
        wordCount = len(words)
        letterCount = len(letters) - letters.count(' ')
        detailsTable.append([wordCount, letterCount])

    return detailsTable


def genericAnalyse(titles):
    detailsTable = []
    for title in titles:
        title.translate(str.maketrans('', '', string.punctuation))
        detailsTable.append([len(title.split()), len(title) - title.count(' ')])

    return detailsTable


def analyse(language, rssFeed):
    titles = parseXML(rssFeed)
    details = []

    if language == "tamil":
        details = tamilAnalyse(titles)
    elif language == "english":
        details = genericAnalyse(titles)
    elif language == "german":
        details = genericAnalyse(titles)
    else:
        print("Language not supported")

    letters = np.array(column(details, 1))
    words = np.array(column(details, 0))
    avgLetters = int(np.mean(letters))
    avgWords = int(np.mean(words))

    f = codecs.open('{}_dump.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("Language : {}, Source RSS Link : {}".format(language.title(), rssFeed), file=f)
    print("Headlines : ", file=f)
    for title in titles:
        print(title, file=f)
    print(tabulate(details, headers=["Word count", "Letter count"], tablefmt="grid", numalign="right"), file=f)
    f.close()

    f = codecs.open('{}_Analysis.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("\n\nLanguage : {}, Source RSS Link : {}".format(language.title(), rssFeed), file=f)
    print('+' + '-' * 45 + '+', file=f)
    print("|  Average Word count  | Average Letter count |", file=f)
    print('+' + '-' * 45 + '+', file=f)
    print("|{0:^22d}|{1:^22d}|".format(avgWords, avgLetters), file=f)
    print('+' + '-' * 45 + '+', file=f)
    f.close()

    fig, ax = plt.subplots()
    data_line = ax.plot(words, label='Number of Words', marker='o')
    mean_line = ax.axhline(avgWords, color='r', label='Mean', linestyle='--')
    legend = ax.legend(loc='upper right')

    plt.savefig("Graph_{}.png".format(language))




def main():
    rssList = {}
    with open("input.txt") as f:
        for line in f.readlines():
            text = line.split()
            rssList[text[0]] = text[1]

    for key in rssList.keys():
        analyse(key, rssList[key])


if __name__ == "__main__":
    main()
