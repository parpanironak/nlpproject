Natural Language Processing
===================

Project description:
http://nlp.cs.nyu.edu/sekine/nlp2015wikification/

Usage:
-----------
Coming soon

Data:
----------
You can download the data we used from https://dumps.wikimedia.org/simplewiki/20150406/simplewiki-20150406-pages-articles.xml.bz2



[[Barcelona F.C. | Barcelona]]

       ^              ^
       |              |

    Entity           Tag


Need a file(not a pickle dump) with for each Tag with all entities it can resolve to one per line

Need a file(not a pickle dump) for each Tag-Entity pair with all the sentences that contain a wiki tag in the above format one per line


Dump file will be have form

<page .... title="title">
.....content.....
</page>

need to store each xml tag in a separate file with name <title>.xml (title is the entity in the entity tag pair)

need to go through each of the file to check if it contains one of the key words and make a list of the file paths and store in a file (grep command exits/ can make separate list for each word)

while we go through the files we also need to keep a count of each Tag-Entity pair ( this is to eliminate less frequently occuring Entities for that tag )

need to go through the entire corpus to determine the idf / need to go through the reduced corpus to find inverse entity frequency

when running system use the reduced corpus and the idf values to create a vector and store it in memory and comapare to the vector of the generated for the input document 
