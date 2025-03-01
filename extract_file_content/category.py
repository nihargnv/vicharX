from transformers import pipeline

# Load Pretrained Zero-Shot Classification Model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define Possible Categories (Tags)


# Function to Categorize Summarized Text
def categorize_text(summary):
    CATEGORIES = [
        "Medical Documents",
        "Legal Contracts",
        "Research Papers",
        "Business Reports",
        "Technical Documents",
        "News Articles",
        "Resumes",
        "Invoices",
        "Finance Reports",
        "Others",
    ]
    result = classifier(summary, CATEGORIES, multi_label=False)
    return result["labels"][0]  # Return the highest confidence category


if __name__ == "__main__":
    # Example Summarized Text (Replace this with actual summaries)
    summary_text = "This document describes a legal contract between two parties, outlining obligations and agreements."

    # Get Category (Tag)
    tag = categorize_text(summary_text)

    # Output Result
    print("Summary:", summary_text)
    print("Tag:", tag)
