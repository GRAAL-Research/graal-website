#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template
app = Flask(__name__)


member_status_pretty_names = {"undergrad": {"fr": "Étudiant sous-gradué", "en": "Undergraduate student"},
                              "master": {"fr": "Étudiant de maîtrise", "en": "Masters student"},
                              "phd": {"fr": "Étudiant doctorant", "en": "PhD Student"},
                              "postdoc": {"fr": "Chercheur post-doctoral", "en": "Postdoctoral Researcher"},
                              "prof": {"fr": "Professeur", "en": "Professor"}}


class Graalien(object):
    def __init__(self, first_name, last_name, status, joined_year, face_picture=None, linkedin=None, scholar=None,
                 github=None, website=None, twitter=None):
        self.first_name = first_name
        self.last_name = last_name
        self.status_ = status
        self.joined_year = joined_year
        self.face_picture = face_picture
        self.linkedin = linkedin
        self.scholar_ = scholar
        self.github = github
        self.website = website
        self.twitter = twitter

        if status not in member_status_pretty_names.keys():
            raise ValueError("Incorrect graalien status. Supporter values are {0!s}".format(self.status_pretty_names))

    @property
    def scholar(self):
        return self.scholar_ + "&view_op=list_works&sortby=pubdate" if self.scholar_ is not None else None

    @property
    def status(self):
        return member_status_pretty_names[self.status_]


@app.route('/')
def hello():
    professors = [
        Graalien(first_name="François",
                 last_name="Laviolette",
                 status="prof",
                 joined_year=-10000,
                 face_picture="images/faces/flaviolette.png",
                 linkedin="https://www.linkedin.com/in/francois-laviolette-3933879/",
                 scholar="https://scholar.google.ca/citations?user=uwwWC3cAAAAJ",
                 website="https://www.ift.ulaval.ca/departement-et-professeurs/professeurs-et-personnel/professeurs-reguliers/fiche/show/laviolette-francois/"),
        Graalien(first_name="Mario",
                 last_name="Marchand",
                 status="prof",
                 joined_year=-10000,
                 face_picture="images/faces/mmarchand.png",
                 linkedin="https://www.linkedin.com/in/mario-marchand-50460913/",
                 scholar="https://scholar.google.ca/citations?user=M792u2sAAAAJ",
                 website="https://www.ift.ulaval.ca/departement-et-professeurs/professeurs-et-personnel/professeurs-reguliers/fiche/show/marchand-mario/"),
        Graalien(first_name="Luc",
                 last_name="Lamontagne",
                 status="prof",
                 joined_year=2004,
                 face_picture="images/faces/llamontagne.png",
                 linkedin="https://www.linkedin.com/in/luc-lamontagne-a42566b/",
                 scholar="https://scholar.google.com/citations?user=mCsuyb0AAAAJ",
                 website="http://www.ift.ulaval.ca/~lamontagne/lamontagne-en.html"),
        Graalien(first_name="Jacques",
                 last_name="Corbeil",
                 status="prof",
                 joined_year=2010,
                 face_picture="images/faces/jcorbeil.png",
                 linkedin="https://www.linkedin.com/in/jacques-corbeil-0486391/",
                 scholar="https://scholar.google.ca/citations?user=ZOxQV80AAAAJ",
                 website="http://corbeillab.genome.ulaval.ca/team_member/jacques-corbeil/"),
        Graalien(first_name="Richard",
                 last_name="Khoury",
                 status="prof",
                 joined_year=2016,
                 face_picture="images/faces/rkhoury.png",
                 linkedin="https://www.linkedin.com/in/richard-khoury-59b92130",
                 scholar="http://scholar.google.ca/citations?user=PgyHf0oAAAAJ",
                 website="http://www2.ift.ulaval.ca/~rikho/")
    ]
    graaliens = [
        Graalien(first_name="Alexandre",
                 last_name="Drouin",
                 status="phd",
                 joined_year=2012,
                 face_picture="images/faces/adrouin.png",
                 linkedin="https://www.linkedin.com/in/drouinalexandre/",
                 scholar="https://scholar.google.ca/citations?user=LR6aJcEAAAAJ",
                 github="https://github.com/aldro61",
                 website="http://graal.ift.ulaval.ca/adrouin/",
                 twitter="https://twitter.com/alexandredrouin"),
        Graalien(first_name="Ulysse",
                 last_name="Côté Allard",
                 status="phd",
                 joined_year=2014,
                 face_picture="images/faces/uacote.png",
                 scholar="https://scholar.google.ca/citations?user=RF5bU6sAAAAJ&hl",
                 github="https://github.com/giguelingueling",
                 website="http://graal.ift.ulaval.ca/ulysse/"),
        Graalien(first_name="Gaël",
                 last_name="Letarte St-Pierre",
                 status="undergrad",
                 joined_year=2016,
                 face_picture="images/faces/gletarte.png",
                 scholar="https://scholar.google.ca/citations?user=XMCOvKoAAAAJ",
                 github="https://github.com/gletarte"),
        Graalien(first_name="Pier-Luc",
                 last_name="Plante",
                 status="phd",
                 joined_year=2014,
                 face_picture="images/faces/plplante.png",
                 linkedin="https://www.linkedin.com/in/pier-luc-plante-b777716b/",
                 scholar="https://scholar.google.ca/citations?user=8Vp-4GgAAAAJ",
                 github="https://github.com/plpla"),
        Graalien(first_name="Frédéric",
                 last_name="Raymond",
                 status="postdoc",
                 joined_year=2011,
                 face_picture="images/faces/fraymond.png",
                 linkedin="https://www.linkedin.com/in/fredericraymond/",
                 scholar="https://scholar.google.ca/citations?user=Ulexpm0AAAAJ",
                 github="https://github.com/fredericraymond",
                 website="http://corbeillab.genome.ulaval.ca/team_member/frederic-raymond/",
                 twitter="https://twitter.com/fredericraymond"),
        Graalien(first_name="Francis",
                 last_name="Brochu",
                 status="phd",
                 joined_year=2014,
                 face_picture="images/faces/fbrochu.png",
                 linkedin="https://www.linkedin.com/in/francis-brochu-a31948139/",
                 scholar="https://scholar.google.ca/citations?user=eH0dEcwAAAAJ",
                 github="https://github.com/PhrankBrochu")
    ]

    # Sort by name date
    graaliens = sorted(graaliens, key=lambda x: x.joined_year, reverse=False)
    return render_template('index.html', graaliens=professors + graaliens)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=3333, debug=False)
