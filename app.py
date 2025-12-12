from flask import Flask, request, jsonify
from scraper import get_article_data, generate_seo_content

app = Flask(__name__)

@app.route("/", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error":"URL missing"}), 400

    text, image = get_article_data(url)
    if not text:
        return jsonify({"error":"Failed to fetch article"}), 500

    seo_result = generate_seo_content(text)

    # Split summary and hashtags
    summary, hashtags = "", ""
    for line in seo_result.split("\n"):
        if line.lower().startswith("summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.lower().startswith("hashtags:"):
            hashtags = line.replace("Hashtags:", "").strip()

    return jsonify({"summary": summary, "hashtags": hashtags, "image": image})

if __name__ == "__main__":
    # Use port 10000 (Render will assign its own port via env var)
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)