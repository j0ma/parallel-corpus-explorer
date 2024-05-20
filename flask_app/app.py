import os
import itertools as it
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Foo
# Set up global things
source_file = os.environ.get("SOURCE_SENTENCES_FILE", "source.txt")
source_language = os.environ.get("SOURCE_LANGUAGE", "Finnish")
target_file = os.environ.get("TARGET_SENTENCES_FILE", "target.txt")
target_language = os.environ.get("TARGET_LANGUAGE", "English")

with open(source_file, "r", encoding="utf-8") as source_file:
    source_sentences = source_file.read().split("\n")
with open(target_file, "r", encoding="utf-8") as target_file:
    target_sentences = target_file.read().split("\n")

assert len(source_sentences) == len(
    target_sentences
), "Source and target files must have the same number of lines"

current_index = random.randint(0, len(source_sentences) - 1)

# Set up route to applicatoin
@app.route("/")
def index():
    global current_index
    source_sentence = source_sentences[current_index]
    target_sentence = target_sentences[current_index]

    template_name = os.environ.get("TEMPLATE_NAME", "index.html")

    return render_template(
        template_name,
        source_sentence=source_sentence,
        target_sentence=target_sentence,
        source_language=source_language,
        target_language=target_language,
    )


@app.route("/next", endpoint="next")
def next_page():
    global current_index
    current_index = (current_index + 1) % len(source_sentences)
    return index()


@app.route("/previous", endpoint="previous")
def previous_page():
    global current_index
    current_index = current_index - 1
    if current_index < 0:
        current_index = len(source_sentences) - 1

    return index()

@app.route("/random", endpoint="random")
def random_page():
    global current_index
    current_index = random.randint(0, len(source_sentences) - 1)

    return index()

# Create a route to go to a specific page
# NOTE: this will be triggered by the form
@app.route("/page", methods=["POST"], endpoint="page_post")
def specific_page_post():
    global current_index
    current_index = int(request.form["page_number"]) - 1
    return index()


@app.route("/page/<int:page>", endpoint="page")
def specific_page(page):
    global current_index
    current_index = page - 1
    return index()

if __name__ == "__main__":
    app.run(debug=True)
