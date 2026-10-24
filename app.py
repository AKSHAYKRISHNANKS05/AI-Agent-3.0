
import streamlit as st
import tempfile
import os

from faster_whisper import WhisperModel
import av

# Compatibility fix for PyAV
original_av_open = av.open

def compatible_av_open(*args, **kwargs):
    kwargs.pop("metadata_errors", None)
    return original_av_open(*args, **kwargs)

av.open = compatible_av_open
from agent import run_task


# Load Whisper model only once
@st.cache_resource
def load_whisper_model():
    return WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8"
    )


# Page configuration
st.set_page_config(
    page_title="AI Agent 3.0",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Agent 3.0")
st.caption("Your Personal AI Assistant")


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("🤖 AI Agent 3.0")

    st.write("Your Personal AI Assistant")

    st.divider()

    st.subheader("Features")

    st.write("💬 AI Chat")
    st.write("🌐 Browser Automation")
    st.write("📁 File Management")
    st.write("🧠 Personal Memory")

    st.divider()

    st.caption("Powered by Akshay Krishnan")


# ---------------- CHAT HISTORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Clear Chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Ask your AI Agent something...",
    accept_audio=True,
    audio_sample_rate=16000
)


# ---------------- AGENT EXECUTION ----------------


if prompt:

    # Handle typed messages and microphone recordings
    if isinstance(prompt, str):
        user_message = prompt

    else:
        user_message = prompt.text or ""

        # If the user recorded audio, transcribe it automatically
        if prompt.audio is not None:
            audio_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".wav"
                ) as temp_file:
                    temp_file.write(prompt.audio.getvalue())
                    audio_path = temp_file.name

                with st.spinner("🎤 Converting your voice into text..."):
                    model = load_whisper_model()

                    segments, info = model.transcribe(
                        audio_path,
                        language="en",
                        beam_size=3,
                        vad_filter=True
                    )

                    voice_text = " ".join(
                        segment.text.strip()
                        for segment in segments
                    ).strip()

                if voice_text:
                    user_message = (
                        f"{user_message} {voice_text}"
                    ).strip()

            except Exception as e:
                st.error(f"Voice recognition error: {e}")
                st.exception(e)

            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)

    # Send recognised speech or typed text to the agent
    if user_message.strip():

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        try:
            with st.spinner("AI Agent is working..."):
                try:
                    results = run_task(user_message)

                except Exception as error:
                    if "ollama" in str(error).lower() or "connection" in str(error).lower():
                        results = [{
                            "task": user_message,
                            "result": (
                                "⚠️ Cannot connect to Ollama. "
                                "Please start Ollama and try again."
                            )
                        }]
                    else:
                        results = [{
                            "task": user_message,
                            "result": f"Something went wrong: {error}"
                        }]

                output = []

                for item in results:
                    if isinstance(item, dict):
                        output.append(
                            f"**Task:** {item['task']}\n\n"
                            f"**Result:** {item['result']}"
                        )
                    else:
                        output.append(str(item))

                response = "\n\n---\n\n".join(output)

        except Exception as e:
            response = f"Something went wrong: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)

    else:
        st.warning("No speech was recognised. Please try recording again.")
