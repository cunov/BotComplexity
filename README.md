# BotComplexity
https://twitter.com/BotComplexity

Twitter bot that tweets when a researcher I'm interested in publishes a new paper

It reads authors from an authors.csv file and searches Google Scholar for publications, storing previously scraped publications in a pubs.csv file. If a new pub is found, it tweets about it.

Replace your keys in the create_api() function, as well as paths to an authors.csv (one line per author) and pubs.csv files. pubs.csv holds the pubIDs of previously tweeted papers, so we don't get repeats. You can initialize pubs.csv when adding a new author by running initialize.py file (if you don't, it will tweet every paper they've ever published on the first run!).

## List of authors I tweet about:
* Duncan J Watts,@duncanjwatts
* Peter Sheridan Dodds,@peterdodds
* Mattias Wahde
* Giovanni Volpe,@VolpeResearch
* Sergiy Butenko
* Dirk Helbing,@DirkHelbing
* Jerome Buhl
* James Bagrow,@bagrow
* Josh Bongard,@DoctorJosh
* Chris Danforth,@ChrisDanforth
* Laurent Hebert-Dufresne,@LHDnets
* Daniel Ari Friedman
* Mats Granath
* Bernhard Mehlig
* Claes Andersson
* Kolbjørn Tunstrøm
* Kristian Lindgren
