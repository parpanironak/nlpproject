#!/bin/bash

echo "Create pages folder by processing simplewiki.xml and creating new documents"
nlpproject/src/newExtractPages.py -i simplewiki.xml

echo "Get count of tags from pages Starting"
mkdir ./taglist
find ./pages -type f -exec grep -il 'Barcelona[:space:]*\]\]' {} + >> taglist/Barcelona.txt
find ./pages -type f -exec grep -il 'Chinese[:space:]*\]\]' {} + >> taglist/Chinese.txt
find ./pages -type f -exec grep -il 'Dutch[:space:]*\]\]' {} + >> taglist/Dutch.txt
find ./pages -type f -exec grep -il 'Finnish[:space:]*\]\]' {} + >> taglist/Finnish.txt
find ./pages -type f -exec grep -il 'Greek[:space:]*\]\]' {} + >> taglist/Greek.txt
find ./pages -type f -exec grep -il 'Italian[:space:]*\]\]' {} + >> taglist/Italian.txt
find ./pages -type f -exec grep -il 'Latin[:space:]*\]\]' {} + >> taglist/Latin.txt
find ./pages -type f -exec grep -il 'Milan[:space:]*\]\]' {} + >> taglist/Milan.txt
find ./pages -type f -exec grep -il 'PST[:space:]*\]\]' {} + >> taglist/PST.txt
find ./pages -type f -exec grep -il 'Public[:space:]*\]\]' {} + >> taglist/Public.txt
find ./pages -type f -exec grep -il 'Scottish[:space:]*\]\]' {} + >> taglist/Scottish.txt
find ./pages -type f -exec grep -il 'Swedish[:space:]*\]\]' {} + >> taglist/Swedish.txt
find ./pages -type f -exec grep -il 'Turkish[:space:]*\]\]' {} + >> taglist/Turkish.txt

find nlpproject/src/ -type f -exec chmod 777 {} +
echo "calculating IDF"
nlpproject/src/calculateIDF.py -i pages/ -o corpus

echo "IDF done, starting Barca"
nlpproject/src/createRawCorpus.py -i taglist/Barcelona.txt -o corpus -t Barcelona
echo "Barca end, Chinese begin"
nlpproject/src/createRawCorpus.py -i taglist/Chinese.txt -o corpus -t Chinese
echo " Chinese end. dutch begin"
nlpproject/src/createRawCorpus.py -i taglist/Dutch.txt -o corpus -t Dutch
echo " dutch end, finnish begin"
nlpproject/src/createRawCorpus.py -i taglist/Finnish.txt -o corpus -t Finnish
echo " finnish end, greek begin"
nlpproject/src/createRawCorpus.py -i taglist/Greek.txt -o corpus -t Greek
echo "Greek end. Italian begin"
nlpproject/src/createRawCorpus.py -i taglist/Italian.txt -o corpus -t Italian
echo " italian end, Latin begin"
nlpproject/src/createRawCorpus.py -i taglist/Latin.txt -o corpus -t Latin
echo "Latin end, Milan begin"
nlpproject/src/createRawCorpus.py -i taglist/Milan.txt -o corpus -t Milan
echo "Milan end, PST begin"
nlpproject/src/createRawCorpus.py -i taglist/PST.txt -o corpus -t PST
echo "PST end, Public begin"
nlpproject/src/createRawCorpus.py -i taglist/Public.txt -o corpus -t Public
echo "Public end, Scottish begin"
nlpproject/src/createRawCorpus.py -i taglist/Scottish.txt -o corpus -t Scottish
echo "Scottish end, Swedish begin"
nlpproject/src/createRawCorpus.py -i taglist/Swedish.txt -o corpus -t Swedish
echo "Swedish end, Turkish begin"
nlpproject/src/createRawCorpus.py -i taglist/Turkish.txt -o corpus -t Turkish
echo "Turkish end"

echo "create vectors beginning"
nlpproject/src/createVectors.py -i corpus
echo "Vectors created, success!"

echo "Processing input document and performing disambiguation"
nlpproject/src/vectorizeInput.py -i fileWithCorrectTags.txt -d corpus > fileWithPredictedTags.txt

echo "Disambiguation complete, success!"
