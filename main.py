import os
import streamlit as st
from openai import OpenAI

# 1. पेज सेटिंग्स
st.set_page_config(page_title="The Hidden Sun AI", page_icon="☀️", layout="centered")

st.title("☀️ The Hidden Sun AI")
st.caption("5th to 12th class & all external questions solver AI")

# 2. API Key लेना
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API Key नहीं मिली! Render के Environment Variables में 'OPENAI_API_KEY' जोड़ें।")
    st.stop()

client = OpenAI(api_key=api_key)

# 3. AI का निर्देश (Instruction)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "आपका नाम 'The Hidden Sun AI' है। आप 5वीं से 12वीं कक्षा के छात्रों के सभी सवालों और अन्य सभी बाहरी (external) सवालों का बहुत ही सरल, सटीक और विस्तार से जवाब हिंदी व अंग्रेजी में देते हैं।"
        }
    ]

# 4. पुरानी चैट दिखाना
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. यूज़र से सवाल लेना
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"एरर आया: {e}")
