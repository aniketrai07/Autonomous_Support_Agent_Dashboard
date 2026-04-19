import google.generativeai as genai

# 🔥 PASTE YOUR NEW KEY HERE
genai.configure(api_key="AIzaSyDFqNbNTCpLMuusOptt4q3bqw58n7UVUG0")

model = genai.GenerativeModel("gemini-1.5-flash")


def call_llm(prompt):
    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            print("⚠️ Empty Gemini response")
            return "{}"

        return response.text.strip()

    except Exception as e:
        print("❌ Gemini Error:", e)
        return "{}"