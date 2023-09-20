
import os
from unittest.mock import Mock
from adapters.list_workshops_presenter_pprint import PPrintListWorkshopPresenter
from main import create_app
from pytest import mark

def test_all_workshops_viewed_irrespective_of_credentials():
    test_user_env = '../.env'
    assert os.path.exists(test_user_env)
    workshop_id = "83847307377"
    app = create_app(env_file = test_user_env)
    app.workshop_workflow.presenter = Mock(PPrintListWorkshopPresenter)
    presenter = app.workshop_workflow.presenter

    app.list_upcoming_workshops()
    upcoming_workshops = presenter.show.call_args[1]['upcoming_workshops']
    assert any(workshop.id == workshop_id for workshop in upcoming_workshops)

    