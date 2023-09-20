from tkinter import *
import pandas as pd
from random import randint, choice

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "French"
FONT_NAME = "Ariel"

# ---- LOGIC ----

current_card = {}

try:
    df = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("./data/french_words.csv")

to_learn = df.to_dict(orient="records")


def select_word():
    global current_card, card_timer
    window.after_cancel(card_timer)
    current_card = choice(to_learn)
    french_word = current_card["French"]
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(canvas_title, text=LANGUAGE, fill="black")
    canvas.itemconfig(canvas_word, text=french_word, fill="black")
    window.after(3000, flip_card)


def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(canvas_word, text=english_word, fill="white")
    canvas.itemconfig(canvas_title, text="English", fill="white")


def remove_word():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    select_word()

# ---- UI -------


window = Tk()
window.title("Flash Cards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

card_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR,highlightthickness=0)
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 265, image="")
canvas_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, "40", "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

right_icon = PhotoImage(file="./images/right.png")
wrong_icon = PhotoImage(file="./images/wrong.png")

button_right = Button(width=100, height=100, image=right_icon, borderwidth=0, highlightthickness=0, command=remove_word)
button_wrong = Button(width=100, height=100, image=wrong_icon, borderwidth=0, highlightthickness=0, command=select_word)
button_wrong.grid(column=0, row=1, padx=100)
button_right.grid(column=1, row=1, padx=100)

select_word()

mainloop()
