from flask import Flask, request, jsonify, send_file
import json
import requests
from PIL import Image
from io import BytesIO
import os
import base64
import openai
import json
import random
import string
from pydub import AudioSegment
import textwrap
# from chapter_split import split_chapters
import nltk
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from difflib import Differ
from bs4 import BeautifulSoup
import tiktoken
from pydub import AudioSegment
import logging
import multiprocessing
import http.client
import urllib.parse
import re
from word2number import w2n
from werkzeug.utils import secure_filename
from deepgram import DeepgramClient

app = Flask(__name__)

key = os.getenv('openai_key')
rapid_api_key = os.getenv('rapid_api_key')
deepkey = os.getenv('deepkey')
openai.api_key = key

dg = DeepgramClient(deepkey)
MIMETYPE = 'wav'
params = {
    "punctuate": True,
    "model": 'general',
    "tier": 'nova'
}

book_dict_before_edited = {}
grammar_edited_book = {}
tone_edited_book = {}

nltk.download('punkt')
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

model_name = 'gpt-3.5-turbo-16k-0613'
num_processes_tone = multiprocessing.cpu_count()
num_processes = 1
print("Number of CPU Cores", num_processes)


def num_tokens_from_string(string: str, encoding_name=model_name):
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens + 7


def merge_sentences(sentences):
    merged_list = []
    current_sentence = ""
    for sentence in sentences:
        if num_tokens_from_string(current_sentence + sentence) <= 2000:
            if current_sentence != "":
                current_sentence += " "
            current_sentence += sentence
        else:
            merged_list.append(current_sentence)
            current_sentence = sentence
    if current_sentence:
        merged_list.append(current_sentence)
    return merged_list


def merge_sentences_grammar(sentences):
    merged_list = []
    current_sentence = ""
    for sentence in sentences:
        if num_tokens_from_string(current_sentence + sentence) <= 800:
            if current_sentence != "":
                current_sentence += " "
            current_sentence += sentence
        else:
            merged_list.append(current_sentence)
            current_sentence = sentence
    if current_sentence:
        merged_list.append(current_sentence)
    return merged_list


def split_into_sentences(text):
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_tokenizer.tokenize(text)
    return sentences


def grammar_check_api(sentence):
    conn = http.client.HTTPSConnection(
        "ai-based-spelling-and-grammar-correction.p.rapidapi.com")
    payload = f"text={sentence}"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Key': rapid_api_key,
        'X-RapidAPI-Host': "ai-based-spelling-and-grammar-correction.p.rapidapi.com"
    }

    conn.request("POST", "/data", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    wrapped_edited_text = textwrap.fill(data, width=80)
    return wrapped_edited_text


'''
    lines = wrapped_edited_text.split('\n')
    # Wrap each line of text and its line number in a container
    wrapped_lines = [f"<div class='line-container'><span class='line-number'>{i+1}</span><span class='text-line' contenteditable='true'>{line}</span></div>" for i, line in enumerate(lines)]
    wrapped_text = "".join(wrapped_lines)
    
    # Return the formatted text with line numbers
    return f"""
    <style>
    .line-container {{
        display: flex;
    }}
    .line-number {{
        color: #888;
        user-select: none;
        width: 40px;  /* Adjust width as needed */
        text-align: right;
        margin-right: 10px;
    }}
    .text-line {{
        white-space: pre-wrap;
        font-family: monospace;
        flex-grow: 1; /* Allows the text line to grow as needed */
    }}
    </style>
    <div class='text-with-lines'>{wrapped_text}</div>
    """
'''


def reset_system_audio_file():
    book_dict_before_edited.clear()
    grammar_edited_book.clear()
    tone_edited_book.clear()

    delete_files_in_directory('/tmp/gradio/wave_files/')
    delete_files_in_directory('/tmp/gradio/')
    return "Reset Completed"


def deepgram_transcription(audio_files):
    for audio_file in audio_files:
        file_name = os.path.basename(audio_file).split(".")[0]
        with open(audio_file, "rb") as f:
            source = {"buffer": f, "mimetype": 'audio/' + MIMETYPE}
            data = dg.transcription.sync_prerecorded(source, params)
            result = {"text": data['results']['channels']
                      [0]['alternatives'][0]['transcript']}
            random_code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=6))
            json_file_path = f"/tmp/gradio/wave_files/{file_name}_{random_code}.json"

            with open(json_file_path, "w") as transcript:
                json.dump(result, transcript)

    return "/tmp/gradio/wave_files/"


