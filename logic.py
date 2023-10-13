import os
import requests
import openai
from bs4 import BeautifulSoup

openai.api_key = 'YOUR-OWN-KEY'


def webScrapper(link):
    headers = {
        'User-Agent': 'FILL YOUR OWN '
                      'FILL YOUR OWN '
                      'FILL YOUR OWN ',
    }
    url = link
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        data = BeautifulSoup(result.text, "html.parser")

    else:
        print(f"Failed to fetch HTML. Status code: {result.status_code}")
        return "Empty"

    return data


def text_splitter(text) -> str:
    words_per_line = 20
    word_count = 0
    words = text.split()
    formatted_text = ""
    for word in words:
        if word_count == words_per_line:
            formatted_text += '\n'
            word_count = 0
        formatted_text += word + ' '
        word_count += 1
    return formatted_text


def text_splitter_for_file(file, text):
    words_per_line = 20
    word_count = 0
    words = text.split()
    for word in words:
        if word_count == words_per_line:
            file.write('\n')
            word_count = 0
        file.write(word+' ')
        word_count +=1

def clean_text(filename: str) -> str:
    invalid_chars = ['</title>', '<title>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename


def file_creator(data) -> None:
    # Check if the file already exists
    directory = r'C:\Users\.....'
    file_name = clean_text(data.title.string) + '.txt'
    directory = os.path.join(directory, file_name)

    with open(directory, 'w') as file:
        file.write(str(data.title))
        file.write('\n')
        p_tags = data.find_all('p')
        if data != "Empty":
            for paragraph in p_tags:
                if paragraph.parent.get('id') == 'story_source':
                    break
                text_splitter_for_file(file, paragraph.getText(strip=True))
    print(f"{file_name} created")


def chat_gpt(data):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", 
         "content": "Write a detailed summary of the following scientific news article." + str(data)}]
    )
    print(response["choices"][0]["message"]["content"])
    
    return response["choices"][0]["message"]["content"]
