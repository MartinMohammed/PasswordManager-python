# * imports all classes and constants but not modules
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
# this package is useful for copy in the clipboard - .copy(string) or .paste() what is in clipboard
import pyperclip
import json

# searching in a json (javaScript object notation) is a better format than a plain text file
# it is basically a list bunch of dictionaries and lists
"""
in-build functions 
To write: json.dump() --> takes json data and convert to python dictionary  
To read: json.read() 
to update: json.update() --> update the existing data in the JSON file with new data  
"""

# ---------------------------- Password Manager by @SouthPoleTux  ------------------------------- #

# constants
BG = "black"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    # list comprehension to reduce redundant code
    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_numbers = [choice(symbols) for _ in range(nr_numbers)]
    password_symbols = [choice(numbers) for _ in range(nr_symbols)]

    # we can just add list together to a big list
    password_list = password_letters + password_numbers + password_symbols

    # double shuffle - is shuffling / mixing the iterator (password_list)
    shuffle(password_list)
    shuffle(password_list)

    # the join function puts iterables together into a string (ok: list, tuple, dictionary, sets (only values or keys))
    password = "".join(password_list)
    entry_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # gut user input with the entries
    website = entry_website.get()
    email_username = entry_email_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password
        }
    }
    # a string can also have boolean value: if its empty "" its false else True
    # the all function looks if all values in the tuple have values in it
    # if yes it wil return True else False
    if all((website, email_username, password)):
        # all field are got input now ask user if he wants to save the input
        # output will be a boolean

        # standard dialogs --> Message Boxes (tkMessageBox) module provides an interface to the message dialogs
        # with show you can see many optional popups
        is_ok = messagebox.askokcancel(title="hello", message=f"These are the details you entered: "
                                                              f"\nEmail: {email_username}"
                                                              f"\nPassword: {password}"
                                                              f"\nIs it ok to save?")
        # user agrees to save his data into the file
        if is_ok:
            try:
                with open("Credentials.json", mode="r") as file:
                    # reading old json data
                    data = json.load(file)
            # combining two exceptions both have same solution
            # when file does not exist or file exist but is empty
            except (FileNotFoundError, json.JSONDecodeError):
                # create the missing file - empty file
                with open("Credentials.json", mode="w") as file:
                    # number of spaces to indent all the JSON Data --> much easier to read
                    json.dump(new_data, file, indent=4)

            # when everything worked = file exist and file have input
            else:
                # update old data with new data
                if website in data.keys():
                    override = messagebox.askyesno(title="Warning", message=f"{website} is already in database."
                                                                            f"\nDo you really want to override?"
                                                                           f"\nOtherwise please lookup Credentials "
                                                                            f"with Search function!")
                    # if user wants to override the data inside the file
                    if override:
                        data[website] = {"email": email_username, "password": password}
                        with open("Credentials.json", mode="w") as file:
                            json.dump(data, file, indent=4)
                    # not overriding
                    else:
                        pass
                # if website not in database
                else:
                    # update the data (complementing it) and add the new data into the file
                    data.update(new_data)
                    with open("Credentials.json", mode="w") as file:
                        json.dump(data, file, indent=4)
            # execute no matter what - clear input of entries
            finally:
                entry_website.delete(0, END)
                entry_password.delete(0, END)
                entry_email_username.delete(0, END)
        # if user does not want to save his data - (maybe FingerSlip)
        else:
            # now the user have the chance to add again
            pass

    # if some fields are empty = not valid input to save:
    else:
        # then he can try again write input on the field
        messagebox.showwarning(title="Warning", message="Please check your input!\nFields must have input!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def find_password():
    searching_website = entry_website.get()
    try:
        with open("Credentials.json", mode="r") as file:
            content = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(title="Database", message="Database is empty.\nPlease add some Data to save.")
    # file exist and is not empty
    else:
        if searching_website != "":
            if searching_website in content.keys():
                # s_w_d --> searching website dictionary where username and password is contained
                s_w_d = content[searching_website]
                messagebox.showinfo(title="Database", message=f"For {searching_website}"
                                                              f"\nUsername is: {s_w_d['email']}"
                                                              f"\nPassword is: {s_w_d['password']}")
            # when there is no entry for the website in the file
            else:
                messagebox.showinfo(title="Database", message=f"No Entry for {searching_website} in Database! ")
        # when user did not specify which website to search in the file
        else:
            messagebox.showwarning(title="Warning", message="Please specify your target in Website Entry field! ")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG)

canvas = Canvas(width=200, height=200, bg=BG, highlightthickness=0)
MYIMAGE = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=MYIMAGE)
canvas.grid(row=0, column=1)
# column-span - to span on columns

# other widgets
# labels
label_website = Label(text="Website:", bg=BG)
label_website.grid(row=1, column=0)

label_email_username = Label(text="Email/Username:", bg=BG)
label_email_username.grid(row=2, column=0)

label_password = Label(text="Password:", bg=BG)
label_password.grid(row=3, column=0)

# entries
entry_website = Entry(width=21)
entry_website.grid(row=1, column=1, columnspan=1)
# will focus on the cursor in the textfield - so you do not have to click at the text field
entry_website.focus()

entry_email_username = Entry(width=39)
entry_email_username.grid(row=2, column=1, columnspan=2)

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1, columnspan=1)

# button
button_generate_pw = Button(text="Generate Password", width=13, command=generate_password)
button_generate_pw.grid(row=3, column=2)

button_add = Button(text="Add", width=36, command=save)
button_add.grid(row=4, column=1, columnspan=2)

button_search = Button(text="Search", width=13, command=find_password)
button_search.grid(row=1, column=2)

window.mainloop()
