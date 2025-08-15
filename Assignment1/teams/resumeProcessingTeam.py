
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.resumeProcessingAgent import getResumeProcessingAgent
from agents.resumeScoringAgent import getResumeScoringAgent
#from agents.resumeUserProxyAgent import getResumeUserProxyAgent

def getResumeProcessingTeam(model_client, resume_path):

    resume_processing_agent = getResumeProcessingAgent(model_client, resume_path)

    resume_scoring_agent = getResumeScoringAgent(model_client)


    text_mention_termination = TextMentionTermination('STOP')

    resumeProcessingTeam = RoundRobinGroupChat(
        participants=[resume_processing_agent,resume_scoring_agent],
        max_turns=20,
        termination_condition=text_mention_termination
    )

    return resumeProcessingTeam