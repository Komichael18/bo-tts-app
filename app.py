import streamlit as st
from gtts import gTTS
import os
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="Bo_TTS", layout="centered")

st.title("🔊 Bo_TTS (မြန်မာစာမှ အသံထွက်သို့)")
st.write("gTTS နှင့် Google AI Studio (Gemini TTS) တို့ကို အသုံးပြု၍ အသံဖိုင်များ ထုတ်လုပ်နိုင်ပါပြီ။")

# API Key Input for Google AI Studio
api_key_input = st.text_input("Google AI Studio API Key ထည့်ရန် (Gemini TTS အတွက်):", type="password")

# Text Input Area
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ထည့်ပါ -", height=150)

# TTS Engine Selection
engine_option = st.selectbox(
    "TTS မော်ဒယ် / အင်ဂျင် ရွေးချယ်ရန်", 
    ["gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)", "Google AI Studio (Gemini TTS)"]
)

# Conditional Settings based on Engine
if engine_option == "gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)":
    speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])
else:
    # Google AI Studio Voice options
    voice_option = st.selectbox("Google AI Studio Voice ရွေးချယ်ရန်:", ["Kore", "Zephyr", "Puck", "Charon", "Fenrir"])

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
                    
                    st.success("gTTS ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                    st.audio(audio_file, format='audio/mp3')
                    
                else:
                    # Google AI Studio Gemini TTS Processing
                    if not api_key_input.strip():
                        st.error("ကျေးဇူးပြု၍ Google AI Studio API Key ထည့်သွင်းပေးပါ။")
                    else:
                        # Initialize GenAI Client
                        client = genai.Client(api_key=api_key_input)
                        
                        # Request audio generation using Gemini model with speech config
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Please read the following text accurately: {text_input}",
                            config=types.GenerateContentConfig(
                                response_mime_type="audio/mp3",
                                speech_config=types.SpeechConfig(
                                    voice_config=types.VoiceConfig(
                                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                            voice_name=voice_option
                                        )
                                    )
                                )
                            )
                        )
                        
                        # Extract audio data from candidates
                        audio_bytes = None
                        if response.candidates:
                            for candidate in response.candidates:
                                if candidate.content and candidate.content.parts:
                                    for part in candidate.content.parts:
                                        if part.inline_data and part.inline_data.data:
                                            audio_bytes = part.inline_data.data
                                            break
                                if audio_bytes:
                                    break
                        
                        if audio_bytes:
                            with open(audio_file, "wb") as f:
                                f.write(audio_bytes)
                                
                            st.success("Google AI Studio (Gemini TTS) ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                            st.audio(audio_file, format='audio/mp3')
                        else:
                            st.error("အသံဖိုင် အထွက်မလာပါ။ ကျေးဇူးပြု၍ API Key သို့မဟုတ် စာသားကို စစ်ဆေးပါ။")
                            
            except Exception as e:
                st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")