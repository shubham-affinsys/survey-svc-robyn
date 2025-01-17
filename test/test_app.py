# tests/test_app.py
import pytest
from robyn import Request, Response
from robyn import Response
import json
from src.__main__ import app # importing our robyn app

def test_root_route(test_robyn):
    test_client =  app.test_client() # calling our test client via our app instance
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello World!"

def test_get_surveys(test_client,test_robyn):
    test_client =  app.test_client()
    response = test_client.get("/surveys")
    assert response.status_code == 200
    assert "data" in response.json()

def test_create_survey_success(test_client,test_robyn):
    test_client =  app.test_client()
    data = {
        "name": "Test Survey",
        "title": "Test Title",
        "questions": [
            {"question_text": "Question 1"},
            {"question_text": "Question 2"}
        ]
    }
    response = test_client.post("/create-survey", json=data)
    assert response.status_code == 200
    assert "survey_id" in response.json()
    assert response.json()["description"] == "Survey created successfully"
    
def test_create_survey_failure(test_client,test_robyn):
    test_client =  app.test_client()
    data = {
        "name": "Test Survey",
        "questions": [
            {"question_text": "Question 1"},
            {"question_text": "Question 2"}
        ]
    }
    response = test_client.post("/create-survey", json=data)
    assert response.status_code == 200
    assert "error" in response.json()
    assert "Could not create survey" in response.json()["error"]

def test_get_survey_questions_success(test_client,test_robyn):
    test_client =  app.test_client()
     # Assume you have a survey with id '123' in the db
    response = test_client.get("/survey", params={"survey_id": "9081eb7f026b4902a45101dfdc22569b"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_survey_questions_failure(test_client,test_robyn):
    test_client =  app.test_client()
    response = test_client.get("/survey")
    assert response.status_code == 200
    assert "error" in response.json()
    assert "please provide survey_id" in response.json()["error"]

def test_options_surveys_all(test_client,test_robyn):
    test_client =  app.test_client()
    response = test_client.options("/surveys/all")
    assert response.status_code == 204

def test_get_surveys_all(test_client,test_robyn):
    test_client =  app.test_client()
    response = test_client.get("/surveys/all")
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

def test_save_user_response_success(test_client,test_robyn):
    test_client =  app.test_client()
    data = {
        "user_id": "user123",
        "survey_id": "9081eb7f026b4902a45101dfdc22569b",
        "responses": [
            {"question_id": "q1", "answer": "answer1"},
            {"question_id": "q2", "answer": "answer2"},
        ],
        "tenant": "tenant1",
        "channel_id": "channel1",
        "status": "complete"
    }
    response = test_client.post("/user-response", json=data)
    assert response.status_code == 200
    assert "response_id" in response.json()
    assert response.json()["description"] == "User response saved successfully"

def test_save_user_response_failure(test_client,test_robyn):
    test_client =  app.test_client()
    data = {
        "user_id": "user123",
        "survey_id": "9081eb7f026b4902a45101dfdc22569b",
        "responses": [
            {"question_id": "q1", "answer": "answer1"},
            {"question_id": "q2", "answer": "answer2"},
        ],
         "channel_id": "channel1",
        "status": "complete"
    }
    response = test_client.post("/user-response", json=data)
    assert response.status_code == 200
    assert "error" in response.json()
    assert "Missing required fields: tenant" in response.json()["error"]