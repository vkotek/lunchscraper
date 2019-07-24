from google.cloud import vision
import io
import requests, os

def detect_text(img_path):
    """Detects text in the file."""
    
    client = vision.ImageAnnotatorClient()

    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    text = response.text_annotations
        
    return text[0].description.split("\n")

def get_image(url, output):
    """Download image from URL """
    
    path = os.getcwd() + "/" + output
    
    with requests.get(url) as image:
        with open(output, 'wb') as file:
            file.write(image.content)
    
    return path

def image_to_text(url):
    
    img_path = get_image(url, "img.jpg")
    menu = detect_text(img_path)
    
    return menu
