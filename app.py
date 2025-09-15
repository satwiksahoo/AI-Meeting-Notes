# import os, json
# import streamlit as st
# from utils.asr import Transcriber
# from utils.rag import RAGIndex
# from utils.summarize import summarize_text
# from utils.emailer import send_summary
# from utils.pdf_exporter import create_summary_pdf

# st.set_page_config(page_title='AI Meeting Notes', layout='wide')
# st.title('🎧 AI Meeting Notes & Action Items Generator')

# with st.sidebar:
#     st.header('Settings')
#     whisper_size = st.selectbox('Whisper model', ['tiny','base','small','medium','large-v3'], index=2)
#     emails = st.text_input('Team emails (comma-separated)')
#     st.markdown('Run an Ollama server locally (optional) and set LLM model in .env')

# @st.cache_resource
# def get_transcriber(size):
#     os.environ['WHISPER_MODEL'] = size
#     return Transcriber(model_size=size)

# @st.cache_resource
# def get_rag():
#     idx = RAGIndex(persist_dir='rag_index')
#     idx.index_folder('knowledge_base')
#     return idx

# uploaded = st.file_uploader('Upload meeting audio (wav/mp3/m4a)', type=['wav','mp3','m4a'])
# if uploaded:
#     os.makedirs('data/audio', exist_ok=True)
#     path = os.path.join('data/audio', uploaded.name)
#     with open(path, 'wb') as f:
#         f.write(uploaded.read())
#     st.audio(path)

#     st.subheader('1) Transcription')
#     with st.spinner('Transcribing with Whisper…'):
#         transcriber = get_transcriber(whisper_size)
#         out = transcriber.transcribe(path)
#     st.success(f"Detected language: {out.get('language')}")
#     st.text_area('Transcript', value=out.get('text',''), height=240)

#     st.subheader('2) Retrieve KB context (RAG)')
#     rag = get_rag()
#     hits = rag.query(out.get('text',''), k=4)
#     with st.expander('Show KB matches'):
#         for i,h in enumerate(hits,1):
#             st.markdown(f"**KB#{i} — {h['source']}**\n\n{h['text'][:600]}..." )

#     st.subheader('3) Summarize → Key Points, Decisions, Action Items')
#     if st.button('Generate Summary'):
#         with st.spinner('Summarizing with LLM…'):
#             summary = summarize_text(out.get('text',''), hits)
#         st.session_state['summary'] = summary

#     if 'summary' in st.session_state:
#         summary = st.session_state['summary']
#         col1,col2,col3 = st.columns(3)
#         # with col1:
#         st.markdown('### Key Points')
#             # kp = st.data_editor(summary.get('key_points', []), num_rows='dynamic')
            
#         kp = st.data_editor(
#     summary.get('key_points', []),
#     num_rows="dynamic",
#     key="key_points_editor"
# )
#         # with col2:
#         st.markdown('### Decisions')
#             # ds = st.data_editor(summary.get('decisions', []), num_rows='dynamic')
            
#         ds = st.data_editor(
#     summary.get('decisions', []),
#     num_rows="dynamic",
#     key="decisions_editor"
# )
#         # with col3:
#         st.markdown('### Action Items (owner, task, due_date, priority)')
#             # ai = st.data_editor(summary.get('action_items', []), num_rows='dynamic')
            
#         ai = st.data_editor(
# summary.get('action_items', []),
#     num_rows="dynamic",
#     key="action_items_editor"
# )
        
# pdf_bytes = create_summary_pdf(summary)
# st.download_button(
#     "⬇️ Download PDF",
#     data=pdf_bytes,
#     file_name="meeting_summary.pdf",
#     mime="application/pdf"
# )
         
         
         
# if st.button('Save Edits'):
#             summary['key_points'] = kp
#             summary['decisions'] = ds
#             summary['action_items'] = ai
#             st.session_state['summary'] = summary
#             st.success('Edits saved.')

# #         st.download_button('⬇️ Download JSON', data=json.dumps(summary, indent=2), file_name='meeting_summary.json')

# #         if emails.strip():
# #             if st.button('📧 Email Summary'):
# #                 to_list = [e.strip() for e in emails.split(',') if e.strip()]
# #                 try:
# #                     send_summary(summary, to_list, subject='Meeting Summary & Action Items')
# #                     st.success('Email sent!')
# #                 except Exception as e:
# #                     st.error(f'Email failed: {e}')
# # else:
# #     st.info('Upload a short meeting audio (2-10 min) to try the demo.')



# import os, json
# import streamlit as st
# from utils.asr import Transcriber
# from utils.rag import RAGIndex
# from utils.summarize import summarize_text
# from utils.emailer import send_summary
# from utils.pdf_exporter import create_summary_pdf

# st.set_page_config(page_title='AI Meeting Notes', layout='wide')
# st.title('🎧 AI Meeting Notes & Action Items Generator')

