import codecs
import string
import time

import feedparser
import matplotlib.pyplot as plt
import numpy as np
import tamil.utf8 as utf8


def display(results):
    f = codecs.open('{}_Analysis.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("__Author: Vinoth__", file=f)
    f.close()

    f = codecs.open('{}_dump.txt'.format(time.strftime("%d-%m-%Y")), 'w', 'utf-8')
    print("__Author: Vinoth__", file=f)
    f.close()

    for result in results:
        language = result[0]
        rssFeed = result[1]
        titles = result[2]
        details = [result[3], result[4]]
        titleCount = 0

        letters = np.array(details[0])
        words = np.array(details[1])
        avgLetters = np.mean(letters)
        avgWords = np.mean(words)

        f = codecs.open('{}_dump.txt'.format(time.strftime("%d-%m-%Y")), 'a', 'utf-8')
        print("\n\nLanguage : {}".format(language), file=f)
        print("Source RSS Feeds:", file=f)
        for feedURL in rssFeed:
            print(feedURL, file=f)
        print("Headlines : ", file=f)
        for title in titles:
            titleCount += len(title)
            for headline in title:
                print(headline, file=f)
        print("Letter Count", file=f)
        print(letters, file=f)
        print("Word Count", file=f)
        print(words, file=f)
        f.close()

        f = codecs.open('{}_Analysis.txt'.format(time.strftime("%d-%m-%Y")), 'a', 'utf-8')
        print("\n\nLanguage : {}".format(language.title()), file=f)
        print("Total Sentences : {}".format(titleCount), file=f)
        print('+' + '-' * 45 + '+', file=f)
        print("|  Average Word count  | Average Letter count |", file=f)
        print('+' + '-' * 45 + '+', file=f)
        print("|{0:^22d}|{1:^22d}|".format(int(avgWords), int(avgLetters)), file=f)
        print('+' + '-' * 45 + '+', file=f)
        f.close()

        fig, ax = plt.subplots()
        data_line = ax.plot(words, label='Number of Words', marker='o')
        mean_line = ax.axhline(avgWords, color='r', label='Mean', linestyle='--')
        legend = ax.legend(loc='upper right')

        plt.savefig("Graph_{}.png".format(language))


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

    return [language.title(), rssFeed, titles, details]


def displayResults(results):
    tamilResults = ['Tamil', [], [], [], []]
    englishResults = ['English', [], [], [], []]
    germanResults = ['German', [], [], [], []]
    for result in results:

        if result[0] == 'Tamil':
            tamilResults[1].append(result[1])
            tamilResults[2].append(result[2])
            tamilResults[3] += (column(result[3], 1))
            tamilResults[4] += (column(result[3], 0))
        if result[0] == 'English':
            englishResults[1].append(result[1])
            englishResults[2].append(result[2])
            englishResults[3] += (column(result[3], 1))
            englishResults[4] += (column(result[3], 0))
        if result[0] == 'German':
            germanResults[1].append(result[1])
            germanResults[2].append(result[2])
            germanResults[3] += (column(result[3], 1))
            germanResults[4] += (column(result[3], 0))

    display([tamilResults, englishResults, germanResults])


def main():
    rssList = []
    results = []
    with open("input.txt") as f:
        for line in f.readlines():
            text = line.split()
            rssList.append([text[0], text[1]])

    for rssFeed in rssList:
        results.append(analyse(rssFeed[0], rssFeed[1]))

    displayResults(results)


if __name__ == "__main__":
    main()
