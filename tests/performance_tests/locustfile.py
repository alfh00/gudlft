from locust import HttpUser, task, between
import random

class ServerPerformanceTest(HttpUser):
    wait_time = between(0.1,0.5)
    @task
    def home(self):
        self.client.get('/')
    
    @task(2)
    def get_sum(self):
        self.client.get('/showSummary', data = {'email': 'admin@irontemple.com'})

    @task(3)
    def get_book(self):
        competitions = [
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
            }
        ]
        clubs = [
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
        comps_and_club = [(random.choice(competitions)['name'], random.choice(clubs)['name']) for i in range(5)]
        for comp, club in comps_and_club:
            url = f'/book/{comp}/{club}'
            self.client.get(url)

    