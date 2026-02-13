from transformers import pipeline

def parse_goal(goal_text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = [
        "social_media_monitoring", "sentiment_analysis", "report_generation",
        "data_collection", "web_scraping", "customer_service", "content_generation"
    ]
    result = classifier(goal_text, candidate_labels)
    return result

if __name__ == "__main__":
    goal = "Monitor social media for brand mentions and generate daily sentiment reports."
    parsed = parse_goal(goal)
    print("Parsed Goal:", parsed)
