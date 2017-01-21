# NewsHeadlinesAnalyser
Statistical analysis of headlines from Tamil, English and German news rss feeds

#Input

Input to the file is stored in input.txt (Please note: No validations added to check the input)

Format of input.txt file is
<language> <rss-Feed-URL>
<language1> <rss-Feed-URL1>
<language2> <rss-Feed-URL2>
<language> <rss-Feed-URL3>
<language2> <rss-Feed-URL4>


#Result

A dump file is created with the date of execution which stores all the headlines fetched from rss feed and their corresponding letter count and word count. 

Analysis file contains the total sentences read, the average word count and average letter count.

Graphs of word count is created for each language separately.
