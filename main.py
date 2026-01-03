import hashlib
import random
from pathlib import Path

import requests
import streamlit as st
import tomllib
from gtts import gTTS

# Dropbox URL (dl=1 for direct download)
DROPBOX_URL = "https://www.dropbox.com/scl/fi/b1bxhq60uomcnt4s9e0u5/chilingo.toml?rlkey=8nc6em3grkv34p1hlgzuzwuuj&st=6bb6bvf3&dl=1"

# Audio cache directory
AUDIO_CACHE_DIR = Path("/tmp/chilingo")


@st.cache_data
def fetch_word_list():
    """Fetch word list from Dropbox and parse TOML."""
    response = requests.get(DROPBOX_URL)
    response.raise_for_status()
    data = tomllib.loads(response.text)
    return data.get("items", [])


def get_audio_path(text: str) -> Path:
    """Generate a unique filename for audio based on text content."""
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return AUDIO_CACHE_DIR / f"{text_hash}.mp3"


def generate_audio(text: str) -> Path:
    """Generate audio file using gTTS, with caching."""
    # Ensure cache directory exists
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    audio_path = get_audio_path(text)

    # Return cached file if it exists
    if audio_path.exists():
        return audio_path

    # Generate new audio file
    print("Generating audio for:", text)
    tts = gTTS(text, lang="zh-cn")
    tts.save(str(audio_path))

    return audio_path


def initialize_session_state():
    """Initialize session state for word order and current index."""
    if "words" not in st.session_state:
        words = fetch_word_list()
        st.session_state.words = words
        st.session_state.order = list(range(len(words)))
        random.shuffle(st.session_state.order)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.quiz_mode = None  # 'text' or 'audio'


def prev_word():
    """Move to the prev word."""
    st.session_state.current_index -= 1
    st.session_state.show_answer = False
    st.session_state.quiz_mode = None

    # Loop back to start if we reach the end
    if st.session_state.current_index < 0:
        st.session_state.current_index = len(st.session_state.order) - 1


def next_word():
    """Move to the next word."""
    st.session_state.current_index += 1
    st.session_state.show_answer = False
    st.session_state.quiz_mode = None

    # Loop back to start if we reach the end
    if st.session_state.current_index >= len(st.session_state.order):
        st.session_state.current_index = 0


def show_answer():
    """Show the answer."""
    st.session_state.show_answer = True


def main():
    st.title("ChiLingo - 中国語単語帳")

    # Initialize session state
    initialize_session_state()

    # Check if we have words
    if not st.session_state.words:
        st.error("単語が見つかりませんでした")
        return

    # Get current word
    word_index = st.session_state.order[st.session_state.current_index]
    word = st.session_state.words[word_index]

    # Progress indicator
    st.progress(
        (st.session_state.current_index + 1) / len(st.session_state.words),
        text=f"単語 {st.session_state.current_index + 1} / {len(st.session_state.words)}",
    )

    # Choose quiz mode if not set
    if st.session_state.quiz_mode is None:
        st.session_state.quiz_mode = random.choice(["text", "audio"])

    st.markdown("---")

    # Quiz mode: Show Chinese text
    if st.session_state.quiz_mode == "text":
        st.markdown(f"## {word['zh']}")

        if not st.session_state.show_answer:
            st.button("答えを表示", on_click=show_answer, use_container_width=True)
        else:
            st.markdown(f"**拼音:** {word['pinyin']}")
            st.markdown(f"**日本語:** {word['ja']}")

            # Generate and play audio
            audio_path = generate_audio(word["zh"])
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

    # Quiz mode: Play audio
    else:
        st.markdown("### 音声を聞いて答えてください")

        # Generate and play audio immediately
        audio_path = generate_audio(word["zh"])
        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        if not st.session_state.show_answer:
            st.button("答えを表示", on_click=show_answer, use_container_width=True)
        else:
            st.markdown(f"## {word['zh']}")
            st.markdown(f"**拼音:** {word['pinyin']}")
            st.markdown(f"**日本語:** {word['ja']}")

    cols = st.columns(2)
    with cols[0]:
        st.button("前へ", on_click=prev_word, use_container_width=True)
    with cols[1]:
        st.button("次へ", on_click=next_word, use_container_width=True)

    st.markdown("---")

    # Reset button in sidebar
    with st.sidebar:
        st.markdown("### 設定")
        if st.button("単語をシャッフル", use_container_width=True):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.quiz_mode = None
            st.rerun()

        if st.button("単語帳を再読み込み", use_container_width=True):
            st.session_state.clear()
            fetch_word_list.clear()
            st.rerun()


if __name__ == "__main__":
    main()
