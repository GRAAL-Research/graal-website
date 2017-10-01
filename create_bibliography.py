#https://pypi.python.org/pypi/GoogleScholar
# -*- coding: utf-8 -*-
import scholarly
import logging
from collections import defaultdict
import json
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PROFESSOR = ["Francois Laviolette", "Mario Marchand"]

def create_bibliography():
    if os.path.isfile("static/bib/bibliography_graal.json"):
        logging.debug("Loading shelves")
        bibliography = json.load(open("static/bib/bibliography_graal.json", 'r'))
        logging.debug("Loaded %s papers already in the json file" % len(bibliography))
    else:
        bibliography = []

    seen_id = defaultdict(bool)
    for item in bibliography:
        seen_id[item["uniq_id"]] = True

    skipped_papers = open("Skipped_papers.txt", 'w')

    for prof in PROFESSOR:
        logging.debug("Searching for %s\n" % prof)
        author_query = scholarly.search_author(prof)
        logging.debug("Performed author search for %s\n" % prof)
        author = next(author_query).fill()
        logging.debug("Filled author\n")
        for publication_short in author.publications:
            print("Working on publication:")
            print(publication_short)
            try:
               # 1. Do we already have the publication in the bibliography?
                uniq_id = publication_short.id_citations
                if uniq_id == "":
                    print("id_citations is not a good uniq id")
                    sys.exit(0)
                if seen_id[uniq_id]:  # We already have this publication in the shelves.
                    logging.debug("Publication with id %s was already in the shelves" % uniq_id)
                    continue

                print("Searching full entry for: %s\n"%publication_short.bib["title"])

                # 2. Publication was not in the shelves. Search for the publication informations.
                for publication_full in scholarly.search_pubs_query(publication_short.bib["title"]):
                    print("one hit: %s" %publication_full)
                    if publication_full.bib["title"] == publication_short.bib["title"]:
                        publication_full.fill()
                        break

                if not publication_full._filled:
                    print("Warning: Full citation for paper '%s' was not found" % publication_short.bib["title"])
                    continue

                title = publication_full.bib["title"]
                try:
                    authors = publication_full.bib["author"]
                    journal = publication_full.bib.get("journal", publication_full.bib.get("booktitle"))
                    year = publication_full.bib["year"]
                except KeyError:
                    # Major information missing, just skip it.
                    skipped_papers.write("Can't find authors, journal or year for %s. Entry was skipped.\n" % title)
                    continue

                url = publication_full.bib.get("url", "")
                volume = publication_full.bib.get("volume", "")
                pages = publication_full.bib.get("pages", "")

                #  url_scholar = publication_full.url_scholarbib  # The scholar url does not work (bcuz Google)

                # 3. Format citation
                citation = ""
                for i in xrange(0, 3):
                    try:
                        a = authors.split(" and ")[i]
                        if citation != "":
                            citation += ", "
                    except IndexError:
                        # Less than 3 authors...
                        break
                    name = a.split(", ")[0]
                    first_name = a.split(", ")[1]
                    citation += "%s %s." % (name, first_name[0])
                if len(authors.split(" and ")) > 3:
                    citation += " et al."

                citation += " (%s). %s. %s, %s, %s " % (year, title, journal, volume, pages)
                citation = citation.replace("{\'e}", "é")

                # 4. Add the citation to the bibliography...
                logging.debug("Added: %s\n" % citation)
                bibliography.append({"year": year, "citation": citation, "url": url, "uniq_id": uniq_id})
                seen_id[uniq_id] = True   # We are only sure the paper was added in the bibliography at this point...
            except:
                print("If you see this repeatedly, you are probably punished by Google the god...")
                json.dump(bibliography, open("static/bib/bibliography_graal_partial.json", 'w'))  # partial dump...
                skipped_papers.write("Paper was not kept for an unknown error: %s\n" % publication_short.bib["title"])
                continue
    json.dump(bibliography, open("static/bib/bibliography_graal.json", 'w'))
    skipped_papers.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s")
    create_bibliography()
