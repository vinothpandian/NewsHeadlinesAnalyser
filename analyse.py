import codecs
import string
import time

import feedparser
import tamil.utf8 as utf8
from tabulate import tabulate

tabulate.WIDE_CHARS_MODE = False



def parseXML(feedURL):
    data = feedparser.parse(feedURL)
    return [post.title for post in data.entries]


def tamilAnalyse(titles):
    detailsTable = []
    avgWordCount = 0
    avgLetterCount = 0
    for title in titles:
        letters = utf8.get_letters(title)
        words = utf8.get_words(letters)
        wordCount = len(words)
        letterCount = len(letters) - letters.count(' ')
        detailsTable.append([wordCount, letterCount])
        avgWordCount += wordCount
        avgLetterCount += letterCount

    return [detailsTable, avgWordCount / len(titles), avgLetterCount / len(titles)]


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

    f = codecs.open('{}_dump.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("Language : {}, Source RSS Link : {}".format(language.title(), rssFeed), file=f)
    print("Headlines : ", file=f)
    for title in titles:
        print(title, file=f)
    print(tabulate(details[0], headers=["Word count", "Letter count"], tablefmt="grid", numalign="right"), file=f)
    f.close()

    f = codecs.open('{}_Analysis.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("\n\nLanguage : {}, Source RSS Link : {}".format(language.title(), rssFeed), file=f)
    print('+' + '-' * 45 + '+', file=f)
    print("|  Average Word count  | Average Letter count |", file=f)
    print('+' + '-' * 45 + '+', file=f)
    print("|{0:^22d}|{1:^22d}|".format(int(details[1]), int(details[2])), file=f)
    print('+' + '-' * 45 + '+', file=f)
    f.close()


def main():
    rssList = {}
    with open("inputO.txt") as f:
        for line in f.readlines():
            text = line.split()
            rssList[text[0]] = text[1]

    for key in rssList.keys():
        analyse(key, rssList[key])


if __name__ == "__main__":
    main()
