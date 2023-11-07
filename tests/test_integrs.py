import pytest

from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response.data


@pytest.mark.parametrize("email, response_must_include, expected_code", [
    ('email@email.com', b'Invalid or not found email address' ,200),           # Test case 1
    ('', b'Invalid or not found email address', 200),                          # Test case 2
    ('', b'Invalid or not found email address', 200),                          # Test case 2 script
    ('admin@irontemple.com', b'<h2>Welcome, admin@irontemple.com </h2>',200),  # Test case 3
])
def test_showSummary_view(client, email, response_must_include, expected_code):
    mock_club_email = {'email':email}
    response = client.post('/showSummary', data=mock_club_email, follow_redirects=True)

    assert response.status_code == expected_code
    assert response_must_include in response.data

@pytest.mark.parametrize("competition, club, expected_content, expected_status", [
    ('Fall Classic', 'Iron Temple', b'<label for="places">How many places?</label>', 200),  
    ('nonexistent_competition', 'nonexistent_club', b'Something went wrong, please try again', 200),  
])
def test_book_view(client, competition, club, expected_content, expected_status):
    response = client.get(f'/book/{competition}/{club}', follow_redirects=True)

    assert response.status_code == expected_status
    assert expected_content in response.data

@pytest.mark.parametrize("competition, club, req_places, expected_content, expected_status", [
    ('Fall Classic', 'Iron Temple', '0', b'Great-booking complete!', 200),  
    ('Fall Classic', 'Iron Temple', '13', b'You can purchase less than 12 places.', 200),  
    ('Fall Classic', 'Iron Temple', '8', b'Not enough points, try less places.', 200),  
    ('Fall Classic', 'Iron Temple', 'hello', b'Enter a valid number of places', 200),
    ('nonexistent_competition', 'nonexistent_club', '5', b'Something went wrong, please try again', 200),
    ('nonexistent_competition', 'nonexistent_club', '<h1>hello</h1>', b'Something went wrong, please try again', 200),
    ('Complete Comp', 'Iron Temple', '4', b'This Competition Is Complete.', 200),
    ('Only 2 places Comp', 'Iron Temple', '4', b'Only 2 are available.', 200),

])
def test_purshase_places(client, competition, club, req_places, expected_content, expected_status, mocker):
    mock_comp_data = mocker.patch('server.competitions', [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Complete Comp",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "0"
        },
        {
            "name": "Only 2 places Comp",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "2"
        }
    ])

    response = client.post('/purchasePlaces',data={'competition':competition, 'club':club ,'places':req_places}, follow_redirects=True)
    
    assert response.status_code == expected_status
    assert expected_content in response.data

@pytest.mark.parametrize("club_name, expected_status, expected_content", [
    ('Iron Temple', 200, b'th>Club</th>'),  # Existing club
    ('Nonexistent Club', 200, b'<li>email doesn'),  # Nonexistent club
])
def test_show_points_table(client, club_name, expected_status, expected_content):
    response = client.get(f'/points-table/{club_name}', follow_redirects=True)

    print(response.data, response.status_code)

    assert response.status_code == expected_status
    assert expected_content in response.data



def test_logout_redirect(client):
    
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200  
    assert b'Welcome to the GUDLFT' in response.data