def transcribe_audio_files(audio_files):
    converted_audio_paths = []

    for audio_file in audio_files:
        file_path = audio_file.name
        print(file_path)
        audio_file_name = os.path.basename(file_path).split(".")[0]
        folder_path = "/tmp/gradio/wave_files"

        # Create directory for wave files if not exists
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except:
                pass

        # Replace spaces with underscores in the filename
        audio_file_name_cleaned = audio_file_name.replace(" ", "_")
        # Generate a random code
        random_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))

        # Create the converted audio file path with the random code
        converted_audio_path = os.path.join(folder_path,
                                            os.path.splitext(audio_file_name_cleaned)[0] + f"_{random_code}.wav")
        converted_audio_paths.append(converted_audio_path)

        # Read the audio file from Google Drive into memory
        with open(file_path, "rb") as f:
            audio_path = f.read()

        # Convert the audio from Google Drive to WAV format
        convert_to_wav(audio_path, converted_audio_path)
        print("Audio conversion to WAV format complete:", audio_file.name)

    whole_book_dict = {}
    transcript_dict = {}
    wave_audio_paths = deepgram_transcription(converted_audio_paths)
    transcript_dict = generate_transcript(wave_audio_paths)
    whole_book_dict = generate_whole_book(transcript_dict)
    # return whole_book_dict
    lines = whole_book_dict.split('\n')
    # Wrap each line of text and its line number in a container
    wrapped_lines = [
        f"<div class='line-container'><span class='line-number'>{i+1}</span><span class='text-line' contenteditable='true'>{line}</span></div>" for i, line in enumerate(lines)]
    wrapped_text = "".join(wrapped_lines)

    # Return the formatted text with line numbers
    return f"""
    <style>
    .line-container {{
        display: flex;
    }}
    .line-number {{
        color: #888;
        user-select: none;
        width: 40px;  /* Adjust width as needed */
        text-align: right;
        margin-right: 10px;
    }}
    .text-line {{
        white-space: pre-wrap;
        font-family: monospace;
        font-size: small;
        flex-grow: 1; /* Allows the text line to grow as needed */
    }}
    </style>
    <div class='text-with-lines'>{wrapped_text}</div>
    """


edited_transcription = ""


def save_edited_transcription(content):
    global edited_transcription
    edited_transcription = content
    return "Transcription saved!"


def show_saved_transcription():
    # This function will return the saved transcription
    global edited_transcription
    return edited_transcription


def reset_system_audio_file():
    book_dict_before_edited.clear()
    grammar_edited_book.clear()
    tone_edited_book.clear()

    delete_files_in_directory('/tmp/gradio/wave_files/')
    delete_files_in_directory('/tmp/gradio/')
    return "Reset Completed"


def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


def convert_to_wav(input_audio, output_path):
    audio = AudioSegment.from_file(io.BytesIO(input_audio))
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")


def generate_transcript(scripts_directory):
    file_count = 1
    transcript_text_list = []
    chapter_dict = {}

    for filename in os.listdir(scripts_directory):
        file_path = os.path.join(scripts_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".json"):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                wrapped_text = textwrap.fill(data['text'], width=80)
                chapter_dict[f'transcrption_file_{file_count}'] = wrapped_text
                file_count += 1
    return chapter_dict


def generate_whole_book(transcript_dict):
    whole_book_dict = {}

    for keys, texts in transcript_dict.items():
        splited_chapters = split_chapters(texts)
        whole_book_dict.update(splited_chapters)

    return display_whole_book(whole_book_dict)


