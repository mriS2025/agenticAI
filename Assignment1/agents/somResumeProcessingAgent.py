from autogen_agentchat.agents import SocietyOfMindAgent


def getSOMResumeProcessingAgent(resumeTeam, model_client):
    resumeProcessingAgentSOM = SocietyOfMindAgent(
        name='society_of_mind_Resume_processing',
        description = 'Society of mind agent with inner team as Resume Processing team',
        team=resumeTeam,
        model_client=model_client
    )
    return resumeProcessingAgentSOM

