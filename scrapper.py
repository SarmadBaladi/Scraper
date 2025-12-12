import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Read API key from environment variable
API_KEY = os.getenv("API_KEY")

# Model name
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=API_KEY)

def get_article_data(url):
    """Scrape text and main image from the article URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get image
        image_url = "No image found"
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image_url = og_image["content"]
        else:
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                image_url = img_tag["src"]

        # Get text
        text_content = " ".join([p.get_text() for p in soup.find_all('p')])
        return text_content[:15000], image_url

    except Exception as e:
        print("Scraping Error:", e)
        return None, None

def generate_seo_content(text_content):
    if not text_content:
        return None
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
Analyze the following article text and provide an SEO response:

1. Summary: 25-30 words
2. Hashtags: 4-5 relevant hashtags

Article:
{text_content}

Return format:
Summary: [Your summary here]
Hashtags: [Your hashtags here]
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"