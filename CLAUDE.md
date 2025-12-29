# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ChiLingo is a Chinese language learning flashcard application built with Streamlit. The app helps users study Chinese vocabulary by:
- Fetching a word list from Dropbox
- Randomizing word order using session state
- Displaying either Chinese text or playing audio (randomly chosen)
- Revealing pinyin, pronunciation (mp3), and Japanese translation on button press

## Commands

### Run the application
```bash
streamlit run main.py
```

### Install dependencies
```bash
uv sync
```

## Architecture

### Data Source
Word list is fetched from a public Dropbox link:
```bash
curl -L 'https://www.dropbox.com/scl/fi/b1bxhq60uomcnt4s9e0u5/chilingo.toml?rlkey=8nc6em3grkv34p1hlgzuzwuuj&st=6bb6bvf3&dl=0'
```

### Data Model
Words are stored in TOML format:
```toml
[[items]]
zh = "你好"
pinyin = "nǐ hǎo"
ja = "こんにちは"
```

### Audio Generation
- Uses gTTS to generate Chinese pronunciation (zh-cn)
- Audio files are cached to `/tmp/chilingo/*.mp3` to avoid regeneration
- Files persist across sessions for performance

### State Management
- `streamlit.cache_data` for word list fetching from Dropbox
- `streamlit.session_state` for managing randomized word order and current position

### Quiz Flow
1. Load and cache word list from Dropbox
2. Randomize order in session state
3. For each word, randomly choose one of two presentation modes:
   - Show Chinese text → reveal pinyin, audio, and Japanese translation
   - Play audio (mp3) → reveal Chinese text, pinyin, and Japanese translation

## Implementation Notes

- Check `/tmp/chilingo/` for existing audio files before generating new ones
- Audio caching is critical for performance - always verify file existence first
