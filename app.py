
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

from agent import run_task, approve_pending_action


# ---------------- WHISPER MODEL ----------------

@st.cache_resource
def load_whisper_model():
    return WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8"
    )


# ---------------- PAGE CONFIGURATION ----------------

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


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "remaining_tasks" not in st.session_state:
    st.session_state.remaining_tasks = []


# ---------------- HELPER FUNCTION ----------------

def process_agent_result(agent_result):
    """
    Display completed tasks and save any pending action.
    """

    output = []

    for item in agent_result.get("results", []):

        output.append(
            f"**Task:** {item['task']}\n\n"
            f"**Result:** {item['result']}"
        )

    pending = agent_result.get("pending_action")

    if pending:

        st.session_state.pending_action = pending

        st.session_state.remaining_tasks = (
            agent_result.get("remaining_tasks", [])
        )

        output.append(
            "⚠️ **Approval required**\n\n"
            f"Action: `{pending['tool']}`\n\n"
            f"Details: `{pending['argument']}`"
        )

    return "\n\n---\n\n".join(output)


def continue_remaining_tasks():
    """
    Execute the tasks remaining after an approved action.
    """

    remaining = st.session_state.remaining_tasks

    if not remaining:
        return ""

    # Reconstruct the remaining command.
    command = " and then ".join(remaining)

    st.session_state.remaining_tasks = []

    result = run_task(
        command,
        streamlit_mode=True
    )

    return process_agent_result(result)


# ---------------- CLEAR CHAT ----------------

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.pending_action = None
    st.session_state.remaining_tasks = []
    st.rerun()


# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Ask your AI Agent something...",
    accept_audio=True,
    audio_sample_rate=16000,
    disabled=st.session_state.pending_action is not None
)


# ---------------- AGENT EXECUTION ----------------

if prompt:

    # Handle typed messages and microphone recordings
    if isinstance(prompt, str):
        user_message = prompt

    else:
        user_message = prompt.text or ""

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

            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)

    # Process the user's message
    if user_message.strip():

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        try:
            with st.spinner("AI Agent is working..."):

                agent_result = run_task(
                    user_message,
                    streamlit_mode=True
                )

                response = process_agent_result(agent_result)

            if not response:
                response = "The agent did not return a result."

        except Exception as e:

            if (
                "ollama" in str(e).lower()
                or "connection" in str(e).lower()
            ):
                response = (
                    "⚠️ Cannot connect to Ollama. "
                    "Please start Ollama and try again."
                )
            else:
                response = f"Something went wrong: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)

    else:
        st.warning(
            "No speech was recognised. Please try recording again."
        )


# ---------------- CONFIRMATION BUTTONS ----------------

if st.session_state.pending_action is not None:

    pending = st.session_state.pending_action

    st.warning(
        f"Your AI Agent wants to perform: **{pending['tool']}**\n\n"
        f"Details: `{pending['argument']}`"
    )

    col1, col2 = st.columns(2)

    # ---------------- ALLOW ----------------

    with col1:

        if st.button(
            "✅ Allow",
            use_container_width=True
        ):

            try:
                with st.spinner("Executing approved action..."):

                    # Execute the approved action
                    result = approve_pending_action(pending)

                    response = (
                        f"✅ **Action completed**\n\n{result}"
                    )

                    # Clear the current pending action
                    st.session_state.pending_action = None

                    # Continue the remaining tasks
                    next_response = continue_remaining_tasks()

                    if next_response:
                        response += (
                            "\n\n---\n\n"
                            + next_response
                        )

            except Exception as e:

                response = f"❌ **Action failed:** {e}"

                st.session_state.pending_action = None
                st.session_state.remaining_tasks = []

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

    # ---------------- CANCEL ----------------

    with col2:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):

            response = (
                f"❌ Action cancelled: **{pending['tool']}**"
            )

            st.session_state.pending_action = None
            st.session_state.remaining_tasks = []

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()