# with st.sidebar:
#     st.header('Settings')
#     whisper_size = st.selectbox('Whisper model', ['tiny', 'base', 'small', 'medium', 'large-v3'], index=0)
#     emails = st.text_input('Team emails (comma-separated)')
#     st.markdown('Run an Ollama server locally (optional) and set LLM model in .env')


# @st.cache_resource
# def get_transcriber(size):
#     os.environ['WHISPER_MODEL'] = size
#     return Transcriber(model_size=size)


# @st.cache_resource
# def get_rag():
#     idx = RAGIndex(persist_dir='rag_index')
#     idx.index_folder('knowledge_base')
#     return idx


# uploaded = st.file_uploader('Upload meeting audio (wav/mp3/m4a)', type=['wav', 'mp3', 'm4a'])
# if uploaded:
#     os.makedirs('data/audio', exist_ok=True)
#     path = os.path.join('data/audio', uploaded.name)
#     with open(path, 'wb') as f:
#         f.write(uploaded.read())
#     st.audio(path)

#     st.subheader('1) Transcription')
    
#     if "transcript" not in st.session_state:    
#         with st.spinner('Transcribing with Whisper…'):
#             transcriber = get_transcriber(whisper_size)
#             out = transcriber.transcribe(path)
#             st.session_state["transcript"] = out
#     else:
#         out = st.session_state["transcript"]
    
#     st.success(f"Detected language: {out.get('language')}")
#     st.text_area('Transcript', value=out.get('text', ''), height=240)

#     st.subheader('2) Retrieve KB context (RAG)')
    
  
    
#     if "rag_hits" not in st.session_state:
#         rag = get_rag()
#         st.session_state["rag_hits"] = rag.query(out.get('text', ''), k=4)
    
#     # hits = rag.query(out.get('text', ''), k=4)
#     hits = st.session_state["rag_hits"] 
#     with st.expander('Show KB matches'):
#         for i, h in enumerate(hits, 1):
#             st.markdown(f"**KB#{i} — {h['source']}**\n\n{h['text'][:600]}...")

#     st.subheader('3) Summarize → Key Points, Decisions, Action Items')
#     if st.button('Generate Summary'):
#         with st.spinner('Summarizing with LLM…'):
#             summary = summarize_text(out.get('text', ''), hits)
#         st.session_state['summary'] = summary

#     if 'summary' in st.session_state:
#         summary = st.session_state['summary']
#         col1, col2, col3 = st.columns(3)

#         # with col1:
#         st.markdown('### Key Points')
#         kp = st.data_editor(
#                 summary.get('key_points', []),
#                 num_rows="dynamic",
#                 key="key_points_editor",
#                 height=500,                # 👈 adjust height (in pixels)
#                 use_container_width=True   # 👈 make it full width of the column
#             )

#         # with col2:
#         st.markdown('### Decisions')
#         ds = st.data_editor(
#                 summary.get('decisions', []),
#                 num_rows="dynamic",
#                 key="decisions_editor",
#                 height=500,                # 👈 adjust height (in pixels)
#                 use_container_width=True   # 👈 make it full width of the column
#             )

#         # with col3:
#         st.markdown('### Action Items (owner, task, due_date, priority)')
#         ai = st.data_editor(
#                 summary.get('action_items', []),
#                 num_rows="dynamic",
#                 key="action_items_editor",
#                 height=500,                # 👈 adjust height (in pixels)
#                 use_container_width=True   # 👈 make it full width of the column
#             )

#         pdf_bytes = create_summary_pdf(summary)
#         st.download_button(
#             "⬇️ Download PDF",
#             data=pdf_bytes,
#             file_name="meeting_summary.pdf",
#             mime="application/pdf"
#         )

#         if st.button('Save Edits'):
#             summary['key_points'] = kp
#             summary['decisions'] = ds
#             summary['action_items'] = ai
#             st.session_state['summary'] = summary
#             st.success('Edits saved.')

#         # st.download_button('⬇️ Download JSON', data=json.dumps(summary, indent=2), file_name='meeting_summary.json')

#         if emails.strip():
#             if st.button('📧 Email Summary'):
#                 to_list = [e.strip() for e in emails.split(',') if e.strip()]
#                 try:
#                     send_summary(summary, to_list, subject='Meeting Summary & Action Items')
#                     st.success('Email sent!')
#                 except Exception as e:
#                     st.error(f'Email failed: {e}')
#         else:
#             st.info('Upload a short meeting audio (2-10 min) to try the demo.')




import os, json
import os
os.environ["STREAMLIT_WATCHDOG"] = "false"
import streamlit as st
from utils.asr import Transcriber
from utils.rag import RAGIndex
from utils.summarize import summarize_text
from utils.emailer import send_summary
from utils.pdf_exporter import create_summary_pdf

import warnings
warnings.filterwarnings("ignore", message="Tried to instantiate class '__path__._path'")


