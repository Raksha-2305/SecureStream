import google.generativeai as genai

# 🔥 PASTE YOUR OWN API KEY HERE
genai.configure(api_key="AIzaSyC0-3ivSZ0ZxTanNvks5bQfFTztmBxgECI")

def get_hashtags(keyword):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"Give 5 short hashtags for {keyword}"
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "#football #goal #sports #soccer #highlights"