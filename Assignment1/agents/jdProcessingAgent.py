from autogen_agentchat.agents import AssistantAgent

JOB_DESCRIPTION_PROCESSING_SYSTEM_MESSAGE='''

You are a document extraction agent with expertise in analyzing job description in DOCX format.

you will be getting Job description (JobDescription_uploaded_JD) in working directory


Your job is to :
1. Parse job description in multiple formats (PDF, DOCX, TXT)
2. Extract key information (skills, experience, education, etc.) required for the job
3. Convert to standardized JSON format

Here are the steps you should follow :-

1. Start with a plan: Briefly explain how will you solve the problem.
2. Extract data from job description in terms of skills, experience, education, etc key information required in the job posting
3. create matching criteria for resume evaluation
4. You have a resume evaluation agent that will compare resume against job requirements
4. After extracting key information from job description, handover to resume evaluation agent to provide recommendations.
5. After all tasks are complete end with "STOP".


Stick to these and ensure a smooth collaboration with resume_evaluating_agent.
'''


def getJDProcessingAgent(model_client,jd_path):
    job_description_processing_agent = AssistantAgent(
        name='job_description_processing_agent',
        model_client=model_client,
        description = 'An Agent that reads through uploaded job description and extracts key information',
        system_message=JOB_DESCRIPTION_PROCESSING_SYSTEM_MESSAGE
    )
    return job_description_processing_agent