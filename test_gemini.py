'''import os
from dotenv import load_dotenv
from google import genai


def main():
    print("📋 Listing all Gemini models visible to this project\n")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return

    client = genai.Client(api_key=api_key)

    try:
        models = list(client.models.list())
    except Exception as e:
        print("❌ Failed to list models")
        print(e)
        return

    print(f"✅ Total models visible: {len(models)}\n")

    for i, model in enumerate(models, start=1):
        print(f"{i:02d}. {model.name}")


if __name__ == "__main__":
    main()'''


import os
from dotenv import load_dotenv
from google import genai


def main():
    print("🔍 Testing Gemini model: gemini-flash-lite-latest\n")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return

    print("✅ API key loaded")

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print("❌ Failed to create Gemini client")
        print(e)
        return

    MODEL_NAME = "models/gemini-flash-lite-latest"
    prompt = "Reply with exactly this text: Gemini Flash Lite is working."

    try:
        print(f"📡 Sending request to {MODEL_NAME} ...")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        print("\n🎉 SUCCESS!")
        print("Model response:")
        print("----------------")
        print(response.text.strip())
        print("----------------")

    except Exception as e:
        print("\n❌ FAILED")
        print("Error details:")
        print(str(e))


if __name__ == "__main__":
    main()
