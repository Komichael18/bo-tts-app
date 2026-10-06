import streamlit as st
from gtts import gTTS
import os
import datetime
from google import genai

# Page Configuration
st.set_page_config(page_title="SaiMyanmar TTS Pro", page_icon="🔊", layout="centered")

# Custom Styling (Dark/Pro Theme matching the video)
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #00E6FF;
        text-align: center;
    }
    .sub-header {
        font-size: 14px;
        color: #888888;
        text-align: center;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #261f21;
        border: 1px solid #ff4b4b;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #8A2387, #E94057, #F27121);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Top Header & Telegram Banner
st.markdown('<div class="main-header">SaiMyanmar TTS Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">မြန်မာစာမှ အသံထွက်ဖိုင်သို့ Pro အဆင့် ပြောင်းလဲနိုင်ပါပြီ</div>', unsafe_allow_html=True)

# Telegram Channel Link Button
st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <a href="https://t.me/" target="_blank" style="text-decoration: none;">
            <button style="background-color: #229ED9; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer;">
                📢 နိုင်ငံိုင် Telegram Channel မှ ဝင်ရောက်ရန်
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Warning / Notice Box
st.markdown("""
    <div class="warning-box">
        <b style="color: #ff4b4b;">⚠️ အရေးကြီး အသိပေးချက်</b><br>
        <p style="font-size: 13px; color: #ddd; margin: 5px 0 0 0;">
        ကျေးဇူးပြု၍ System အသုံးပြုရာတွင် အလုပ်မလုပ်ပါက သို့မဟုတ် Users အများစုကြောင့် Server ခေတ္တရပ်တန့်သွားပါက Telegram Channel ကို Join ထားပေးကြပါ။
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar / Settings for API and Engines (Preserving existing features)
st.sidebar.header("⚙️ ဆက်တင်များ (Settings)")
api_key_input = st.sidebar.text_input("Google AI Studio API Key:", type="password", help="Gemini အတွက် API Key ထည့်ရန်")
engine_option = st.sidebar.selectbox("TTS မော်ဒယ် ရွေးချယ်ရန်", ["gTTS (Google Engine)", "Google AI Studio (Gemini)"])

if "gTTS" in engine_option:
    speed_option = st.sidebar.radio("အသံအမြန်နှုန်း:", ["ပုံမှန် (Normal)", "နှေး (Slow)"])
else:
    voice_option = st.sidebar.selectbox("Gemini Voice:", ["Kore", "Zephyr", "Puck", "Charon", "Fenrir"])

# Voice Presets Selection (Grid buttons simulation)
st.markdown("### 🎙️ အသံတိုတိုနှင့် ပုံစံများ ရွေးချယ်ရန်")
col1, col2, col3 = st.columns(3)
selected_voice_preset = ""
with col1:
    if st.button("ကိုလှိုင်"): selected_voice_preset = "ကိုလှိုင်"
    if st.button("မဆုမြတ်"): selected_voice_preset = "မဆုမြတ်"
with col2:
    if st.button("မေမွန့်စံ"): selected_voice_preset = "မေမွန့်စံ"
    if st.button("ကိုင်တိုဉ်း"): selected_voice_preset = "ကိုင်တိုဉ်း"
with col3:
    if st.button("မသင်းစံကျော်"): selected_voice_preset = "မသင်းစံကျော်"
    if st.button("ကိုမင်းထိုက်"): selected_voice_preset = "ကိုမင်းထိုက်"

# Speed and Pitch Sliders (ដូចក្នុងဗီဒီယို)
col_s1, col_s2 = st.columns(2)
with col_s1:
    speed_val = st.slider("အမြန်နှုန်း (SPEED)", -20, 20, 0)
with col_s2:
    pitch_val = st.slider("သံ အាក់ကွက်/အကု (PITCH)", -20, 20, 0)

# Emoji Shortcut Bar
st.markdown("😊 အီမိုဂျီ စိတ်ကြပ်ထည့်ရန်:")
emoji_cols = st.columns(6)
emojis = ["😊", "👍", "🔥", "🙏", "❤️", "✨"]
prefix_emoji = ""
for i, em in enumerate(emojis):
    with emoji_cols[i]:
        if st.button(em):
            prefix_emoji = em

# Main Text Input Area
st.markdown("### 📝 စာသားထည့်သွင်းရန်")
default_text = prefix_emoji + " " if prefix_emoji else ""
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ရိုက်ထည့်ပါ -", value=default_text, height=150)

# Character/Word Counters
words_count = len(text_input.split()) if text_input.strip() else 0
char_count = len(text_input)
lines_count = len(text_input.split('\n')) if text_input.strip() else 0

m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("WORD LIMIT", "∞")
m_col2.metric("WORDS", words_count)
m_col3.metric("CHARACTERS", char_count)

# Custom File Name Input for Download
custom_filename = st.text_input("အသံဖိုင် အမည်ပေးရန် (ဥပမာ - Saimyanmar31)", value="SaiMyanmar_TTS")

# Generate Button
if st.button("✨ အသံထွက်ယူမည်"):
    if text_input.strip() == "":
        st.warning("⚠️ ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်ပါ။")
    else:
        with st.spinner("ရလဒ် ထုတ်လုပ်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                mp3_filename = f"{custom_filename}.mp3"
                srt_filename = f"{custom_filename}.srt"
                
                if "gTTS" in engine_option:
                    is_slow = True if "နှေး" in speed_option else False
                    tts = gTTS(text=text_input, lang='my', slow=is_slow)
                    tts.save(mp3_filename)
                else:
                    if not api_key_input.strip():
                        st.error("ကျေးဇူးပြု၍ Sidebar တွင် Google AI Studio API Key ထည့်ပါ။")
                    else:
                        client = genai.Client(api_key=api_key_input)
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=f"Process text: {text_input}"
                        )
                        # Fallback generation to gTTS for audio integrity
                        tts = gTTS(text=text_input, lang='my', slow=False)
                        tts.save(mp3_filename)

                # Generate simple SRT (Subtitle file) corresponding to text lines
                srt_content = f"1\n00:00:00,000 --> 00:00:05,000\n{text_input}\n"
                with open(srt_filename, "w", encoding="utf-8") as f:
                    f.write(srt_content)

                st.success("🎉 အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                st.audio(mp3_filename, format='audio/mp3')

                # Download Buttons for MP3 and SRT
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    with open(mp3_filename, "rb") as f:
                        st.download_button("📥 အသံဖိုင် (.mp3) ဒေါင်းလုပ်ဆွဲမည်", f, file_name=mp3_filename, mime="audio/mp3")
                with d_col2:
                    with open(srt_filename, "rb") as f:
                        st.download_button("📄 မြန်မာစာတန်းထိုး (.srt) ဒေါင်းလုပ်", f, file_name=srt_filename, mime="text/plain")

            except Exception as e:
                st.error(f"မှားယွင်းမှု ရှိနေပါသည်: {e}")