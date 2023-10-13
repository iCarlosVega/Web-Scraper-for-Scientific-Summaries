import threading
from tkinter import *
from tkinter import scrolledtext
from logic import webScrapper, text_splitter, file_creator, chat_gpt, clean_text


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


#Creates window
def start():
    def start_scraping():
        def background_task():
            url = input.get()
            status_label.config(text="Scrapping...")
            root.update()

            data = webScrapper(url)
            file_creator(data)
            parsed_text.insert(INSERT, clean_text(data.title.string) + '\n')
            parsed_text.insert(INSERT, '\n')
            p_tags = data.find_all('p')
            if data != "Empty":
                for paragraph in p_tags:
                    if paragraph.parent.get('id') == 'story_source':
                        break
                    formatted_text = text_splitter(paragraph.getText(strip=True))
            
            summarized_text = chat_gpt(formatted_text)
            parsed_text.insert(INSERT,str(summarized_text))


            status_label.config(text="Done")

        threading.Thread(target=background_task).start()

    root = Tk()
    root.title("Article Summarizer")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    input = Entry(root, width=90)
    input.pack(pady=20)

    scrape_button = Button(root, text="Scrape", command=start_scraping)
    scrape_button.pack(pady=20)

    parsed_text = scrolledtext.ScrolledText(root, wrap=WORD, width=250, height=50)
    parsed_text.pack(pady=20)

    status_label = Label(root, text="")
    status_label.pack(pady=20)

    root.mainloop()
