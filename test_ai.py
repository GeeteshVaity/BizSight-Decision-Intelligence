from groq import Groq
import streamlit as st

def main():
    print("🔍 Testing Groq API...")

    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            print("❌ GROQ_API_KEY not found in Streamlit secrets")
            return

        print("✅ API key found")

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly this sentence: Groq AI is working perfectly."
                }
            ],
            temperature=0,
        )

        print("✅ AI RESPONSE RECEIVED:")
        print(response.choices[0].message.content)

    except Exception as e:
        print("❌ ERROR OCCURRED")
        print(e)

if __name__ == "__main__":
    main()
