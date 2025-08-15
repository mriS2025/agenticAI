import streamlit as st
import uuid
import glob
import re
import asyncio
import os
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

from config.dockerutil import start_docker_container,stop_docker_container, getDockerCommandLineExecutor

from teams.resumeAssistantTeam import getResumeAssistantTeam
from models.openai_model_client import get_model_client


async def run_resumeAssistant(docker,openai_model_client,task):
    try:
        await start_docker_container(docker)
        #1 parse session id from task string
        match=re.search(r"\| *session_id *= *([a-zA-Z0-9\-]+)",task)
        if not match:
            raise ValueError("Session ID not found in task string.")
        session_id=match.group(1)
        print(f"session_id: {session_id}")

        resume_files=glob.glob(f"/tmp/{session_id}_uploaded_resume_*.pdf")
        print(f"resume_files: {resume_files}")

        jd_files=glob.glob(f"/tmp/{session_id}_uploaded_JD*.docx")
        print(f"jd_files: {jd_files}")

        if not resume_files or not jd_files:
            raise FileNotFoundError(f"Files not found for session ID {session_id}")
        
        resume_path=resume_files[0]
        print(f"resume_path: {resume_path}")
        jd_path=jd_files[0]


        team = getResumeAssistantTeam(openai_model_client, resume_path, jd_path)
        print("team created")

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)


        async for message in team.run_stream(task=task):
            print("inside run stream")
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('resume_processing_agent'):
                    with st.chat_message('Resume Processor',avatar='🤖'):
                        st.markdown(message.content)
                elif message.source.startswith('resume_scoring_agent'):
                    with st.chat_message('Resume Scoring',avatar='👨‍💻'):
                        st.markdown(message.content)
                    # add elif for other agents???
                st.session_state.messages.append(message.content)
                    # st.markdown(f"{message.content}")
            elif isinstance(message,TaskResult):
                st.markdown(f'Stop Reason :{message.stop_reason}')
                st.session_state.messages.append(message.stop_reason)

        st.session_state.autogen_team_state = await team.save_state()
        return None
     
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:   
        await stop_docker_container(docker)


st.title('Resume Assistant') 

uploaded_resume = st.file_uploader("Upload your resume in .PDF format", type=["PDF"])

uploaded_JD= st.file_uploader("Upload your Job description in .docx format", type=["docx"])

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if('images_shown') not in st.session_state:
    st.session_state.images_shown=[] 


task = st.chat_input("Enter your task here...")



if task:
    if uploaded_resume and uploaded_JD:
        #Generate session id
        session_id=str(uuid.uuid4())
        #define file save paths
        save_dir="/tmp"
        resume_path=os.path.join(save_dir,f"{session_id}_uploaded_resume_{uploaded_resume.name}")
        jd_path=os.path.join(save_dir,f"{session_id}_uploaded_JD{uploaded_JD.name}")

        #save uploaded files
        with open(resume_path,"wb") as f:
            f.write(uploaded_resume.read())
        with open(jd_path,"wb") as f:
            f.write(uploaded_JD.read()) 
        
        #task with session reference
        task=task+f"| session_id={session_id}"
        print(f"task: {task}")

        #pass task to agents
        openai_model_client= get_model_client()
        
        docker = getDockerCommandLineExecutor()

        error = asyncio.run(run_resumeAssistant(docker,openai_model_client,task))
    else:
        st.error("please upload both files")




