import streamlit as st
from gtts import gTTS
import base64
import os
from google import genai

# Page Configuration
st.set_page_config(page_title="Bo_TTS", layout="centered")

st.title("🔊 Bo_TTS (မြန်မာစာမှ အသံထွက်သို့)")
st.write("gTTS နှင့် Google AI Studio (Gemini TTS) တို့ကို အသုံးပြု၍ အသံဖိုင်များ ထုတ်လုပ်နိုင်ပါပြီ။")

# API Key Input for Google AI Studio
api_key_input = st.text_input("Google AI Studio API Key ထည့်ရန် (Gemini TTS အတွက် - Optional):", type="password")

# Text Input Area
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ထည့်ပါ -", height=150)

# TTS Engine Selection
engine_option = st.selectbox(
    "TTS မော်ဒယ် / အင်ဂျင် ရွေးချယ်ရန်", 
    ["gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)", "Google AI Studio (Gemini 3.8 Flash TTS)"]
)

# Conditional Settings based on Engine
if engine_option == "gTTS (Google - ပုံမှန်/နှေး ချိန်ညှိရန်)":
    speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])
else:
    # Google AI Studio Voice options
    voice_option = st.selectbox("Google AI Studio Voice ရွေးချယ်ရန်:", ["Kore", "Zephyr"])
    style_instruction = st.text_input("အသံထွက် ပုံစံညွှန်ကြားချက် (Style / Tone - ဥပမာ: cheerful and friendly)", "clear and natural")

# Generate Button
if st.button("Generate"):
    if text_input.strip() == "":
        st.warning("ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်ပါ။")
    else:
        with st.spinner("အသံဖိုင် ထုတ်လုပ်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                audio_file = "output.wav"
                
                if "gTTS" in engine_option:
                    audio_file = "output.mp3"
                    is_slow = True if speed_option == "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)" else False
                    tts = gTTS(text=text_input, lang='my', slow=is_slow)
                    tts.save(audio_file)
                    st.success("gTTS ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                    st.audio(audio_file, format='audio/mp3')
                    
                else:
                    if not api_key_input.strip():
                        st.error("ကျေးဇူးပြု၍ Google AI Studio API Key ထည့်သွင်းပေးပါ။")
                    else:
                        # Initialize Google GenAI Client with user API Key
                        client = genai.Client(api_key=api_key_input)
                        
                        # Call Gemini TTS Model
                        interaction = client.models.create(
                            model="gemini-3.8-flash-tts",
                            input=[{
                                "type": "user_input", 
                                "content": [{
                                    "type": "text", 
                                    "text": text_input, 
                                    "annotations": [{
                                        "type": "speech_metadata", 
                                        "style": style_instruction,
                                    }]
                                }]
                            }],
                            response_format={"type": "audio"},
                            generation_config={
                                "speech_config": [
                                    {"voice": voice_option},
                                ]
                            },
                        )
                        
                        # Save output audio data
                        if interaction.output_audio and interaction.output_audio.data:
                            audio_bytes = base64.b64decode(interaction.output_audio.data)
                            with open(audio_file, "wb") as f:
                                f.write(audio_bytes)
                                
                            st.success("Google AI Studio (Gemini TTS) ဖြင့် အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                            st.audio(audio_file, format='audio/wav')
                        else:
                            st.error("အသံဖိုင် ထုတ်ယူရာတွင် အမှားအယွင်း ရှိသွားပါသည်။")
                            
            except Exception as e:
                st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")