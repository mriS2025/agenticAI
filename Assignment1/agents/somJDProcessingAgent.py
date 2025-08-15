from autogen_agentchat.agents import SocietyOfMindAgent


def getSOMJDProcessingAgent(jdTeam, model_client):
    jdProcessingAgentSOM = SocietyOfMindAgent(
        name='society_of_mind_JD_processing',
        description = 'Society of mind agent with inner team as JD Processing team',
        team=jdTeam,
        model_client=model_client
    )
    return jdProcessingAgentSOM

