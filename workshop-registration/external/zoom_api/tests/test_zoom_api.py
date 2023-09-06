import os
from unittest.mock import Mock, patch
from pytest import fixture, mark
from external.zoom_api import ZoomAPI
from external.zoom_api.zoom_oauth import create_access_token
from external.zoom_api.get_meeting import get_meeting
from external.zoom_api.get_meetings import get_meetings
from external.zoom_api.list_registrants import list_registrants

@fixture(scope="session")
def access_token():
    access_data = create_access_token()
    return access_data['access_token']

def test_can_get_token():
    # Given secret information set as environment variables (account id, client id, client secret)
    account_id = os.environ.get('ACCOUNT_ID')
    assert account_id
    client_id = os.environ.get('CLIENT_ID')
    assert client_id
    client_secret = os.environ.get('CLIENT_SECRET')
    assert client_secret

    # When the user asks for access token
    zoom_api = ZoomAPI()
    access_token = zoom_api._get_access_token()

    # Then access token is returned
    assert access_token


def test_get_zoom_workshop_from_id():
    # Given a meeting id
    meeting_id = '860 6126 7458'

    # When we ask for zoom meeting
    zoom_api = ZoomAPI()
    zoom_meeting = zoom_api.get_meeting(meeting_id=meeting_id)

    # Then we see topic
    assert zoom_meeting.topic == 'iBOTS Workshop: Intro to Data Analysis with Python and Pandas '
    assert zoom_meeting.registration_url == 'https://us02web.zoom.us/meeting/register/tZItceiqqDwuH9yaRnk81FeBi3qwQP-3rgTI'
    for occurrence in zoom_meeting.occurrences:
        assert occurrence.start_time
    assert zoom_meeting.agenda 
    assert zoom_meeting.id

def test_get_zoom_session_from_id(access_token):
    # Given a meeting id
    meeting_id = '899 0138 0945'

    # When we ask for zoom meeting
    zoom_meeting = get_meeting(access_token=access_token, meeting_id=meeting_id)

    # Then we see topic
    assert zoom_meeting.topic == 'Feedback on workshop material (Jens and Mo)'
    assert zoom_meeting.agenda == ''
    assert zoom_meeting.id 
    
def test_get_upcoming_zoom_meetings_from_user_id(access_token):
    # GIVEN there are upcoming zoom meetings for a user with a speific id
    user_id = os.environ["TEST_USER_ID"]
    
    # WHEN user asks for the upcoming zoom meetings
    zoom_meetings = get_meetings(access_token=access_token, user_id=user_id)
    
    # THEN a list of upcoming zoom meeetings is returned
    agenda_counter = 0
    for meeting in zoom_meetings:
        assert meeting.id
        assert meeting.topic
        assert meeting.start_time
        if hasattr(meeting, "agenda"):
            agenda_counter += 1
    assert agenda_counter>1


def test_zoom_api_calls_get_meeting():
    # GIVEN a meeting ID 
    meeting_id = '899 0138 0945'
    zoom_api = ZoomAPI()
    zoom_api._get_access_token = Mock()
    zoom_api._get_access_token.return_value = 'open sesame'

    # WHEN the zoom api get meeting method is called
    with patch("external.zoom_api.api.get_meeting") as get_meeting:
        zoom_api.get_meeting(meeting_id=meeting_id)
        
    get_meeting.assert_called_with(access_token='open sesame', meeting_id=meeting_id) 


def test_zoom_api_calls_get_meetings():
    # GIVEN a meeting ID 
    user_id = Mock()
    zoom_api = ZoomAPI()
    zoom_api._get_access_token = Mock()
    zoom_api._get_access_token.return_value = 'open sesame'

    # WHEN the zoom api get meeting method is called
    with patch("external.zoom_api.api.get_meetings") as get_meetings:
        zoom_api.get_meetings(user_id=user_id)
        
    get_meetings.assert_called_with(access_token='open sesame', user_id=user_id) 



@mark.parametrize("status,num", [('approved', 2), ('pending', 0), ('denied', 1)])
def test_get_registrants_gets_right_number_of_registrants_from_meeting_id(access_token, status, num):
    # Given a meeting id
    meeting_id = '838 4730 7377'

    # When we ask for zoom meeting
    zoom_api = ZoomAPI()
    registrants = list_registrants(access_token=access_token, meeting_id=meeting_id, status=status)

    # THEN
    assert len(registrants) == num


    