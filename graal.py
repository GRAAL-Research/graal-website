#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from flask import Flask, render_template
app = Flask(__name__)


member_status_pretty_names = {"undergrad": {"fr": "Étudiant sous-gradué", "en": "Undergraduate student"},
                              "master": {"fr": "Étudiant de maîtrise", "en": "Masters student"},
                              "phd": {"fr": "Étudiant doctorant", "en": "PhD Student"},
                              "postdoc": {"fr": "Chercheur post-doctoral", "en": "Postdoctoral Researcher"},
                              "prof": {"fr": "Professeur", "en": "Professor"}}


class Graalien(object):
    def __init__(self, first_name, last_name, status, joined_year, face_picture=None, linkedin=None, scholar=None,
                 github=None, website=None):
        self.first_name = first_name
        self.last_name = last_name
        self.status_ = status
        self.joined_year = joined_year
        self.face_picture = face_picture
        self.linkedin = linkedin
        self.scholar_ = scholar
        self.github = github
        self.website = website

        if status not in member_status_pretty_names.keys():
            raise ValueError("Incorrect graalien status. Supporter values are {0!s}".format(self.status_pretty_names))

    @property
    def scholar(self):
        return self.scholar_ + "&view_op=list_works&sortby=pubdate"

    @property
    def status(self):
        return member_status_pretty_names[self.status_]


@app.route('/')
def hello():
    professors = [
        Graalien(first_name="Francois",
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
    ]
    graaliens = [
        Graalien(first_name="Alexandre",
                 last_name="Drouin",
                 status=member_status_pretty_names.keys()[np.random.randint(0, len(member_status_pretty_names))],
                 joined_year=2012,
                 face_picture="images/faces/adrouin.png",
                 linkedin="https://www.linkedin.com/in/drouinalexandre/",
                 scholar="https://scholar.google.ca/citations?user=LR6aJcEAAAAJ",
                 github="https://github.com/aldro61",
                 website="http://graal.ift.ulaval.ca/adrouin/")
        for _ in xrange(14)
    ]

    # Sort by joined date
    graaliens = sorted(graaliens, key=lambda x: "{0!s} {1!s}".format(x.first_name, x.last_name), reverse=False)
    return render_template('index.html', graaliens=professors + graaliens)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404