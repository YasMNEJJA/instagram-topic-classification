# app.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model.models import DummyModel, TransformerModel

app = FastAPI()

# Mount static files (e.g., CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """
    Render the input form.
    """
    return templates.TemplateResponse("form.html", {"request": request, "topic_result": None})

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, text: str = Form(...)):
    """
    Handle form submission and return classification results.
    """

    # Path to the file containing the topics
    file_path = "./data/instagram_magazine_topics.txt"

    # Open the file and read the lines into a list
    with open(file_path, "r") as file:
        topics = [line.strip() for line in file]

    model = TransformerModel(topics)

    topic_result = model.predict(text)

    topics_with_scores = list(zip(topic_result["labels"], topic_result["scores"]))

    # Sort topics by scores in descending order
    topics_with_scores_sorted = sorted(topics_with_scores, key=lambda x: x[1], reverse=True)

    # Extract the top 5 topics
    top_5_topics = topics_with_scores_sorted[:5]

    # Identify the topic with the highest probability
    highest_topic, highest_topic_probability = topics_with_scores_sorted[0]
    # Identify the topic with the highest probability

    sentiment_result = model.analyze_sentiment(text)
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "top_5_topics": top_5_topics,
        "all_labels": topic_result["labels"],  # All available labels
        "sentiment_result": sentiment_result, 
        "highest_topic": highest_topic, 
        "highest_topic_probability": highest_topic_probability, 
        "input_text": text})
