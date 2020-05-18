from hashlib import sha256
import sqlite3
import random
import string
import time
import sys
import pyperclip
from tkinter import *
from tkinter import ttk


class PasswordManagerGUI:
    def __init__(self, master):
        # BACK-END
        self.conn = sqlite3.connect(
            r"C:\Users\akush\Desktop\Programming\Projects\Password_Manager\password_database.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Passwords (hash_key text primary key, password text)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS User_Info (service text, username text)")
        self.admin_password = 'Barrys2e5!'
        self.service = ''
        self.user_name = ''
        self.passw = ''
        self.hash_key = ''
        self.num_chars = 0
        # TKINTER SETUP
        self.master = master
        self.tabs = ttk.Notebook(self.master)
        self.master.geometry("450x410")
        # root.configure(bg='#020202')

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text='ADMIN')
        self.tabs.add(self.tab2, text='DATABASE')
        self.tabs.add(self.tab3, text='MANAGER')

        self.tabs.pack(expand=1, fill='both')

        # self.tab1
        self.login_frame = Frame(self.tab1, width=450, height=450, bg='#475a6b')
        self.login_frame.pack()

        self.title = Label(self.tab1, width=25, text='PASSWORD SAFE', font=(
            'System', 20, 'bold'), bg='#475a6b',  fg='#f8f8ff')
        self.title.place(relx=0.03, rely=0.12)

        self.login_text = StringVar()
        self.login_text.set("Enter password.")
        self.login_entry = Entry(self.tab1, textvariable=self.login_text, width=34,
                                 font=('System', 12, 'bold'), justify=LEFT, bg='#f8f8ff')
        self.login_entry.place(relx=0.02, rely=0.42)

        self.login_btn = Button(self.tab1, fg='#f8f8ff', width=10, bg='#475a6b',
                                font=('System', 12, 'bold'), text='SUBMIT', command=self.driver)
        self.move_data_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#475a6b', state=DISABLED,
                                    font=('System', 12, 'bold'), text='STORED DATA', command=lambda: self.change_tab(1))
        self.move_manager_btn = Button(self.tab1, fg='#f8f8ff', width=20, bg='#475a6b', state=DISABLED,
                                       font=('System', 12, 'bold'), text='PASSWORD MANAGER', command=lambda: self.change_tab(2))
        self.quit_program_btn = Button(self.tab1, fg='#f8f8ff', width=42, bg='#475a6b',
                                       font=('System', 12, 'bold'), text='QUIT PROGRAM', command=self.quit_program)

        self.login_btn.place(relx=0.74, rely=0.41)
        self.move_data_btn.place(relx=0.015, rely=0.65)
        self.move_manager_btn.place(relx=0.515, rely=0.65)
        self.quit_program_btn.place(relx=0.016, rely=0.8)

        # self.tab2
        self.data_frame = Frame(self.tab2, width=450, height=450, bg='#475a6b')
        self.data_frame.pack()

        self.data_label = Label(self.tab2, fg='#f8f8ff', text="PASSWORDS STORED", width=30,
                                font=('System', 14, 'bold'), bg='#475a6b')
        self.data_label.place(relx=0.15, rely=0.05)

        self.data_text = Text(self.tab2, font=('System', 12, 'bold'),
                              height=12, width=42, bg='#f8f8ff')  # change colour to lighter
        self.data_text.place(relx=0.075, rely=0.15)

        self.show_data_btn = Button(self.tab2, fg='#f8f8ff', width=19, height=1, font=(
            'System', 12, 'bold'), text=r'DISPLAY DATA', bg='#475a6b', command=self.show_data)
        self.manager_btn = Button(self.tab2, fg='#f8f8ff', width=19, height=1, font=(
            'System', 12, 'bold'), text='GO TO MANAGER', bg='#475a6b', command=lambda: self.change_tab(2))
        self.quit_prog_btn = Button(self.tab2, fg='#f8f8ff', width=39, height=1, font=(
            'System', 12, 'bold'), text='QUIT PROGRAM', bg='#475a6b', command=self.quit_program)

        self.show_data_btn.place(relx=0.06, rely=0.80)
        self.manager_btn.place(relx=0.51, rely=0.80)
        self.quit_prog_btn.place(relx=0.06, rely=0.90)

        # self.tab3

        self.manager_frame = Frame(self.tab3, width=450, height=450, bg='#475a6b')
        self.manager_frame.pack()

        self.manager_label = Label(self.tab3, fg='#f8f8ff', text="PASSWORDS MANAGER", width=30,
                                   font=('System', 14, 'bold'), bg='#475a6b')
        self.manager_label.place(relx=0.15, rely=0.03)

        self.guide = "Choose a command from below and follow the instructions."
        self.instructions_manager = Message(self.tab3, fg='#f8f8ff', text=self.guide, bg='#475a6b', width=450,
                                            font=('System', 12), justify=LEFT)
        self.instructions_manager.place(relx=0, rely=0.11)

        self.services_input = StringVar()
        self.services_input.set("Name of service.")
        self.services_entry = Entry(self.tab3, width=34, bg='#f8f8ff', textvariable=self.services_input, font=(
            'System', 12, 'bold'), state='disabled')
        self.submit_service = Button(self.tab3, fg='#f8f8ff', width=8, text='SUBMIT', bg='#475a6b', state='disabled', font=(
            'System', 12, 'bold'), command=lambda: self.submit_btn(0))
        self.services_entry.place(relx=0.02, rely=0.30)
        self.submit_service.place(relx=0.76, rely=0.29)

        self.username_input = StringVar()
        self.username_input.set("Username.")
        self.username_entry = Entry(self.tab3, width=34, bg='#f8f8ff', textvariable=self.username_input, font=(
            'System', 12, 'bold'), state='disabled')
        self.submit_username = Button(self.tab3, fg='#f8f8ff', state='disabled', width=8, text='SUBMIT', bg='#475a6b', font=(
            'System', 12, 'bold'), command=lambda: self.submit_btn(1))
        self.username_entry.place(relx=0.02, rely=0.40)
        self.submit_username.place(relx=0.76, rely=0.39)

        self.password_input = StringVar()
        self.password_input.set("Password.")
        self.password_entry = Entry(self.tab3, width=34, bg='#f8f8ff', textvariable=self.password_input, font=(
            'System', 12, 'bold'), state='disabled')
        self.submit_password = Button(self.tab3, fg='#f8f8ff', state='disabled', width=8, text='SUBMIT', bg='#475a6b', font=(
            'System', 12, 'bold'), command=lambda: self.submit_btn(2))
        self.password_entry.place(relx=0.02, rely=0.50)
        self.submit_password.place(relx=0.76, rely=0.49)

        self.access_btn = Button(self.tab3, fg='#f8f8ff', width=20, text='ACCESS DATABASE', bg='#475a6b', font=(
            'System', 12, 'bold'), command=self.access_passwords)
        self.gen_btn = Button(self.tab3, fg='#f8f8ff', width=20, text='GENERATE PASSWORD', bg='#475a6b', font=(
            'System', 12, 'bold'), command=self.generate_password)
        self.store_btn = Button(self.tab3, fg='#f8f8ff', width=20, text='STORE PASSWORD', bg='#475a6b', font=(
            'System', 12, 'bold'), command=self.store_password)
        self.delete_btn = Button(self.tab3, fg='#f8f8ff', width=20, text=r'DELETE PASSWORD', bg='#475a6b', font=(
            'System', 12, 'bold'), command=self.delete_password)

        self.access_btn.place(relx=0.015, rely=0.62)
        self.gen_btn.place(relx=0.515, rely=0.62)
        self.store_btn.place(relx=0.015, rely=0.74)
        self.delete_btn.place(relx=0.515, rely=0.74)

        self.quit_btn = Button(self.tab3, fg='#f8f8ff', width=20, text='QUIT PROGRAM', bg='#475a6b', font=(
            'System', 12, 'bold'), command=self.quit_program)
        self.data_tab_btn = Button(self.tab3, fg='#f8f8ff', width=20, text='STORED DATA', bg='#475a6b', font=(
            'System', 12, 'bold'), command=lambda: self.change_tab(1))

        self.data_tab_btn.place(relx=0.015, rely=0.86)
        self.quit_btn.place(relx=0.515, rely=0.86)

        self.tabs.tab(1, state='disabled')
        self.tabs.tab(2, state='disabled')

        self.master.bind('<Return>', self.reset_manager)

    def reset_manager(self, event=None):
        # resets the manager
        self.guide = "Choose a command from below and follow the instructions."
        self.instructions_manager.configure(text=self.guide)
        self.service, self.user_name, self.passw = '', '', ''
        self.services_input.set("Name of service.")
        self.username_input.set("Username.")
        self.password_input.set("Password.")
        self.services_entry.configure(state='disabled')
        self.username_entry.configure(state='disabled')
        self.password_entry.configure(state='disabled')
        self.submit_service["state"] = DISABLED
        self.submit_username["state"] = DISABLED
        self.submit_password["state"] = DISABLED

    def initialise_command(self, pass_enable):
        # enables the necessary buttons and entries
        self.submit_service["state"] = NORMAL
        self.submit_username["state"] = NORMAL
        self.services_entry.configure(state='normal')
        self.username_entry.configure(state='normal')
        if pass_enable:
            self.password_entry.configure(state='normal')
            self.submit_password["state"] = NORMAL

    def driver(self):
        # checks if the password is the same as the admin password
        # it then enables all the other
        input_pass = self.login_text.get()
        if input_pass == self.admin_password:
            self.tabs.tab(1, state='normal')
            self.tabs.tab(2, state='normal')
            self.login_text.set("Welcome to your safe.")
            self.login_btn['state'] = DISABLED
            self.move_data_btn['state'] = NORMAL
            self.move_manager_btn['state'] = NORMAL
            self.login_entry.configure(state='disabled')
        else:
            self.login_text.set("Wrong password. Try again.")

    def fetch_all_data(self):
        # gets the data from the SQL Database
        # used to validate input for the access and delete password
        self.cur.execute("SELECT service, username FROM User_Info ORDER BY service ASC")
        self.rows = self.cur.fetchall()
        if not self.rows:
            return False
        else:
            return True

    def show_data(self):
        # update the 2nd tab with all the data that is fetched
        # orders everything and then print
        self.data_text.configure(state='normal')
        self.data_text.delete('1.0', END)
        data_to_show = self.fetch_all_data()
        str_to_show = ''
        if data_to_show:
            for c, (s, u) in enumerate(self.rows):
                str_to_show += '{:02}. {} ; {}\n'.format(c+1, s, u)
        else:
            str_to_show = 'There is no saved data. Save or create \npasswords through the manager on the next \ntab.'
        self.data_text.insert(INSERT, str_to_show)
        self.data_text.configure(state='disabled')

    def check_if_valid(self):
        # checks if combination of username and service is valid
        data_present = self.fetch_all_data()
        if data_present:
            if (self.service, self.user_name) in self.rows:
                return True
        return False

    def get_hash_key(self):
        # generate the foreign key from username and service
        hash = sha256(self.service.lower().encode('utf-8')+self.user_name.lower().encode('utf-8') +
                      self.admin_password.lower().encode('utf-8')).hexdigest()
        self.hash_key = hash[:15]

    def access_passwords(self):
        self.guide = 'Enter the service name and username. The password will be fetched and copied. Hit enter when you are done.'
        self.instructions_manager.configure(text=self.guide)
        self.initialise_command(False)
        if self.service and self.user_name:
            self.submit_service["state"] = DISABLED
            self.submit_username["state"] = DISABLED
            self.services_entry.configure(state='disabled')
            self.username_entry.configure(state='disabled')
            valid_combo = self.check_if_valid()
            if valid_combo:
                self.get_hash_key()
                self.cur.execute(
                    'SELECT password FROM Passwords WHERE hash_key = ?', (self.hash_key,))
                self.passw = self.cur.fetchone()[0]
                self.copy_password()
                self.guide = 'Password copied. Hit enter to continue.'
            else:
                self.passw = "Error: combination does not exist."
                self.guide = "You have typed the wrong service name/username or there is no data stored. Hit enter and try again."
            self.instructions_manager.configure(text=self.guide)
            self.password_input.set(self.passw)

        else:
            self.master.after(100, self.access_passwords)

    def check_if_exists(self):
        # avoids duplicates as I cannot update a unique constraint onto the table now
        self.cur.execute("SELECT username from User_Info WHERE service = ?", (self.service,))
        try:
            username_saved = self.cur.fetchone()[0]
            if username_saved == self.user_name:
                self.cur.execute(
                    "DELETE from User_Info where service = ? and username = ?", (self.service, self.user_name))
        except:
            return

    def create_password(self):
        # generates a password based on number of chars and special chars
        # reinitialises both
        char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        self.passw = ''.join(random.sample(char_list, 16))

    def generate_password(self):
        # gets the service name and username
        # displays the new password
        self.initialise_command(False)
        self.guide = "Enter the service and username, a random password will be generated, stored and copied."
        self.instructions_manager.configure(text=self.guide)
        if self.service and self.user_name:
            self.create_password()
            self.get_hash_key()
            self.check_if_exists()
            self.cur.execute(
                'INSERT OR REPLACE INTO User_Info(service,username) VALUES (?,?)', (self.service, self.user_name,))
            self.cur.execute(
                'INSERT OR REPLACE INTO Passwords(hash_key, password) VALUES (?,?)', (self.hash_key, self.passw))
            self.conn.commit()
            self.password_input.set(self.passw)
            self.copy_password()
            self.guide = 'Password generated and copied. Hit enter to continue.'
            self.instructions_manager.configure(text=self.guide)
        else:
            self.master.after(100, self.generate_password)

    def delete_password(self):
        # enables password
        # gets the username and service name and then checks if true
        # if it is true then it deletes it
        # disables all the buttons
        self.guide = 'Enter the service name, username and password that you wish to delete.'
        self.instructions_manager.configure(text=self.guide)
        self.initialise_command(True)
        if self.service and self.user_name and self.passw:
            check_combo = self.check_if_valid()
            if check_combo:
                self.get_hash_key()
                self.cur.execute(
                    'SELECT password FROM Passwords WHERE hash_key = ?', (self.hash_key,))
                actual_passw = self.cur.fetchone()[0]
                if self.passw == actual_passw:
                    self.cur.execute('DELETE FROM Passwords WHERE hash_key = ? and password = ?',
                                     (self.hash_key, self.passw,))
                    self.cur.execute('DELETE FROM User_Info WHERE service = ? and username = ?',
                                     (self.service, self.user_name,))
                    self.guide = "Successfully deleted. Hit enter to continue."
                    self.instructions_manager.configure(text=self.guide)
                    self.conn.commit()
                else:
                    self.guide = 'Error: The combination does not exist. Hit enter to try again.'
                    self.instructions_manager.configure(text=self.guide)
        else:
            self.master.after(100, self.delete_password)

    def store_password(self):
        # enables password
        # gets username, password and service
        self.guide = "Enter service name, username and password you wish to store below."
        self.instructions_manager.configure(text=self.guide)
        self.initialise_command(True)
        if self.service and self.user_name and self.passw:
            self.get_hash_key()
            self.check_if_exists()
            self.cur.execute(
                'INSERT OR REPLACE INTO User_Info(service,username) VALUES (?,?)', (self.service, self.user_name,))
            self.cur.execute(
                'INSERT OR REPLACE INTO Passwords (hash_key, password) VALUES (?,?)', (self.hash_key, self.passw,))
            self.conn.commit()
            self.guide = "The database has been updated. Click Enter to choose from the commands again and continue."
            self.instructions_manager.configure(text=self.guide)
        else:
            self.master.after(100, self.store_password)

    def randomize_order(self):
        # randomizes the order of the data stored in the DATABASE
        self.cur.execute("SELECT service, username FROM User_Info")
        data = self.cur.fetchall()
        random.shuffle(data)
        self.cur.execute("DELETE FROM User_Info")
        for row in data:
            self.cur.execute('INSERT INTO User_Info(service,username) VALUES (?,?)',
                             ((row[0], row[1],)))
        self.conn.commit()

    def copy_password(self):
        # copies it onto the clipboard
        pyperclip.copy(self.passw)

    def submit_btn(self, n):
        if n == 0:
            self.service = self.services_input.get()
        elif n == 1:
            self.user_name = self.username_input.get()
        else:
            self.passw = self.password_input.get()

    def change_tab(self, n):
        # changes the tab accordingly
        self.tabs.select(n)

    def quit_program(self):
        # randomizes the order and then quits the program
        self.randomize_order()
        sys.exit()


def main():
    root = Tk()
    pass_manager = PasswordManagerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
