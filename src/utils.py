
from models import Survey
from log import logger
import uuid
import json
from sqlalchemy.future import select

from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Optional

def get_survey_with_id(session: Session, survey_id: str) -> Optional[Survey]:
    """
    Fetch a survey record by its ID.

    Args:
        session (Session): The SQLAlchemy session to use for the query.
        survey_id (str): The ID of the survey to fetch.

    Returns:
        Optional[Survey]: The survey record if found, otherwise None.
    """
    try:
        record = session.query(Survey).filter(Survey.survey_id == survey_id).first()
        record = record.as_dict()
        if not record:
            logger.warning(f"Survey with ID {survey_id} not found.")
        return record
    except Exception as e:
        logger.error(f"Error while fetching survey from DB: {e}")
        return None


from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

from uuid import uuid4

def create_survey(session:Session, data: dict) -> dict:
    """
    Create a new survey record in the database.
    
    Args:
        data (dict): A dictionary containing survey details:
                     - "title": The title of the survey
                     - "description": The description of the survey
                     - "survey_data": JSON data for the survey content
                     - "tenant": The tenant ID
                     
    Returns:
        dict: A response dictionary with the created survey ID or an error message.
    """

    try:
        with  session:
            survey_id = data.get("survey_id", str(uuid4()))
            new_survey = Survey(
                survey_id=survey_id,
                title=data.get("title"),
                description=data.get("description"),
                survey_data=data.get("survey_data"),
                created_at=data.get("created_at", datetime.now(timezone.utc)),
                tenant=data.get("tenant"),
            )
            session.add(new_survey)
            session.commit()
            session.refresh(new_survey)
            return {"status": "success", "survey_id": new_survey.survey_id}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}
