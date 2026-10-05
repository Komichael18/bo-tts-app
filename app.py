import streamlit as st
from gtts import gTTS
import os

# Page Configuration
st.set_page_config(page_title="Bo_TTS", layout="centered")

st.title("🔊 Bo_TTS (မြန်မာစာမှ အသံထွက်သို့)")
st.write("မြန်မာစာသားများကို ထည့်သွင်းပြီး အသံဖိုင်အဖြစ် ပြောင်းလဲနိုင်ပါပြီ။")

# Text Input Area
text_input = st.text_area("ဖတ်စေချင်တဲ့ စာကို ဒီမှာ ထည့်ပါ -", height=150)

# Voice Selection
voice_option = st.selectbox("ပိုင်နာမည် (အသံပုံစံ ရွေးချယ်ရန်)", ["သီလာ (အမျိုးသမီး)", "သီဟ (အမျိုးသား)"])

# Speed Selection (အသံအမြန်နှုန်း ချိန်ညှိရန်)
speed_option = st.radio("အသံအမြန်နှုန်း ရွေးချယ်ရန်:", ["ပုံမှန် (Normal)", "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)"])

# Generate Button
if st.button("Generate"):
    if text_input.strip() == "":
        st.warning("ကျေးဇူးပြု၍ စာသားအနည်းဆုံး တစ်ခုခု ထည့်ပါ။")
    else:
        with st.spinner("အသံဖိုင် ထုတ်လုပ်နေပါပြီ ခဏစောင့်ပါ..."):
            try:
                # Speed ကို အခြေခံ၍ slow parameter ကို True သို့မဟုတ် False သတ်မှတ်ခြင်း
                is_slow = True if speed_option == "နှေး (Slow - ပိုမိုရှင်းလင်းရန်)" else False
                
                # gTTS ကို အသုံးပြု၍ မြန်မာစာကို အသံဖိုင်သို့ ပြောင်းခြင်း
                tts = gTTS(text=text_input, lang='my', slow=is_slow)
                audio_file = "output.mp3"
                tts.save(audio_file)
                
                st.success("အသံဖိုင် အောင်မြင်စွာ ထွက်လာပါပြီ!")
                
                # Streamlit Audio Player
                st.audio(audio_file, format='audio/mp3')
                
            except Exception as e:
                st.error(f"မှားယွင်းမှု တစ်စုံတစ်ရာ ရှိနေပါသည်: {e}")