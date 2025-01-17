import sys
from functools import reduce

def jsonLogic(tests, data=None):
    # Base case: return primitive values as-is
    if tests is None or not isinstance(tests, dict):
        return tests

    data = data or {}

    # Extract the operation and its arguments
    op, values = next(iter(tests.items()))

    # Supported operations
    operations = {
        "==": lambda a, b: a == b,
        "===": lambda a, b: a is b,
        "!=": lambda a, b: a != b,
        "!==": lambda a, b: a is not b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": lambda a, b, c=None: a < b if c is None else a < b < c,
        "<=": lambda a, b, c=None: a <= b if c is None else a <= b <= c,
        "!": lambda a: not a,
        "and": lambda *args: all(args),
        "or": lambda *args: any(args),
        "?": lambda a, b, c: b if a else c,
        "var": lambda a, not_found=None: reduce(
            lambda d, k: d.get(k, not_found) if isinstance(d, dict) else not_found,
            str(a).split("."),
            data,
        ),
    }

    if op not in operations:
        raise RuntimeError(f"Unrecognized operation '{op}'")

    # Ensure values are a list for unary operators or single arguments
    if not isinstance(values, (list, tuple)):
        values = [values]

    # Recursively evaluate arguments
    evaluated_values = [jsonLogic(val, data) for val in values]

    # Apply the operation with evaluated arguments
    return operations[op](*evaluated_values)

true=True
false = False

def get_next_question(operation, data):
    next_question = []
    for op in operation:
        if "if" in op:
            condition, actions = op["if"]
            if jsonLogic(condition, data):
                for action in actions:
                    if "update" in action and not action["update"]["body"]["hide"]:
                        entity = action["update"]["entity"][0]
                        next_question.append(entity.split(".")[-1])  
                break
    return next_question


from utils import get_survey_with_id
from models import SessionLocal
import json
from log import logger

def get_all_questions(survey_id):
    
    with SessionLocal() as session:
        try:
            survey = get_survey_with_id(session=session,survey_id=survey_id)
            if not survey:
                return {"error":"Not Found"}
            survey_data = survey.get("survey_data",None)
            survey_data = json.loads(survey_data)
        except Exception as e:
            logger.error(f"error while extracting question from survey {e}")
    if survey_data is None:
        return {"error":"Not Found"}

    formatted_questions = {}

    for question in survey_data:
        f_ques  = {"id": question.get("id"), "label": question.get("label"), "type": question.get("type")}

        action  = question.get('actions',None)
        if action:
            # get condition for next question
            operation = action[0].get("operation")
            f_ques['rules'] = operation

        if question.get("valuesAllowed",None):
            options  = question.get("valuesAllowed").get("options")
            f_options = []

            for option in options:
                f_option = {}
                f_option["type"] = "payload"
                f_option["title"] = option.get("display_value")
                f_option["payload"] = option.get("api_value")
                f_options.append(f_option)

            f_ques["options"] = f_options

        formatted_questions[f_ques.get("id")]=f_ques
    return  formatted_questions

