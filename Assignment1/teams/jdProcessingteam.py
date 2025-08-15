
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.jdProcessingAgent import getJDProcessingAgent
from agents.resumeEvaluationAgent import getResumeEvaluationAgent


def getJDProcessingTeam(model_client, jd_path):

    job_description_processing_agent = getJDProcessingAgent(model_client, jd_path)

    resume_evaluation_agent = getResumeEvaluationAgent(model_client)


    text_mention_termination = TextMentionTermination('STOP')

    jdProcessingTeam = RoundRobinGroupChat(
        participants=[job_description_processing_agent,resume_evaluation_agent],
        max_turns=10,
        termination_condition=text_mention_termination
    )

    return jdProcessingTeam