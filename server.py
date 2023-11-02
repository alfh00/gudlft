import os
from dotenv import load_dotenv

import json
from flask import Flask,render_template,request,redirect,flash,url_for

load_dotenv()

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST', 'GET'])
def showSummary():
    if request.method == 'POST':
        email =request.form['email']
    if request.method == 'GET':
        email = request.args.get('email')

    club = next((club for club in clubs if club['email'] == email), None)
    if club is not None:
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash(f"Invalid or not found email address")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if foundClub is not None and foundCompetition is not None:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong, please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    MAX_PLACES_NUMBER = 12
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if competition is not None and club is not None:
        try:
            placesRequired = int(request.form['places'])
        except (ValueError, TypeError):
            flash("Enter a valid number of places")
            return redirect(url_for('book', competition= competition['name'], club= club['name']))


        available_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])

        
        if available_places == 0:
            flash(f"This Competition Is Complete.")
            return redirect(url_for('book', competition= competition['name'], club= club['name']))
        if placesRequired > MAX_PLACES_NUMBER:
            flash(f"You can purchase less than 12 places.")
            return redirect(url_for('book', competition= competition['name'], club= club['name']))
        if club_points < placesRequired:
            flash(f"Not enough points, try less places.")
            return redirect(url_for('book', competition= competition['name'], club= club['name']))
        if available_places < placesRequired :
            flash(f"Only {available_places} are available.")
            return redirect(url_for('book', competition= competition['name'], club= club['name']))
        
        competition['numberOfPlaces'] = str(available_places - placesRequired)
        club['points'] = str(club_points- placesRequired)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    else:
        flash("Something went wrong, please try again")
        return redirect(url_for('index'))


# TODO: Add route for points display
@app.route('/points-table/<club>')
def show_points_table(club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    if foundClub is not None:
        return render_template('points_table.html',club=foundClub, clubs=clubs)
    else:
        flash("email doesn't match any club")
        return redirect(url_for('index'))



@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG'))