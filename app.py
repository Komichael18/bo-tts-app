import streamlit as st
from gtts import gTTS
import pyttsx3
import os

# Page Configuration
st.set_page_config(page_title="Bo_TTS", layout="centered")

st.title("🔊 Bo_TTS (မြန်မာစာမှ အသံထွက်သို့)")
st.write("မြန်မာစာသားများကို ထည့်သွင်းပြီး အသံဖိုင်အဖြစ် ပြောင်းလဲနိုင်ပါပြီ။")

# Text Input Area
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ထည့်ပါ -", height=150)

# TTS Engine Selection (TTS မော်ဒယ် ရွေးချယ်ရန်)
engine_option = st.selectbox(
    "TTS မော်ဒယ် / အင်ဂျင် ရွေးချယ်ရန်", 
    ["gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)", "Offline System Engine (pyttsx3)"]
)

# Conditional Settings based on Engine
if engine_option == "gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)":
    speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])
else:
    voice_gender = st.selectbox("အသံပုံစံ ရွေးချယ်ရန်:", ["အမျိုးသမီးသံ", "အမျိုးသားသံ"])

# Generate Button
if st.button("Generate"):
    if text_input.strip() == "":
        st.warning("ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်ပါ။")
    else:
        with st.spinner("အသံဖိုင် ထုတ်လုပ်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                audio_file = "output.mp3"
                
                if "gTTS" in engine_option:
                    # gTTS Processing
                    is_slow = True if speed_option == "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)" else False
                    tts = gTTS(text=text_input, lang='my', slow=is_slow)
                    tts.save(audio_file)
                    
                else:
                    # pyttsx3 Processing (Offline)
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    
                    # Set voice type if available
                    if voices:
                        if "အမျိုးသမီး" in voice_gender and len(voices) > 1:
                            engine.setProperty('voice', voices[1].id)
                        else:
                            engine.setProperty('voice', voices[0].id)
                            
                    # Save to file (pyttsx3 typically saves as wav, converted or saved directly)
                    audio_file = "output.wav"
                    engine.save_to_file(text_input, audio_file)
                    engine.runAndWait()
                
                st.success("အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                
                # Streamlit Audio Player
                st.audio(audio_file)
                
            except Exception as e:
                st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")