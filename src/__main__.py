import psycopg2
from os import getenv
from robyn import Robyn,Request, Response

from models import Survey, UserResponse, SessionLocal

from dotenv import load_dotenv
load_dotenv()
from extractor import get_all_questions
from log import logger
app = Robyn(__file__)


from utils import create_survey,save_user_response,get_survey_with_id,get_all_surveys

@app.before_request()
def before_req(request):
    logger.debug(f"request recieved --> {request.method} : {request.url.path}  body : {request.body}")
    return request

@app.after_request()
def after_req(response):
    logger.debug(f"request completed --> status: {response.status_code} desc :{response.description}")
    return response

@app.get("/surveys")
def get_users():
    try:
        with SessionLocal() as session:
            surveys = get_all_surveys(session)
        return {"data": surveys}
    except Exception as e:
        logger.error(f"Error whie fething all surveys {e}")
        return {"error":"error while fetching all surveys"}


@app.post("/create-survey")
async def create_survey_handler(request: Request):
    try:
        data =  request.json()
        with SessionLocal() as session:

            response = create_survey(session,data)

            if response["status"] == "success":
                return {"description": "Survey created successfully", "survey_id": response["survey_id"]}
            else:
                logger.error(f"error while creating survey {response['message']}")
                return {"error": "Could not create survey", "message": response["message"]}

    except Exception as e:
        logger.error(f"Error while creating survey: {e}")
        return {"error": "Internal server error"}

import json

@app.get("/survey")
async def get_survey_questions(request):
    try:
        survey_id = request.query_params.get("survey_id",None)

        if survey_id is None:
            logger.error("Survey id was not provided")
            return {"error":"please provide survey_id"}
        logger.info(f"survey_id in query params : {survey_id}")        
        questions = get_all_questions(survey_id=survey_id)
        logger.info(f"question fetched from db success for survey_id : {survey_id}")
        return questions
    except Exception as e:
        logger.error(f"error while fetching survey questions {e}")
        return {"error":"cannot fetch survey data"}
    
@app.get("/surveys/all")
async def get_survey_questions(request):
    data = [
            {
                "id": "3f95e50bddf24121bf9f7f4cc8e98376",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "95b44ea894144291aeee0735b299889b",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "37942a7aca3649f98e1d65cf6e549f04",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "975f84ef12074c3e8bde89be4413c39f",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "e629bcf48aa84b62a9cffe39762dc3de",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "8d2af7be28034566b376c2386707ae65",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "de9cb1e3ddde43da8dd6b071df95c776",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "6f1f56fea27040478a26bb92f71a1752",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "4c40852df02f43c59e5aa49795d14436",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "f2576bd6fc114041a99ef6c67b771852",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "76625780a50740c1a1144a566ae19765",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "f203d181dd264c6aaed46bf2614d10db",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "76783fc355c745daae1bcf81f013c89a",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "43d2165c5b3f43d6a88b5343d61f9ac6",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "c4d370e5559b42b38f5291d4bd908c83",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "522deacd76974ef6a8ad020ff3f49562",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "30ec61c58a3a4d35b083b8416b6be6eb",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "08305b6502634a5db2697b2d6984348d",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "ca33643b4c9445b48467a1f382321b0f",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "ba08220b3dab4032b746ae0efd0bc222",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "9081eb7f026b4902a45101dfdc22569b",
                "name": "CES_survey",
                "title": "ces_survey"
            },
            {
                "id": "4169f0ce0f94417baba4f9206287bc0e",
                "name": "CES_survey",
                "title": "ces_survey"
            }
        ]
    return json.dumps(data)

@app.post("/user-response")
async def save_survey_response(request):
    try:
        data = request.json()

        required_fields = ["user_id", "survey_id", "responses", "tenant", "channel_id", "status"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            logger.error(f"Missing required fields: {', '.join(missing_fields)}")
            return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

        with SessionLocal() as session:
            survey =  get_survey_with_id(session,data['survey_id'])
            if survey is None:
                logger.error(f"Survey_id is invalid : {data['survey_id']}")
                return {"error":"survey_id is invalid"}

            record = save_user_response(session,data)

            if record["status"] == "success":
                return {"description": "User response saved successfully", "response_id": record["response_id"]}
            else:
                logger.error(f"error while saving user response {record['message']}")
                return {"error": "Could not save user response", "message": record["message"]}
            
    except Exception as e:
        logger.error(f"Error while saving survey response: {e}")
        return {"error": "Error while saving user response"}


@app.get("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
