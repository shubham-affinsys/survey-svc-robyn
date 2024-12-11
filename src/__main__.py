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
