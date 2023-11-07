import pytest
import random

from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_clubs():
    clubs = [
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }]
    listOfClubs = loadClubs()
    assert listOfClubs == clubs

def test_get_competitions():
   competitions =  [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
   listOfComps = loadCompetitions()
   assert competitions == listOfComps