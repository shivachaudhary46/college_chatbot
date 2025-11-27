from transformers import pipeline 

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

query = "I was present yesterday but i was absent today ? did i pass my attendance optimum 70 % ?"


def classify_text(query):
    candidate_labels = ["attendance", "fees", "marks", "course", "assignment", "college", "user_info", "general"]
    result = classifier(query, candidate_labels=candidate_labels)
    
    # Get the label with highest score (first item in the result)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    
    return top_label

print(classify_text(query))