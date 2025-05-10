from tkinter import *
import pandas
import random

# ---------- CONSTANTS ----------
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = []
current_language = None
current_language_index = -1
language_selected = False

languages = [
    {"name": "Hindi to English"},
    {"name": "French to English"},
    {"name": "Italian to English"},
    {"name": "Spanish to English"},
    {"name": "German to English"}
]

# ---------- FUNCTION DEFINITIONS ----------

def next_card():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text=current_language.split()[0], fill="black")
    canvas.itemconfig(card_word, text=current_card["Word"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    start_flip_timer()

def start_flip_timer():
    global flip_timer
    flip_timer = windows.after(3000, func=flip_card)
def flip_card():
    if "English" in current_card:
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=current_card["English"], fill="white")
        canvas.itemconfig(canvas_image, image=card_back_img)

    print(current_card)
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    file_name = f"data/words_to_learn_{current_language.split()[0].lower()}.csv"
    data.to_csv(file_name, index=False)
    next_card()

def select_language():
    global language_selected, flip_timer
    language_selected = False
    canvas.itemconfig(card_title, text="Which language\ndo you want to learn?", fill="black")
    canvas.itemconfig(card_word, text="", fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    windows.after_cancel(flip_timer)
    flip_timer = windows.after(3000, func=cycle_language)  # <-- ADD THIS LINE

def cycle_language():
    global current_language_index, current_language
    current_language_index = (current_language_index + 1) % len(languages)
    current_language = languages[current_language_index]["name"]
    canvas.itemconfig(card_title, text="", fill="black")
    canvas.itemconfig(card_word, text=current_language, fill="black")
    canvas.itemconfig(canvas_image, image=card_back_img)

def wrong_clicked():
    if not language_selected:
        cycle_language()
    else:
        next_card()

def right_button_clicked():
    global to_learn, language_selected
    if not language_selected:
        language_selected = True
        language_key = current_language.split()[0].lower()
        try:
            data = pandas.read_csv(f"data/words_to_learn_{language_key}.csv")
        except FileNotFoundError:
            data = pandas.read_csv(f"data/{language_key}_words.csv")
        to_learn = data.to_dict(orient="records")
        next_card()
    else:
        is_known()

# ---------- UI SETUP ----------

windows = Tk()
windows.title("FLASHCARD APP")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Add a bold title using a Label
title_label = Label(windows, text="FLASHCARD APP", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

flip_timer = windows.after(3000, func=lambda: None)  # dummy timer

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong_clicked)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_button_clicked)
right_button.grid(row=1, column=1)

# ---------- START APP ----------

select_language()
windows.mainloop()