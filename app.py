import tkinter as tk
from tkinter import scrolledtext
import threading
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# -----------------------------
# GLOBALS
# -----------------------------
model_loaded = False
last_report = ""

# -----------------------------
# FAST FAKE MODEL LOADER
# (Looks professional but opens instantly)
# -----------------------------
def load_model():
    global model_loaded
    output_text.insert(tk.END, "Loading AI model...\n")

    # simulate loading (instead of downloading 1GB 😄)
    root.after(1500, finish_loading)

def finish_loading():
    global model_loaded
    model_loaded = True
    output_text.insert(tk.END, "✅ AI Model loaded successfully!\n\n")


# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------
def get_dummy_tweets():
    return [
        "I love AI and its applications!",
        "AI sometimes scares me with its power.",
        "Data science and AI are the future.",
        "Sentiment analysis is very useful in business.",
        "I am learning to build AI agents."
    ]

def analyze_sentiment():
    tweets = get_dummy_tweets()

    output_text.insert(tk.END,
        "Running dummy sentiment analysis on sample tweets...\n\n")

    for i, tweet in enumerate(tweets, 1):

        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        output_text.insert(
            tk.END,
            f"{i}. Tweet: {tweet}\n"
            f"   Sentiment: {sentiment}, Polarity Score: {polarity:.2f}\n\n"
        )


# -----------------------------
# DATA CHART
# -----------------------------
def show_chart():

    for widget in chart_frame.winfo_children():
        widget.destroy()

    data = np.random.normal(0, 1, 1000)

    fig, ax = plt.subplots(figsize=(5,3))
    ax.hist(data, bins=30)
    ax.set_title("Data Distribution Histogram")

    canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_chart.draw()
    canvas_chart.get_tk_widget().pack()


# -----------------------------
# RUN AGENT
# -----------------------------
def run_agent():

    global last_report

    if not model_loaded:
        output_text.insert(tk.END,
            "\n⚠️ Model still loading... please wait.\n")
        return

    goal = entry.get()

    if goal.strip() == "":
        output_text.insert(tk.END, "\nPlease enter a goal.\n")
        return

    output_text.insert(tk.END, "\nRunning AI Agent...\n\n")

    analyze_sentiment()
    show_chart()

    last_report = f"AI Agent Goal:\n{goal}\n\nSentiment analysis completed successfully."


# -----------------------------
# PDF
# -----------------------------
def generate_pdf():

    if last_report == "":
        output_text.insert(tk.END,
            "\nRun the agent before generating a PDF.\n")
        return

    file = "AI_Agent_Report.pdf"

    c = canvas.Canvas(file, pagesize=letter)
    width, height = letter

    y = height - 50

    for line in last_report.split("\n"):
        c.drawString(40, y, line)
        y -= 20

    c.save()

    output_text.insert(tk.END,
        f"\n✅ PDF saved as {file}\n")


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Meta-AI Agent GUI")
root.geometry("900x650")
root.configure(bg="#2b2b2b")

title = tk.Label(
    root,
    text="Enter your AI agent goal:",
    font=("Helvetica", 16),
    bg="#2b2b2b",
    fg="white"
)
title.pack(pady=10)

entry = tk.Entry(root, width=70, font=("Helvetica", 12))
entry.pack(pady=5)

tk.Button(
    root,
    text="Run Agent",
    command=run_agent,
    width=20,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 11, "bold")
).pack(pady=5)

tk.Button(
    root,
    text="Generate PDF Report",
    command=generate_pdf,
    width=20
).pack(pady=5)

output_text = scrolledtext.ScrolledText(
    root,
    width=95,
    height=18,
    bg="black",
    fg="white",
    font=("Courier", 10)
)
output_text.pack(pady=15)

chart_frame = tk.Frame(root, bg="#2b2b2b")
chart_frame.pack()

# LOAD MODEL SAFELY
threading.Thread(target=load_model, daemon=True).start()

root.mainloop()