def display_whole_book(whole_book_dict):
    book_before_edited = ""

    def custom_sort_key(key):
        if key == 'Introduction':
            return 0
        else:
            return int(key.split(' ')[-1])

    sorted_book_dict = dict(
        sorted(whole_book_dict.items(), key=lambda x: custom_sort_key(x[0])))

    global book_dict_before_edited
    book_dict_before_edited = sorted_book_dict

    for keys, text in sorted_book_dict.items():
        book_before_edited += f"<h2>{keys}</h2>"
        book_before_edited += "<br>"
        book_before_edited += f"<p>{text}</p>"
        book_before_edited += "<br>"

    # html_text_body = f"""<div onmousedown="return false" onselectstart="return false">{book_before_edited}</div>"""
    return book_before_edited


def convert_word_to_number(word):
    try:
        number = w2n.word_to_num(word)
    except:
        pass
        number = None
    return number


def split_chapters(wrapped_text):
    try:
        hole_para = wrapped_text.strip()
        chapter_list = []
        output_chapter_text = ""
        book_dict = {}

        # Check it is introduction
        if re.compile(r'\b' + re.escape("introduction") + r'\b', re.IGNORECASE).search(wrapped_text[:100]):
            lines = wrapped_text.split('.')
            modified_text = '.'.join(lines[1:])
            output_chapter_text += "----------Introduction-----------"
            output_chapter_text += "\n"
            output_chapter_text += modified_text
            book_dict = {"Introduction": modified_text}
            return book_dict

        # Split chapter text
        word = 'chapter'
        split_text = re.split(rf'(?i)\s*{re.escape(word)}\s*', hole_para)

        for idx, text in enumerate(split_text):
            if text.strip() != "" and len(text) > 1:
                words = text.split()
                first_word = words[0]
                last_word = words[len(words) - 1]
                chapter_numb = convert_word_to_number(first_word[:-1])

                if chapter_numb is not None and chapter_numb not in chapter_list:
                    # Append the chapter number incrementally
                    # print("\n")
                    chapter_list.append(chapter_numb)
                    output_chapter_text += f"CHAPTER."
                    # print("----------------", "Chapter:", chapter_numb, "------------------")
                    # Remove Chapter numbers in sentences
                    words = words[1:]
                    # Captialize first letter in first word
                    word_one = words[0].capitalize()

                    # Remove End word in the sentences
                    word_lst = words[len(words) - 1].lower()

                    if word_lst == "and" or word_lst == "end":
                        words.pop()

                    # Generate the sentence
                    chapter_text = f"{word_one} " + " ".join(words[1:])
                    chapter_text = textwrap.fill(
                        chapter_text.strip(), width=80)
                    chapter_text = chapter_text.strip()
                    output_chapter_text += chapter_text
                    # print(chapter_text)

                else:
                    word_one = words[0]
                    if word_one[len(word_one) - 1] == "." or word_one == ".":
                        words = words[1:]
                    else:
                        words = ["chapter "] + words

                    # Remove End word in the sentences
                    try:
                        word_lst = words[len(words) - 1].lower()
                        if word_lst == "and" or word_lst == "end":
                            words.pop()
                    except:
                        pass

                    chapter_text = " ".join(words)
                    chapter_text = textwrap.fill(
                        chapter_text.strip(), width=80)
                    chapter_text = chapter_text.strip()
                    output_chapter_text += chapter_text

        split_chapters = output_chapter_text.split("CHAPTER.")
        chapter_count = 0
        for chapter in split_chapters:
            if len(chapter) > 0:
                book_dict[f'Chapter {chapter_list[chapter_count]}'] = chapter
                chapter_count += 1

        return book_dict

        # return output_chapter_text
    except Exception as e:
        return f"Error occured when coverting to the chapters: {e}"


def langchain_function(prompt):
    chat_model = ChatOpenAI(
        temperature=0.4, openai_api_key=key, model_name=model_name)
    prompt = prompt
    messages = [HumanMessage(content=prompt)]
    edited_ouput = chat_model.predict_messages(messages)
    wrapped_edited_text = textwrap.fill(edited_ouput.content, width=80)
    return wrapped_edited_text


