from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------------------- create new flash cards ------------------------------- #

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(create_background, image=front_card)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(create_background, image=back_card)

def is_known():
    to_learn.remove(current_card)
    data_learn = pandas.DataFrame(to_learn)
    data_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Quiz Card/ Languages")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")

# Flip cards
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
create_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

right = PhotoImage(file="./images/right.png")
right_button = Button(image=right, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)
wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card())
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
