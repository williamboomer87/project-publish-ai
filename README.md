#Publish-AI
#Overview
This Flask application serves as a server for various AI language processing tasks. It includes functionalities such as transcription of audio files, grammar checking, tone adjustment, and cover image generation using OpenAI models. The application utilizes multiple external APIs, including OpenAI, Deepgram, and RapidAPI.

Prerequisites
Python 3.6 or higher
Required Python packages can be installed using pip install -r requirements.txt
Environment variables:
openai_key: OpenAI API key
rapid_api_key: RapidAPI key
deepkey: Deepgram API key
Getting Started

Clone the repository:

git clone https://github.com/your-username/flask-ai-language-processing.git
cd flask-ai-language-processing

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .env file in the project root and add the following:

openai_key=your_openai_api_key
rapid_api_key=your_rapidapi_key
deepkey=your_deepgram_api_key

Run the Flask application:

python app.py
The server will start running at http://127.0.0.1:5000/

API Endpoints
Generate Cover Image

Endpoint: /generate_cover_image
Method: POST
Request Payload Example:

{
  "open_user_prompt": "Your User Prompt",
  "open_author": "Author Name",
  "open_tagline": "Tagline",
  "image_url": "URL of Reference Image",
  "size1": 800,
  "size2": 1200
}

Generate Press Release

Endpoint: /generate_press_release
Method: POST
Request Payload Example:

{
  "book_title": "Your Book Title",
  "book_sub": "Subtitle",
  "instruction": "Instructions for Press Release",
  "tag": "Tagline",
  "name": "Author Name",
  "book_type": "Type of Book",
  "book_status": "Status of Book",
  "book_desc": "Book Description",
  "choice": "User's Choice",
  "ques1": "Question 1",
  "ques2": "Question 2",
  "ques3": "Question 3",
  "ques4": "Question 4",
  "ques5": "Question 5",
  "ques6": "Question 6",
  "ques7": "Question 7",
  "ques8": "Question 8"
}

Transcribe Text

Endpoint: /transcribe
Method: POST
Request Payload Example:

{
  "text": "Text to Transcribe"
}

Check Tone

Endpoint: /check-tone
Method: POST
Request Payload Example:

{
  "text": "Text to Adjust Tone",
  "tone": "Desired Tone",
  "tone1": "Secondary Tone"
}

Transcribe Audio

Endpoint: /upload-audio
Method: POST
Request Payload Example: Form data with audio file attached
Important Notes
Make sure to provide the required API keys in the environment variables.
Adjust the OpenAI models and other parameters according to your requirements.
