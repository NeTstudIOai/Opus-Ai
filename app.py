from flask import Flask, render_template, request, jsonify
from ddgs import DDGS
import os

app = Flask(__name__)

def search_internet(query, max_results=5):
    results_data = []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        for r in results:
            results_data.append({
                "title": r.get("title"),
                "link": r.get("href"),
                "snippet": r.get("body")
            })
    return results_data


# === HTML page route (your original) ===
@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query")
        results = search_internet(query)

    return render_template("index.html", results=results, query=query)


# === NEW: API route for JS fetch() ===
@app.route("/search", methods=["POST"])
def search_api():
    data = request.get_json()
    query = data.get("query", "")
    results = search_internet(query)
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