st.set_page_config(page_title='AI Meeting Notes', layout='wide')
st.title('🎧 AI Meeting Notes & Action Items Generator')

with st.sidebar:
    st.header('Settings')
    whisper_size = st.selectbox('Whisper model', ['tiny', 'base', 'small', 'medium', 'large-v3'], index=0)
    emails = st.text_input('Team emails (comma-separated)')
    # st.markdown('Run an Ollama server locally (optional) and set LLM model in .env')


@st.cache_resource
def get_transcriber(size):
    os.environ['WHISPER_MODEL'] = size
    return Transcriber(model_size=size)


@st.cache_resource
def get_rag():
    idx = RAGIndex(persist_dir='rag_index')
    idx.index_folder('knowledge_base')
    return idx


uploaded = st.file_uploader('Upload meeting audio (wav/mp3/m4a)', type=['wav', 'mp3', 'm4a'])
if uploaded:
    os.makedirs('data/audio', exist_ok=True)
    path = os.path.join('data/audio', uploaded.name)
    with open(path, 'wb') as f:
        f.write(uploaded.read())
    st.audio(path)

    # 🔄 Reset state if new file uploaded
    if "last_file" not in st.session_state or st.session_state["last_file"] != uploaded.name:
        st.session_state.clear()
        st.session_state["last_file"] = uploaded.name

    # ----------------
    # 1) Transcription
    # ----------------
    st.subheader('1) Transcription')
    
    if "transcript" not in st.session_state:    
        # with st.spinner('Transcribing with Whisper…'):
        #     transcriber = get_transcriber(whisper_size)
        #     out = transcriber.transcribe(path)
        #     st.session_state["transcript"] = out
        transcriber = get_transcriber(whisper_size)
        with st.spinner(f"Processing audio... This may take a few minutes for long files."):
            # Optional: split audio into chunks (if your Transcriber supports it)
            out = transcriber.transcribe(path, chunk_ms=60_000)  # 1 min chunks
        st.session_state["transcript"] = out

    else:
        out = st.session_state["transcript"]
    
    st.success(f"Detected language: {out.get('language')}")
    st.text_area('Transcript', value=out.get('text', ''), height=240)

    # ----------------
    # 2) RAG retrieval
    # ----------------
    st.subheader('2) Retrieve KB context (RAG)')

    if "rag_hits" not in st.session_state:
        # rag = get_rag()
        # st.session_state["rag_hits"] = rag.query(out.get('text', ''), k=4)
        rag = get_rag()
        with st.spinner("Indexing knowledge base..."):
            rag.index_folder("knowledge_base")  # Only needed if you want to re-index
        st.session_state["rag_hits"] = rag.query(out.get('text', ''), k=4)


    hits = st.session_state["rag_hits"]

    with st.expander('Show KB matches'):
        for i, h in enumerate(hits, 1):
            st.markdown(f"**KB#{i} — {h['source']}**\n\n{h['text'][:600]}...")

    # ----------------
    # 3) Summarization
    # ----------------
    st.subheader('3) Summarize → Key Points, Decisions, Action Items')

    if st.button('Generate Summary'):
        with st.spinner('Summarizing with LLM…'):
            summary = summarize_text(out.get('text', ''), hits)
        st.session_state['summary'] = summary

    if 'summary' in st.session_state:
        summary = st.session_state['summary']
        col1, col2, col3 = st.columns(3)

        # Key Points
        # with col1:
        st.markdown('### Key Points')
        kp = st.data_editor(
                summary.get('key_points', []),
                num_rows="dynamic",
                key="key_points_editor",
                height=500,
                use_container_width=True
            )

        # Decisions
        # with col2:
        st.markdown('### Decisions')
        ds = st.data_editor(
                summary.get('decisions', []),
                num_rows="dynamic",
                key="decisions_editor",
                height=500,
                use_container_width=True
            )

        # Action Items
        # with col3:
        st.markdown('### Action Items (owner, task, due_date, priority)')
        ai = st.data_editor(
                summary.get('action_items', []),
                num_rows="dynamic",
                key="action_items_editor",
                height=500,
                use_container_width=True
            )

        # PDF download
        pdf_bytes = create_summary_pdf(summary)
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes,
            file_name="meeting_summary.pdf",
            mime="application/pdf"
        )

        # Save edits
        if st.button('Save Edits'):
            summary['key_points'] = kp
            summary['decisions'] = ds
            summary['action_items'] = ai
            st.session_state['summary'] = summary
            st.success('Edits saved.')

        # Email option
        if emails.strip():
            if st.button('📧 Email Summary'):
                to_list = [e.strip() for e in emails.split(',') if e.strip()]
                try:
                    send_summary(summary, to_list, subject='Meeting Summary & Action Items')
                    st.success('Email sent!')
                except Exception as e:
                    st.error(f'Email failed: {e}')
        else:
            st.info('Upload a short meeting audio (2-10 min) to try the demo.')
