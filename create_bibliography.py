import requests
import xml.etree.ElementTree as ET
import json
import os
import re


DBLP_URL = 'https://dblp.uni-trier.de/pers/xx/'

PROFESSOR_DLPB_IDS = [
    "l/Laviolette:Fran=ccedil=ois",
    "m/Marchand:Mario",
    "l/Lamontagne:Luc",
    "k/Khoury:Richard",
    "c/Corbeil:Jacques",
    "d/Durand:Audrey",
    "g/Germain:Pascal"
]


def loadDBLPXML(dblp_id):
    tmp_xml_filename = 'dblp.xml'
    url = DBLP_URL + dblp_id
    resp = requests.get(url)
    return ET.fromstring(resp.content)

def format_author_name(author):
    last_space_pos = author.rfind(' ')
    last_name = author[last_space_pos + 1:]
    first_name_list = author[:last_space_pos].split(' ')
    initials = ' '.join(first_name[0] + '.' for first_name in first_name_list)
    return last_name + ' ' + initials

def format_authors(authors_list):
    authors = ', '.join(map(format_author_name, authors_list[:3]))
    if len(authors_list) > 3:
        authors += ' et al.'
    return authors

def get_value(publication_element, key, default=None):
    el = publication_element.find(key)
    return el.text if el is not None else default

def create_bibliography_entry(key, publication_element):
    title = get_value(publication_element, 'title')
    year = int(get_value(publication_element, 'year'))
    booktitle = get_value(publication_element, 'booktitle')
    journal = get_value(publication_element, 'journal', default=booktitle)
    volume = get_value(publication_element, 'volume')
    pages = get_value(publication_element, 'pages')
    url = get_value(publication_element, 'ee')

    authors_list = [el.text for el in publication_element.iter('author')]
    authors = format_authors(authors_list)


    citation = f"{authors} ({year}). {title} {journal}"
    if volume is not None:
        citation += f', {volume}'
    if pages is not None:
        citation += f', {pages}'
    return {"year": year, "citation": citation, "url": url, "uniq_id": key}

def create_bibliography():
    bibliography = []
    seen_key = set()
    for dblp_id in PROFESSOR_DLPB_IDS:
        person_element = loadDBLPXML(dblp_id)
        for publication_element in person_element.iter('r'):
            publication_element = publication_element[0]
            key = publication_element.attrib['key']
            if key not in seen_key:
                seen_key.add(key)
                entry = create_bibliography_entry(key, publication_element)
                bibliography.append(entry)

    json.dump(bibliography, open("static/bib/bibliography.json", 'w'), indent=2)

if __name__ == '__main__':
    create_bibliography()
