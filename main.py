from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))] + \
                    [choice(symbols) for _ in range(randint(2, 4))] + \
                    [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("password_data.json") as password_data:
            data = json.load(password_data)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")
    else:
        if website in data:
            found_email = data[website]["email"]
            found_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {found_email}\nPassword: {found_password}")
        else:
            messagebox.showinfo(title="Oops", message=f"No details for {website} exits.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def update_json(data):
    # Save updated data
    with open("password_data.json", "w") as password_data:
        json.dump(data, password_data, indent=4)


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields blank!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}"
                                                              f"\nPassword: {password}\nFor this website: {website}"
                                                              f"\nIs it ok to save?")
        if is_ok:
            try:
                with open("password_data.json", "r") as password_data:
                    # Read old data
                    data = json.load(password_data)
            except FileNotFoundError:
                update_json(new_data)
            else:
                # Update old data with new data
                data.update(new_data)
                update_json(data)
            finally:
                # Reset GUI
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Website
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="nsew")

# Email/Username
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=38)
email_entry.insert(0, "lastkookie101@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

# Password
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="nsew")

# Generate Password
gen_password_btn = Button(text="Generate Password", width=12, command=generate_password)
gen_password_btn.grid(row=3, column=2)

# Add Password
add_btn = Button(text="Add", width=35, command=save_password)
add_btn.grid(row=4, column=1, columnspan=2, sticky="nsew")

# Find Password
find_password_btn = Button(text="Search", width=12, command=find_password)
find_password_btn.grid(row=1, column=2)

window.mainloop()
