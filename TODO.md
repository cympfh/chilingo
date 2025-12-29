# Chilingo - Chinese Linguistics Tools

## 単語帳

```bash
curl -L 'https://www.dropbox.com/scl/fi/b1bxhq60uomcnt4s9e0u5/chilingo.toml?rlkey=8nc6em3grkv34p1hlgzuzwuuj&st=6bb6bvf3&dl=0'
```

This is public link. You can try `curl` it.

## 概要

Streamlit で実現する中国語学習のための単語帳

1. 単語帳をDropboxから取得
    - streamlit.cache_data
2. ランダムに並び変える
    - streamlit.session_state
3. 順に表示していくが、次の２通りのどちらかランダム
    - 中国語を表示
        - ボタンを押すと拼音，発声(mp3), 日本語訳を表示
    - 発声 (mp3) を再生
        - ボタンを押すと中国語，拼音，日本語訳を表示

単語帳は

```toml
[[items]]
zh = "你好"
pinyin = "nǐ hǎo"
ja = "こんにちは"
```

だけ。
mp3 は gTTS で生成する。

```python
from gtts import gTTS

text = "你好，世界"  # 中国語テキスト、またはピンイン "Ni hao, shi jie"
lang = 'zh-cn'

tts = gTTS(text, lang=lang)
tts.save("output.mp3")
```

これは一度生成したらディスク (/tmp/chilingo/*.mp3) に保存しておき、次回からは再生成しないようにする。