def generate_HTML_dict_from_input1(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    data = {}
    current_key = None

    for container in soup.find_all(class_="line-container"):
        text_line = container.find(class_="text-line")
        if text_line:
            h2_tag = text_line.find('h2')
            if h2_tag:
                current_key = h2_tag.text.strip()
                h2_tag.extract()

            if current_key:
                data.setdefault(current_key, "")
                data[current_key] += text_line.get_text(
                    separator=" ", strip=True) + " "

    for key in data:
        data[key] = remove_leading_number(data[key])

    return data


def generate_HTML_dict_from_input2(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    data = {}
    current_key = None

    # Find the first h2 tag as the key
    h2_tag = soup.find('h2')
    if h2_tag:
        current_key = h2_tag.text.strip()

    # Find the text-with-lines div and extract text
    text_with_lines_div = soup.find('div', class_='text-with-lines')
    if text_with_lines_div and current_key:
        text_lines = text_with_lines_div.find_all(class_="text-line")
        text_content = " ".join(
            [line.get_text(separator=" ", strip=True) for line in text_lines])
        data[current_key] = remove_leading_number(text_content)

    return data


def remove_leading_number(text):
    return re.sub(r'^\s*\d+\s*', '', text)


def generate_HTML_dict_from_input2_tone(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    data = {}
    current_key = None

    # Find the first h2 tag as the key
    h2_tag = soup.find('h2')
    if h2_tag:
        current_key = h2_tag.text.strip()
        # Find the next sibling that is a paragraph (p) tag
        next_p_tag = h2_tag.find_next_sibling('p')
        if next_p_tag:
            data[current_key] = next_p_tag.get_text(separator=" ", strip=True)

    return data


def check_grammar_spellings_file():
    grammar_edited_book_now = {}
    print('book_dict_before_edited', type(
        book_dict_before_edited), book_dict_before_edited)
    for key, text in book_dict_before_edited.items():
        print('text', text)
        try:
            print("Start grammar check:", key)
            t1 = time.time()
            text = remove_leading_number(text)
            chapter_sentences = split_into_sentences(text)
            token_safe_texts = merge_sentences_grammar(chapter_sentences)
            grammer_edited = grammar_prompt(token_safe_texts)
            t2 = time.time()
            print("Time spent:", t2 - t1)
            print("End grammar check:", key)
        except:
            pass
            print("Error in tone check:", key)
            grammer_edited = text
        grammar_edited_book_now[key] = grammer_edited
        yield display_whole_book(grammar_edited_book_now)

    global grammar_edited_book
    grammar_edited_book = grammar_edited_book_now


def grammar_prompt(text):
    prompt_list = []
    for sentences in text:
        sentences.strip()
        # prompt = """You are going to act as a proofreader. Read the below text and split the whole text into sentences. By looping through each and every sentence, you need to correct any spelling, grammar, or punctuation errors and return the corrected text. Important: Do not change its meaning or content."""
        # prompt += "\n"
        # prompt += sentences
        # prompt = sentences
        prompt_list.append(sentences)

    print("Number of requests for grammar:", len(prompt_list))
    with multiprocessing.Pool(processes=num_processes) as pool:
        # results = pool.map(langchain_function, prompt_list)
        results = pool.map(grammar_check_api, prompt_list)
    print(results)
    out_put_text = ' '.join(results)
    # return out_put_text

    lines = out_put_text.split('\n')
    # Wrap each line of text and its line number in a container
    wrapped_lines = [
        f"<div class='line-container'><span class='line-number'>{i+1}</span><span class='text-line' contenteditable='true'>{line}</span></div>" for i, line in enumerate(lines)]
    wrapped_text = "".join(wrapped_lines)

    # Return the formatted text with line numbers
    return f"""
    <style>
    .line-container {{
        display: flex;
    }}
    .line-number {{
        color: #888;
        user-select: none;
        width: 40px;  /* Adjust width as needed */
        text-align: right;
        margin-right: 10px;
    }}
    .text-line {{
        white-space: pre-wrap;
        font-family: monospace;
        flex-grow: 1; /* Allows the text line to grow as needed */
    }}
    </style>
    <div class='text-with-lines'>{wrapped_text}</div>
    """


def check_tone_of_the_book_file(tone, tone1):
    tone_edited_book_now = {}
    if not grammar_edited_book:
        print("grammar_edited_book is empty")
        return tone_edited_book_now

    for key, text in grammar_edited_book.items():
        try:
            print(f"Start tone check for {key}")
            chapter_sentences = split_into_sentences(text)
            token_safe_texts = merge_sentences(chapter_sentences)
            tone_edited = tone_prompt(token_safe_texts, tone, tone1)
            if tone_edited:
                tone_edited_book_now[key] = tone_edited
                print(f"End tone check for {key}")
            else:
                print(f"No tone edited content for {key}")
        except Exception as e:
            print(f"Error in tone check for {key}: {e}")

    global tone_edited_book
    tone_edited_book = tone_edited_book_now
    return tone_edited_book_now


def tone_prompt(texts, tone, tone1):
    prompt_list = []
    for text in texts:
        new_tone = tone.lower()
        text.strip()
        prompt = f""" You are going to act as a Tone Changer. Read the below text and arrange the text's tone to {new_tone,tone1} tone. Important: Do not change the meaning of the text when changing the tone and make sure changed text is different from original text. """
        prompt += "\n"
        prompt += text
        prompt_list.append(prompt)
    print("Number of langchain requests for tone:", len(prompt_list))
    with multiprocessing.Pool(processes=num_processes_tone) as pool:
        results = pool.map(langchain_function, prompt_list)

    out_put_text = ' '.join(results)
    return out_put_text


def generate_press_release(data):
    try:
        # Construct the prompt using user-provided values
        prompt_text = f"""Generate output with the following details and follow the structure thoroughly, add more chapters as possible and write more about each and every chapter.
                           Output should be at least 3500 words.:
                           print Book Title: {data['book_title']}
                           print Subtitle: {data['book_sub']}
                           print Instructions: {data['instruction']}
                           print Tagline: {data['tag']}
                           Author Name: {data['name']}
                           printing above inputs one over one is in bold must.
                           Take this inputs {data['book_type']},{data['book_status']},{data['book_desc']},{data['choice']},{data['ques1']},{data['ques2']},{data['ques3']},{data['ques4']},{data['ques5']},{data['ques6']},{data['ques7']},{data['ques8']} and give me the
                           and generate,
                           Introduction and add points as instructions, below the Introduction add chapters.
                           Chapters and points should add there as instructions.
                           Name that as chapter 1,2,3...
                           
                           Ensure the above structure thoroughly.
                           Give this as formatted HTML output.
                           """

        # Use GPT-3.5 Turbo to generate the press release
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 Turbo engine
            prompt=prompt_text,
            max_tokens=2500,  # Set the desired press release length
            temperature=0.9,  # Adjust the temperature for creativity
        )

        # Extract the generated press release from the GPT-3.5 Turbo response
        press_release = response['choices'][0]['text'].strip()
        press_release.strip("\t")
        return press_release
    except Exception as e:
        return str(e)


UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.DEBUG)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/generate_cover_image', methods=['POST'])
def generate_cover_image():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    open_user_prompt = data.get('open_user_prompt')
    open_author = data.get('open_author')
    open_tagline = data.get('open_tagline')
    image_url = data.get('image_url')
    size1 = data.get('size1')
    size2 = data.get('size2')

    api_url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}'
    }
    data = {
        "model": "dall-e-3",
        "prompt": f"""
           Reference image: {image_url}
           Generate a image design for titled embossed text`{open_user_prompt}` is first priority in the top of the Ai generated image design with bold letters.
           Bottom of the Ai generated image design palced embossed text `{open_author}` using semi-bold letters.
           The slogan embossed text`{open_tagline}` should be placed on the second priority in the cover design.
           Aim for a simple and straightforward style, avoiding unnecessary details and prioritizing a clean and minimalist design that allows the illustration to stand out.
           The illustration should be a full-body view in portrait orientation with a "{size1} x {size2}".
           Ensure, Do not include any 3D views of the image, show only flat Ai generated image view, and Do not add elements that distract from the main illustration.
           The generated image fits the entire body in portrait orientation. Focus on creating only 2D image. Focus on the quality of the text that generates.
           Do not add shadows to the illustration.
           Please mark this as a high priority, do not mistake letters provided `{open_user_prompt}` and `{open_author}`, `{open_tagline}`. I want exact same letters as provided to the inputs.
           Do not add any objects to the illustration generated image.
           Focus more priority on `{open_user_prompt}` and `{open_author}` and `{open_tagline}` to avoid spelling mistakes and clearly print all the letters the output image.
       """,
        "n": 1,
        "size": f"{size1}x{size2}"
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        generated_image_url = result['data'][0]['url']

        # Fetch the image data from the URL
        image_response = requests.get(generated_image_url)
        image = Image.open(BytesIO(image_response.content))
        img_io = BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
    else:
        return jsonify({"error": f"Error: {response.status_code} {response.text}"})


@app.route('/initial-form', methods=['POST'])
def generate_press_release_endpoint():
    try:
        data = request.json

        result = generate_press_release(data)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/transcribe', methods=['POST'])
def transcribe_text():
    try:
        # Assuming text is sent as JSON
        data = request.get_json()
        text = data.get('text')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Split the text into sentences
        sentences = split_into_sentences(text)

        # Perform grammar correction on each sentence
        corrected_sentences = [grammar_check_api(
            sentence) for sentence in sentences]

        # Join the corrected sentences back into a single string
        processed_text = " ".join(corrected_sentences)

        # Return the processed text
        return jsonify({"processed_text": processed_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/check-tone', methods=['POST'])
def check_tone():
    try:
        data = request.json
        text = data.get('text')
        tone = data.get('tone')
        tone1 = data.get('tone1')

        if not text or not tone:
            logging.error("Missing text or tone in the request")
            return jsonify({"error": "Missing text or tone"}), 400

        # Split the text into sentences and merge them for token safety
        chapter_sentences = split_into_sentences(text)
        token_safe_texts = merge_sentences(chapter_sentences)

        # Adjust the tone of the text
        tone_edited = tone_prompt(token_safe_texts, tone, tone1)

        if not tone_edited:
            logging.warning("The result is empty")
            return jsonify({"result": "No content available for the given tone adjustments"})

        return jsonify({"result": tone_edited})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload-audio', methods=['POST'])
def transcribe_audio():
    print("Received request")

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "No selected file or file type not allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    print("File saved successfully")

    # Read the audio file
    with open(file_path, 'rb') as audio_file:
        audio_content = audio_file.read()

    # Deepgram API endpoint
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        # Replace with your Deepgram API key
        "Authorization": "Token 7d2edf49af806f4d3f33e56f839468c61b372823",
        "Content-Type": file.content_type
    }

    # Parameters for the Deepgram API
    params = {
        "filler_words": "false",
        "summarize": "v2"
    }

    # Send the request to Deepgram
    try:
        response = requests.post(
            url, params=params, data=audio_content, headers=headers)
        response.raise_for_status()
        print("Received response from Deepgram")
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": "HTTP Error", "details": str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request Exception", "details": str(e)}), 500

    # Process the response
    json_response = response.json()
    transcript = json_response.get("results", {}).get("channels", [{}])[
        0].get("alternatives", [{}])[0].get("transcript", "")

    # Define the regular expression pattern
    pattern = r'(Chapter (One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty)|Conclusion|Introduction)'

    # Function to add bold formatting
    def bold_text(match):
        return f"**{match.group()}**"

    # Replace occurrences in the transcript with the bold version
    formatted_transcript = re.sub(
        pattern, bold_text, transcript, flags=re.IGNORECASE)

    return jsonify({"transcript": formatted_transcript})


if __name__ == '__main__':
    app.run(debug=True)
