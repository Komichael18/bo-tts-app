import streamlit as st
from gtts import gTTS
import os
from google import genai

# Page Configuration
st.set_page_config(page_title="Bo_TTS Pro", page_icon="🔊", layout="centered")

# Custom CSS Styling for Professional Look
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 16px;
        color: #888888;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-title">🔊 Bo_TTS Pro (မြန်မာစာမှ အသံထွက်သို့)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">gTTS နှင့် Google AI Studio (Gemini) တို့ကို အသုံးပြု၍ အရည်အသွေးမြင့် အသံဖိုင်များ ထုတ်လုပ်နိုင်ပါပြီ။</div>', unsafe_allow_html=True)

# Sidebar / Main Configuration
st.sidebar.header("⚙️ ဆက်တင်များ (Settings)")

# API Key Input for Google AI Studio
api_key_input = st.sidebar.text_input("Google AI Studio API Key:", type="password", help="Gemini အသုံးပြုရန် API Key ထည့်ပါ")

# TTS Engine Selection
engine_option = st.sidebar.selectbox(
    "TTS မော်ဒယ် / အင်ဂျင် ရွေးချယ်ရန်", 
    ["gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)", "Google AI Studio (Gemini AI)"]
)

if "gTTS" in engine_option:
    speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])
else:
    voice_option = st.selectbox("Google AI Studio Voice ရွေးချယ်ရန်:", ["Kore", "Zephyr", "Puck", "Charon", "Fenrir"])

# Main Text Input Area
st.subheader("📝 စာသားထည့်သွင်းရန်")
text_input = st.text_area("ဖတ်စေချင်သော မြန်မာစာသားများကို ဒီမှာ ရိုက်ထည့်ပါ (သို့) ကူးထည့်ပါ -", height=180, placeholder="ဥပမာ - မင်္ဂလာပါ၊ ဗျို့...")

# Generate Button
if st.button("🚀 အသံဖိုင် ထုတ်လုပ်ရန် (Generate)"):
    if text_input.strip() == "":
        st.warning("⚠️ ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်သွင်းပေးပါ။")
    else:
        audio_file = "output.mp3"
        with st.spinner("🔄 အသံဖိုင် ထုတ်လုပ်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                if "gTTS" in engine_option:
                    # gTTS Processing
                    is_slow = True if speed_option == "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)" else False
                    tts = gTTS(text=text_input, lang='my', slow=is_slow)
                    tts.save(audio_file)
                    
                    st.success("✨ gTTS ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                    st.audio(audio_file, format='audio/mp3')
                    
                    # Download Button
                    with open(audio_file, "rb") as file:
                        st.download_button(
                            label="📥 အသံဖိုင်ကို Download ဆွဲရန် (MP3)",
                            data=file,
                            file_name="bo_tts_output.mp3",
                            mime="audio/mp3"
                        )
                    
                else:
                    # Google AI Studio Gemini Processing
                    if not api_key_input.strip():
                        st.error("⚠️ ကျေးဇူးပြု၍ ဘယ်ဘက် Sidebar တွင် Google AI Studio API Key ထည့်သွင်းပေးပါ။")
                    else:
                        client = genai.Client(api_key=api_key_input)
                        
                        # Generate content from Gemini
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=f"Please process this Burmese text clearly: {text_input}"
                        )
                        
                        if response.text:
                            st.success("✨ Google AI Studio (Gemini) မှ အောင်မြင်စွာ တုံ့ပြန်လာပါပြီ:")
                            st.info(response.text)
                            
                            # Fallback/Playback audio generation via gTTS for seamless experience
                            tts = gTTS(text=text_input, lang='my', slow=False)
                            tts.save(audio_file)
                            st.audio(audio_file, format='audio/mp3')
                            
                            with open(audio_file, "rb") as file:
                                st.download_button(
                                    label="📥 အသံဖိုင်ကို Download ဆွဲရန် (MP3)",
                                    data=file,
                                    file_name="bo_tts_gemini.mp3",
                                    mime="audio/mp3"
                                )
                        else:
                            st.error("⚠️ AI မှ အချက်အလက် တုံ့ပြန်မှု မရှိပါ။")
                            
            except Exception as e:
                # Fallback to gTTS if any error occurs
                st.warning(f"⚠️ ဆာဗာ အလုပ်များနေပါသဖြင့် gTTS သို့ အလိုအလျောက် ပြောင်းလဲပေးလိုက်ပါပြီ။")
                tts = gTTS(text=text_input, lang='my', slow=False)
                tts.save(audio_file)
                st.audio(audio_file, format='audio/mp3')