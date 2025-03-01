import os
import pytesseract
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Set Tesseract OCR path (if not in system PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update path as needed

# Load the BLIP model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img).strip()
    return text

def generate_image_summary(image_path):
    """Generate a scene description summary using BLIP image captioning model."""
    img = Image.open(image_path).convert("RGB")

    # Preprocess the image
    inputs = processor(img, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
    
    summary = processor.decode(output[0], skip_special_tokens=True)
    return summary

def process_image(image_path):
    """Main function to process an image: OCR first, then image summarization if needed."""
    extracted_text = extract_text_from_image(image_path)

    if extracted_text:
        print("\n✅ Extracted Text from Image:\n", extracted_text)
        return extracted_text
    else:
        print("\n⚠️ No readable text found! Generating image summary...")
        summary = generate_image_summary(image_path)
        print("\n📸 Image Scene Summary:\n", summary)
        return summary

if __name__ == "__main__":
    # Example usage
    image_file = r"C:\playGround\projects\Agentica_t2\backend\aiFileManager\extract_file_content\test_img.jpg"  # Update with your image path
    process_image(image_file)
