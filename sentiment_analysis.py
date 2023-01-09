##########################################################
# Troy Carloni, Brandon Butler
# 664 Project
# Description: sentiment analysis using delta TFIDF
##########################################################
import pandas as pd
import math
import os
import plotly.express as px
from rake_nltk import Rake
import re
import sys

pd.options.plotting.backend = "plotly"
# Arrays for storing movie review collection
negTextArray = []
posTextArray = []

rake = Rake(include_repeated_phrases=False, min_length=2, max_length=2)


# Dictionary for sentiment analysis
evalTextDict = {}

# used to ensure entire collection of reviews are opened.
failedCount1 = 0
failedCount2 = 0
failedCount3 = 0

with open("log.txt", 'w') as f:
    f.close()

# personal scoring txt
personal_scoringDict = {}
tempStr = ""
text = str(sys.argv).split(",")
textScoring = text[1].replace("'", "").strip()
textTestCorpus = text[2].replace("'", "").strip()
textTestCorpus = textTestCorpus.replace("]", "")

# with open("personal_scoring.txt", encoding="utf-8") as f:
with open(textScoring, encoding="utf-8") as f:
    while True:
        temp = f.readline()
        if not temp:
            break
        temp = temp.split(':')
        tempStr = temp[1].replace("\n", "")
        personal_scoringDict[temp[0]] = tempStr

print(personal_scoringDict.values())

# open and collect negative review collection into array
neglist = os.listdir("train/neg/")
for filename in neglist:
    try:
        with open("train/neg/"+str(filename), encoding="utf-8") as f:
            negTextArray.append(f.readlines())
            f.close()
    except IOError as e:
        failedCount1 += 1
print("failed to open: "+str(failedCount1))

# open and collect positive review collection into array
poslist = os.listdir("train/pos/")
for filename in poslist:
    try:
        with open("train/pos/"+str(filename), encoding="utf-8") as f:
            posTextArray.append(f.readlines())
            f.close()
    except IOError as e:
        failedCount2 += 1
print("failed to open: "+str(failedCount2))


# testList = os.listdir("longRun_test_corpus/")
testList = os.listdir(textTestCorpus)
x = 0
for filename in testList:
    try:
        with open(textTestCorpus+"/"+str(filename), encoding="utf-8") as f:
            evalTextDict[str(filename)+"_"+str(x+1)] = f.readlines()
            f.close()
    except IOError as e:
        failedCount3 += 1
    x += 1
print("failed to open: "+str(failedCount3))

# performs analysis on each text included in evalTextDict
alldata = {}
allarray = []
f = open('log.txt', 'a')
f1 = open('data_log.txt', 'a')
resultNum = 1
x = 1
for topkey in evalTextDict:
    rake.extract_keywords_from_text(str(evalTextDict.get(topkey)))
    test = rake.get_word_frequency_distribution()
    phrases = rake.get_ranked_phrases()

    # checks feature words against pos/neg review collection, if word is found at least once count is increase by 1
    posDict = {}
    negDict = {}

    for key in test:
        negDict[key] = 0
        posDict[key] = 0
        for entry in negTextArray:
            if str(entry).find(key) != -1:
                negDict[key] += 1
        for entry in posTextArray:
            if str(entry).find(key) != -1:
                posDict[key] += 1

    for phrase in phrases:
        phrase = re.sub(r'\{|\[|\]|\}|\)|\(|\.', '', str(phrase))
        negDict[phrase] = 0
        posDict[phrase] = 0
        for entry in posTextArray:
            if re.search(r'\b' + phrase + r'\b', str(entry), flags=re.IGNORECASE | re.ASCII):
                posDict[phrase] += 1
        for entry in negTextArray:
            if re.search(r'\b' + phrase + r'\b', str(entry), flags=re.IGNORECASE | re.ASCII):
                negDict[phrase] += 1

    evalDict = {}

    for key in test:
        if str(key).find(']') == -1 and str(key).find('[') == -1:
            evalDict[key] = test.get(key)

    for phrase in phrases:
        phrase = re.sub(r'\{|\[|\]|\}|\)|\(|\.', '', str(phrase))
        phraseCount = re.findall(
            r'\b' + phrase + r'\b', str(evalTextDict.get(topkey)))
        evalDict[phrase] = len(phraseCount)

    # calculations
    wordScore = {}

    for key in evalDict:
        if negDict.get(key) == None or posDict.get(key) == None:
            wordScore[key] = 0
        elif negDict.get(key) == 0 or posDict.get(key) == 0:
            wordScore[key] = 0
        else:
            #print (str(evalDict[key]) +" * "+ str(negDict[key])+"/"+str(posDict[key]))
            wordScore[key] = int(evalDict[key]) * \
                math.log2(int(negDict[key])/int(posDict[key]))

    f.write("\n"+topkey+"\n")

    for key in wordScore:
        alldata[key] = -1*wordScore.get(key)
        f.write(str(key)+": "+str(wordScore.get(key))+"\n")

    # sums up word values to determine final scoring : positive or negative
    wordSum = 0
    for value in wordScore.values():
        wordSum += value

    wordSum = wordSum*-1
    score = (wordSum/(len(evalTextDict.get(topkey)[0])/100))+5
    if score > 10:
        score = 10
    if score < 0:
        score = 0
    f1.write(topkey+":" + str(wordSum)+" :" +
             str(len(evalTextDict.get(topkey)[0])) + " :"+str(score)+"\n")

    print(topkey + ": "+str(score))
    allarray.append(score)


# ALL DATA WORD SCORES SCATTER PLOT
rangeArray = list(range(0, len(alldata)))
fig2 = px.scatter(x=rangeArray, y=alldata.values(), hover_name=alldata.keys(
), labels={'x': 'x', 'y': 'wordScore'})

# ALL DATA PERSONAL SCORE + PROGRAM SCORE
alldataDict = {}
xArray = []
yArray = []
y1Array = []
i = 0
for key in personal_scoringDict:
    xArray.append(key)
    yArray.append(float(personal_scoringDict.get(key)))
    y1Array.append(allarray[i])
    i += 1

df = pd.DataFrame(
    {"text_name": xArray, "personal_score": yArray, "program_score": y1Array})
fig1 = px.bar(
    data_frame=df,
    x="text_name",
    y=["personal_score", "program_score"],
    opacity=0.9,
    orientation="v",
    barmode='group',
    title='Sentiment Analysis',
)

fig2.write_html("test_results/results_"+str(1)+".html")
fig1.write_html("test_results/results_"+str(2)+".html")


f1.write("\n")
f1.close()
f.close()
