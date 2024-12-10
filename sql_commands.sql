
# CREATING TABLES
CREATE TABLE survey (
    id SERIAL PRIMARY KEY,
    tenant VARCHAR,
    group_name VARCHAR,
    title VARCHAR,
    link VARCHAR,
    data JSONB
);

CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES survey(id) ON DELETE CASCADE,
    text VARCHAR,
    type VARCHAR,
    rule JSONB,
    validation JSONB
);

CREATE TABLE option (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    text VARCHAR,
    value VARCHAR
);

CREATE TABLE user_survey_response (
    id SERIAL PRIMARY KEY,
    profile_id VARCHAR,
    survey_id INTEGER NOT NULL REFERENCES survey(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    option_text VARCHAR,
    option_value VARCHAR,
    user_response VARCHAR,
    created_at TIMESTAMP
);



-- CREATING TABLES
CREATE TABLE survey (
    id SERIAL PRIMARY KEY,
    tenant VARCHAR,
    group_name VARCHAR,
    title VARCHAR,
    link VARCHAR,
    data JSONB
);

CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES survey(id) ON DELETE CASCADE,
    text VARCHAR,
    type VARCHAR,
    rule JSONB,
    validation JSONB
);

CREATE TABLE option (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    text VARCHAR,
    value VARCHAR
);

CREATE TABLE user_survey_response (
    id SERIAL PRIMARY KEY,
    profile_id VARCHAR,
    survey_id INTEGER NOT NULL REFERENCES survey(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    option_text VARCHAR,
    option_value VARCHAR,
    user_response VARCHAR,
    created_at TIMESTAMP
);

-- INSERTING VALUES

-- Insert into `survey`
INSERT INTO survey (tenant, group_name, title, link, data)
VALUES ('tenant1', 'group1', 'Customer Feedback', 'http://survey.link', '{"description": "Survey data"}');

-- Insert into `question`
INSERT INTO question (survey_id, text, type, rule, validation)
VALUES (1, 'What is your age?', 'number', '{"min": 18}', '{"required": true}');

-- Insert into `option`
INSERT INTO option (question_id, text, value)
VALUES (1, '18-25', '18_25'),
       (1, '26-35', '26_35'),
       (1, '36-45', '36_45');

-- Insert into `user_survey_response`
INSERT INTO user_survey_response (profile_id, survey_id, question_id, option_text, option_value, user_response, created_at)
VALUES ('user123', 1, 1, '18-25', '18_25', 'I am in this age group', CURRENT_TIMESTAMP);

-- UPDATING VALUES

-- Update `survey` title
UPDATE survey
SET title = 'Updated Customer Feedback'
WHERE id = 1;

-- Update `question` text
UPDATE question
SET text = 'What is your updated age?'
WHERE id = 1;

-- Update `option` text
UPDATE option
SET text = '18 to 25 years'
WHERE id = 1;

-- Update `user_survey_response` user response
UPDATE user_survey_response
SET user_response = 'Updated response', created_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- DELETING VALUES

-- Delete a specific `survey`
DELETE FROM survey
WHERE id = 1;

-- Delete a specific `question`
DELETE FROM question
WHERE id = 1;

-- Delete a specific `option`
DELETE FROM option
WHERE id = 1;

-- Delete a specific `user_survey_response`
DELETE FROM user_survey_response
WHERE id = 1;

-- BULK INSERT EXAMPLE
INSERT INTO option (question_id, text, value)
VALUES 
    (1, '46-55', '46_55'),
    (1, '56-65', '56_65'),
    (1, '66+', '66_plus');

-- TRANSACTION EXAMPLE
BEGIN;

INSERT INTO survey (tenant, group_name, title, link, data)
VALUES ('tenant2', 'group2', 'Employee Satisfaction', 'http://survey2.link', '{"description": "Employee survey data"}');

INSERT INTO question (survey_id, text, type, rule, validation)
VALUES (2, 'How satisfied are you with your job?', 'text', '{}', '{"required": true}');

COMMIT;

