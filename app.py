import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import tempfile
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from etl.extract import transcribe_audio
from etl.load import init_db, log_meeting, log_actions
from utils.google_api import get_gmail_service, send_email
from google.auth.exceptions import RefreshError

st.set_page_config(page_title="MeetScribe", layout="wide")
st.title("🎙️ MeetScribe")
st.caption("Hello and Welcome to MeetScribe-AI. Turn any meeting audio into Transcript + Tasks + Decisions + Follow-ups.")
st.caption("100% Offline. Upload audio → Transcript → Smart Actions → DB")

init_db()

@st.cache_resource
def load_llm():
    with st.spinner("Loading Qwen2.5 ... May take 5 - 10 minutes for the first run"):
        model_name = "Qwen/Qwen2.5-7B-Instruct"
        # model_name = "Qwen/Qwen2.5-1.5B-Instruct" -- Use this model for faster load guys.
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=1024, temperature=0.1, do_sample=False, return_full_text=False)
    return tokenizer, pipe

tokenizer, llm = load_llm()
st.success("✅ LLM Successfully Loaded and Ready")

def extract_actions_qwen(transcript):
    system_prompt = """Extract actions. Return ONLY JSON: {"tasks": ["..."], "decisions": ["..."], "followups": ["..."]}. Reply in the SAME language as the transcript. All values must be strings."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript:\n{transcript}"}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    result = llm(prompt, max_new_tokens=512)[0]['generated_text']
    try:
        result = json.loads(result.strip().replace("```json", "").replace("```", ""))
        actions_list = []
        for t in result.get("tasks", []): actions_list.append({"type":"task","text":str(t),"owner":None,"due":None})
        for d in result.get("decisions", []): actions_list.append({"type":"decision","text":str(d),"owner":None,"due":None})
        for f in result.get("followups", []): actions_list.append({"type":"followup","text":str(f),"owner":None,"due":None})
        return result, actions_list
    except: return {"tasks": [], "decisions": [], "followups": []}, []

def generate_summary_qwen(transcript):
    system_prompt = "Summarize this meeting transcript in 5 bullet points. Reply in the SAME language as the transcript."
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript:\n{transcript}"}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return llm(prompt, max_new_tokens=512)[0]['generated_text']

uploaded_file = st.file_uploader("Upload Meeting Audio", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    meeting_title = st.text_input("Meeting Title", value=uploaded_file.name)
    attendees = st.text_input("Attendees - comma separated", value="")

    if st.button("Process Meeting", type="primary"):
        with st.spinner("Transcribing..."):
            transcript, segments = transcribe_audio(tmp_path)
        with st.spinner("Working My Magic..."):
            actions_json, actions_list = extract_actions_qwen(transcript)
            summary = generate_summary_qwen(transcript)

        meeting_id = log_meeting(meeting_title, transcript, attendees)
        log_actions(meeting_id, actions_list)
        st.success(f"✅ Saved to DB with ID: {meeting_id}")

        tab1, tab2, tab3, tab4 = st.tabs(["📝 Transcript", "✨ AI Summary", "✅ Actions", "📧 Send Summary"])

        with tab1: st.text_area("Full Transcript", transcript, height=400)
        with tab2:
            st.markdown(summary)
            st.download_button("Download Summary", summary, file_name=f"{meeting_title}_summary.txt")
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1: st.subheader("Tasks"); [st.checkbox(t) for t in actions_json.get("tasks", [])]
            with col2: st.subheader("Decisions"); [st.write(f"- {d}") for d in actions_json.get("decisions", [])]
            with col3: st.subheader("Follow-ups"); [st.write(f"- {f}") for f in actions_json.get("followups", [])]
        with tab4:
            st.subheader("Send via Gmail")
            email_list = st.text_area("To emails, comma separated")
            email_body = f"Meeting: {meeting_title}\n\nSummary:\n{summary}\n\nActions:\n{json.dumps(actions_json, indent=2)}"
            if st.button("Send Email"):
                try:
                    service = get_gmail_service(st.secrets["gmail"])
                    for email in [e.strip() for e in email_list.split(",") if e]:
                        send_email(service, email, f"MeetScribe: {meeting_title}", email_body)
                    st.success(f"✅ Sent to {len([e for e in email_list.split(',') if e])} people")
                except KeyError: st.error("Add [gmail] to.streamlit/secrets.toml first")
                except RefreshError: st.error("Token expired. Re-run get_google_token.py")

    os.remove(tmp_path)

st.markdown("---")
st.caption("💡 Built with Streamlit •  LLM: Qwen2.5, Whisperer •  Deployment: Hugging Face Spaces")
st.caption("© 2026 Avash's MeetScribe Platform. All rights reserved.")