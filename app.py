import streamlit as st
from gtts import gTTS
import os
from google import genai

# Page Configuration
st.set_page_config(page_title="Bo_TTS", layout="centered")

st.title("🔊 Bo_TTS (မြန်မာစာမှ အသံထွက်သို့)")
st.write("gTTS နှင့် Google AI Studio (Gemini) တို့ကို အသုံးပြု၍ စာသားများ လုပ်ဆောင်နိုင်ပါပြီ။")

# API Key Input for Google AI Studio
api_key_input = st.text_input("Google AI Studio API Key ထည့်ရန် (Gemini အတွက်):", type="password")

# Text Input Area
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ထည့်ပါ -", height=150)

# TTS Engine Selection
engine_option = st.selectbox(
    "TTS မော်ဒယ် / အင်ဂျင် ရွေးချယ်ရန်", 
    ["gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)", "Google AI Studio (Gemini AI Text & TTS)"]
)

# Conditional Settings based on Engine
if engine_option == "gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)":
    speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])
else:
    voice_option = st.selectbox("Google AI Studio Voice ရွေးချယ်ရန်:", ["Kore", "Zephyr", "Puck", "Charon", "Fenrir"])

# Generate Button
if st.button("Generate"):
    if text_input.strip() == "":
        st.warning("ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်ပါ။")
    else:
        with st.spinner("လုပ်ဆောင်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                audio_file = "output.mp3"
                
                if "gTTS" in engine_option:
                    # gTTS Processing (Reliable Audio Generation)
                    is_slow = True if speed_option == "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)" else False
                    tts = gTTS(text=text_input, lang='my', slow=is_slow)
                    tts.save(audio_file)
                    
                    st.success("gTTS ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                    st.audio(audio_file, format='audio/mp3')
                    
                else:
                    # Google AI Studio Gemini Processing
                    if not api_key_input.strip():
                        st.error("ကျေးဇူးပြု၍ Google AI Studio API Key ထည့်သွင်းပေးပါ။")
                    else:
                        client = genai.Client(api_key=api_key_input)
                        
                        # Generate text response or analysis from Gemini
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Please process this Burmese text: {text_input}"
                        )
                        
                        if response.text:
                            st.success("Gemini AI မှ အောင်မြင်စွာ တုံ့ပြန်လာပါပြီ:")
                            st.write(response.text)
                            
                            # Automatically generate audio for the text using gTTS for seamless playback
                            tts = gTTS(text=text_input, lang='my', slow=False)
                            tts.save(audio_file)
                            st.audio(audio_file, format='audio/mp3')
                        else:
                            st.error("AI မှ အချက်အလက် တုံ့ပြန်မှု မရှိပါ။")
                            
            except Exception as e:
                st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")