# Add new author and populate previous pubs into pubfile
from scholarly import scholarly

newAuthors = ['Jerome Buhl','Steven Strogatz'] # Replace Me
with open('authors.csv','a') as authorFile:
    for newAuthor in newAuthors:
        authorFile.write(newAuthor+'\n')
        search_query = scholarly.search_author(newAuthor)
        author = scholarly.fill(next(search_query))
        pubIDs = []
        for pub in author['publications']:
            authPubID = pub['author_pub_id']
            iColon = authPubID.find(':')
            pubID = authPubID[iColon+1:]
            pubIDs.append(pubID)

        with open('pubs.csv','a') as pubFile:
            for pubID in pubIDs:
                pubFile.write(pubID+'\n')
