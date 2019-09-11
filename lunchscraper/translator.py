import os

path = "/home/vojtech/ipython/key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

if os.environ.get('CI') == 'True':
    # For integration testing, don't run API.
    
    def translate(text, source_language, target_language):
        return text
    
else:

    def translate(text, source_language, target_language):

        from google.cloud import translate_v3beta1 as translate
        client = translate.TranslationServiceClient()

        project_id = "lunch-scraper"
        location = "global"

        parent = client.location_path(project_id, location)


        if os.environ.get('CI') != None:
            return text

        if isinstance(text, list):
            text = "\n".join(text)

        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type='text/plain',  # mime types: text/plain, text/html
            source_language_code=source_language,
            target_language_code=target_language)

        try:
            response = response.translations[0].translated_text
            response = response.split("\n")
        finally:
            return response