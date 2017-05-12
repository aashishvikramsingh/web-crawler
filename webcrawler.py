import urllib2
import time
from BeautifulSoup import BeautifulSoup



# FRONTIER: seed list [list].
# URL_TRAVERSED: urls which has been processed and popped out from the FRONTIER [list].
# depth: keeps track of depth and the count of the seeds at the given depth. First seed is
# "https://en.wikipedia.org/wiki/Sustainable_energy".
# FRONTIER_FILE_PATH: path to the file where all urls traversed are stored.
# CORPUS_FILE_PATH: path to the file where all corpus are stored.


FRONTIER = []
URL_TRAVERSED = []
FRONTIER_LIMIT_EXCEED=0
FRONTIER_FILE_PATH="C:\\users\\aashi\\desktop\\wc\\BFS\\"
CORPUS_FILE_PATH="C:\\users\\aashi\\desktop\\wc\\BFS\\"



def main(seed_url, keyword ):
    # depth_level: current depth. Max depth allowed is 5
    # count_urls_processed_current_depth: keeps the count of urls processed at the given depth.
    # count_unique_links_processed: it counts the total urls processed irrespective of depth. As per problem statement,
    #  this hould not be more than 1000.

    global FRONTIER
    global URL_TRAVERSED
    global FRONTIER_FILE_PATH
    global CORPUS_FILE_PATH
    global FRONTIER_LIMIT_EXCEED
    depth = {1: 1, 2: "none", 3: "none", 4: "none"}
    depth_level = 1
    count_urls_processed_current_depth = 0
    count_unique_links_processed = 0

    # Add first seed to the FRONTIER
    FRONTIER.append(seed_url)



    while  depth_level <= 5 and count_unique_links_processed < 1000:
        #Fetch the url from FRONTIER
        connecturl = FRONTIER[0]

        #delay between two subsequent call to wiki is set to 1 sec.
        time.sleep(1)

        # Opening and reading content from the url fetched from FRONTIER
        connection = urllib2.urlopen(connecturl)
        htmldata = connection.read()
        soup = BeautifulSoup(htmldata)

        # retrieve the required links by filtering.
        if FRONTIER_LIMIT_EXCEED == 0:
            push_FRONTIER(soup, keyword)
        else:
            " "


        ##########################
        print ("Feching content from URL No " + str(count_unique_links_processed+1) + ":")
        print ("URL: " + FRONTIER[0])
        ###########################
        # record the url which has been processed.
        f = open(FRONTIER_FILE_PATH+"BFS_frontier.txt", "a")
        f.write("\n" + str(FRONTIER[0]))
        f.closed

        #Saving the url contents in file
        f = open(CORPUS_FILE_PATH + "BFS_corpus_"+str(count_unique_links_processed+1) + ".txt", "w")
        f.write("\n"+ FRONTIER[0]+"\n")
        f.write(htmldata)
        f.closed

        # pop the url processed from the FRONTIER
        URL_TRAVERSED.append(FRONTIER.pop(0))

        #increment unique link processed counter by 1
        count_unique_links_processed += 1



        #increment the count_urls_processed_current_depth by 1.
        count_urls_processed_current_depth += 1

        # goto next depth level if all urls at current depth is processed.
        if  count_urls_processed_current_depth >= (depth[depth_level]):
            depth_level += 1
            depth[depth_level] = len(FRONTIER)
            print ("total urls processed till now: " + str(count_unique_links_processed))
            print ("urls processed at depth: "+ str(depth_level-1) + ": "+ str(count_urls_processed_current_depth))
            print ("\n Processing depth: " + str(depth_level))
            print ("\n number of urls to be processed: "+ str(depth[depth_level]))


            count_urls_processed_current_depth = 0

#-----------------------------------------------------------------------------------------------------------------------

def push_FRONTIER(bs,keyword):

    # hash: '#'.
    # colon: ':'
    # connecturl: url to be appended in FRONTIER
    global FRONTIER
    global URL_TRAVERSED
    global FRONTIER_LIMIT_EXCEED
    pound = "#"
    colon = ":"
    connecturl=""

    for link in bs.body.findAll('a', href=True):
        if len(FRONTIER)<1000:
            valid_link=str(link['href'].encode("UTF-8"))

            if pound in valid_link and colon not in valid_link:
                if valid_link.rpartition('#')[0]:
                    valid_link=valid_link.rpartition('#')[0]
                else:
                    valid_link=""
            if valid_link and pound not in valid_link and colon not in valid_link:
                if (valid_link.lower().startswith('/wiki') or valid_link.lower().startswith(
                    "https://en.wikipedia.org") or valid_link.lower().startswith("http://en.wikipedia.org")):
                    if keyword.lower() in valid_link.lower() or keyword.lower() in str(link.contents).lower():
                        if valid_link.upper() not in str(FRONTIER).upper() and valid_link.lower() not in str(
                            FRONTIER).lower():
                            if valid_link.upper() not in str(URL_TRAVERSED).upper() and valid_link.lower() not in str(URL_TRAVERSED).lower():
                                if "https://en.wikipedia.org" not in valid_link.lower():
                                    connecturl = "https://en.wikipedia.org" + valid_link
                                else:
                                    connecturl = valid_link
                                FRONTIER.append(connecturl)
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            FRONTIER_LIMIT_EXCEED=1
            break

#-----------------------------------------------------------------------------------------------------------------------

#call to main(url,keyword)
main("https://en.wikipedia.org/wiki/Sustainable_energy",'solar')