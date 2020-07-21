# Pagerank_Algorithm_Webcrawler

Implements the renowned pagerank algorithm on a dataset formed by its Web Crawler from a seed webpage. BeautifulSoup + SQLite + Python

## Code Explanation : ##

* __*googlespider.py*__ : This file takes as input a seed URL, e.g, "www.facebook.com" and spiders through. It parses the source code of the page for all <a> tags with href values and adds them to a database. When it is done with the current page, it moves over to the immediate next entry in the database and adds all of its links to end of the database. Using this technique, a database of links is made, and this interconnected links database is our input to the pagerank algorithm. An example runtime screenshot of the terminal can be found in *SpiderGoogle1.png*

* __*PageRank.py*__ : This code implements the page rank algorithm on the dataset formed by the spider and adds the rank allotted by it as an extra column in the same database. Basically it takes into account 3 things to define the score for a link: a) Number of links this link points to   b) Number of links this link is pointed by    c) The rank of the links that point to this link. Using a combination of these 3 parameters a score is assigned to each link and this is done for multiple iterations.

* __*SanityCheck.py*__ : Checks if the pagerank algorithm implemented is ranking correctly or not by running it on a connected network of 4 links, connected by all sides except one diagonal.

* __*All other files*__ : Used for visualising the network formed by the links. Tried to see if all the links started from "Google.com" form a small-world network, or a bow-tie network ( as proposed in early papers ) etc.

### Conclusion ### 

Allowed the code to run for approximately 1 lakh links seeded by "www.facebook.com". On running the pagerank algorithm on this database, the expected "www.facebook.com" emerged as the highest ranked page, which suggests that the algorithm works correctly.
