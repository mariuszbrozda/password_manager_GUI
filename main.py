from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            'email': email,
            'website': website,
            'password': password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
               with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
                website_entry.delete(0, END)
                password_entry.delete(0, END)
        else:
            # Update old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
               website_entry.delete(0, END)
               password_entry.delete(0, END)
               email_entry.delete(0, END)



def search():

    try:
        website = website_entry.get()
        with open('data.json', 'r') as read_json:
            read_data = json.load(read_json)
            search_password = read_data[website]['password']
            search_email = read_data[website]['email']
    except FileNotFoundError:
        new_website = messagebox.askokcancel(title="Oops", message=f"Sorry, there is no password saved for ' {website} ' \n Do you want to add {website} first ")
        if new_website:
            generate_password()
            messagebox.showwarning(title="Add email", message=f"Please add email adress. ")
    except KeyError:
        new_website = messagebox.askokcancel(title="Oops", message=f"Sorry, there is no website with that name. \n Do you want to add {website} first ")
        if new_website:
            generate_password()
            messagebox.showwarning(title="Add email", message=f"Please add email adress. ")
    else:
        password_entry.insert(END, search_password)
        email_entry.insert(END, search_email)
        messagebox.showinfo(title=website, message=f"Email: {search_email} \n Password: {search_password} \n ")



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=0, pady=0, bd=0)
window.geometry('650x450')


# Background
img = PhotoImage(file="../password_manager_pyhton/locker-bg.png")
bg = Label(window, image=img, bd=0, highlightthickness=1)
bg.grid(row=0, column=0)

#Labels
website_label = Label(text="Website:", relief='flat', font=('Helvetica', 14, ),
                      padx=2, pady=2, fg='white', bd=1, bg='SkyBlue4', highlightthickness=0, highlightbackground='green')
website_label.place(x=306, y=230)

email_label = Label(text="Email/Username:", relief='flat', font=('Helvetica', 14, ),
                      padx=2, pady=2, fg='white',bd=1, bg='SkyBlue4', highlightthickness=0, )
email_label.place( x=305, y=261)

password_label = Label( text="Password:", relief='flat', font=('Helvetica', 14, ),
                      padx=2, pady=2, fg='white',bd=1, bg='SkyBlue4', highlightthickness=0,)
password_label.place( x=305, y=292)

#Entries
website_entry = Entry(width=16,  font=('Helvetica', 15, ),
                       fg='white',bd=0, bg='SkyBlue4',highlightbackground='SkyBlue4', highlightthickness=2, highlightcolor='white')
website_entry.place(x=377, y=231)
website_entry.focus()

email_entry = Entry(width=18, font=('Helvetica', 15, ),
                       fg='white',bd=0, bg='SkyBlue4',highlightbackground='SkyBlue4', highlightthickness=2, highlightcolor='white',)
email_entry.place(x=432, y=262)

password_entry = Entry( width=23, font=('Helvetica', 15, ),
                       fg='white',bd=0, bg='SkyBlue4',highlightbackground='SkyBlue4', highlightthickness=2, highlightcolor='white')
password_entry.place( x=389, y=293)

# Buttons

generate_password_button = Button( text="Generate Password", command=generate_password, relief='sunken', font=('Helvetica', 15, 'bold'), bg='SkyBlue4',)
generate_password_button.place( x=305, y=325)

search_button = Button( text="Search", relief='sunken', command=search, width=7, font=('Helvetica', 15, 'bold' ),)
search_button.place( x=532, y=231)

add_button = Button( text="Add", command=save, relief='sunken',  width=14, font=('Helvetica', 15, 'bold'),)
add_button.place(x=472, y=325)

window.mainloop()