from hashlib import sha256
import sqlite3
import random
import string
import time
import sys
import pyperclip


class ManagePasswords:

    def __init__(self):
        self.conn = sqlite3.connect("password_database.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Passwords (hash_key text primary key, password text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS User_Info (service text, username text)")
        self.admin_password = 'Barrys2e5!'
        self.service = ''
        self.user_name = ''
        self.passw = ''
        self.hash_key = ''
        self.driver()

    def create_password(self):
        print("Enter service name.")
        self.service = input()
        print("Enter username.")
        self.user_name = input()
        print("Enter number of characters as a digit, recommended 16.")
        while True:
            num_chars = input()
            if num_chars.isalnum():
                print("Do you want special characters, recommened yes.")
                sp = input()
                special_chars = True if 'y' in sp.lower() else False
                break
            else:
                print("Please enter valid number in digits.")
                continue
        char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits
        if special_chars:
            char_list += string.punctuation
        self.passw = ''.join(random.sample(char_list, int(num_chars)))
        time.sleep(0.25)
        print("Generated password is {}, now storing in database and copying to clipboard.".format(self.passw))
        time.sleep(1)
        self.get_hash_key()
        self.store_password()
        self.copy_password()

    def get_hash_key(self):
        # generate hashkey using the service, username and admin password as a salt
        hash = sha256(self.service.lower().encode('utf-8')+self.user_name.lower().encode('utf-8') +
                      self.admin_password.lower().encode('utf-8')).hexdigest()
        self.hash_key = hash[:15]

    def input_password(self):
        # add password and pass_key to sql database
        # add the service and username as well
        print("-"*20)
        print("Enter service name")
        self.service = input()
        print()
        print("Enter username")
        self.user_name = input()
        print()
        print("Enter password to store (case sensitive)")
        self.passw = input()
        self.get_hash_key()
        self.store_password()

    def store_password(self):
        # stores password after generating or user inputted
        self.cur.execute(
            'INSERT OR REPLACE INTO Passwords (hash_key, password) VALUES (?,?)', (self.hash_key, self.passw,))
        self.cur.execute(
            'INSERT OR REPLACE INTO User_Info (service,username) VALUES (?,?)', (self.service, self.user_name,))
        print("Securely stored onto database.")
        self.conn.commit()

    def randomize_order(self):
        # randomizes the order of user info stored in the table
        self.cur.execute("SELECT service, username FROM User_Info")
        data = self.cur.fetchall()
        random.shuffle(data)
        self.cur.execute("DELETE FROM User_Info")
        for row in data:
            self.cur.execute('INSERT INTO User_Info(service,username) VALUES (?,?)',
                             ((row[0], row[1],)))
        self.conn.commit()

    def retrieve_password(self):
        # get hash key and then fetch from sql
        passw_present = self.show_services()
        if not passw_present:
            print("You cannot access passwords if there aren't any.")
            return
        else:
            time.sleep(0.5)
            while True:
                print("Enter name of the service you wish to access.")
                self.service = input()
                print()
                print("Enter username for the service.")
                self.user_name = input()
                print()
                if (self.service, self.user_name) in self.rows:
                    break
                else:
                    print("No such combination of service and username exists, please re-enter.")
                    print()
                    continue
            self.get_hash_key()
            self.cur.execute('SELECT password from Passwords WHERE hash_key = ?', (self.hash_key,))
            self.passw = self.cur.fetchone()[0]
            time.sleep(0.25)
            print("Password for {} and username {} is {}".format(
                self.service, self.user_name, self.passw))
            self.copy_password()

    def show_services(self):
        # called by retrieve password
        # get all the services and then display
        self.cur.execute("SELECT service, username FROM User_Info ORDER BY service ASC")
        self.rows = self.cur.fetchall()
        if not self.rows:
            print("No passwords to display.")
            return False
        else:
            print("-"*20)
            print("Services and Usernames:")
            for i, (ser, user) in enumerate(self.rows):
                i += 1
                print('{:02}. Service: {}, Username: {}.'.format(i, ser, user))
                time.sleep(0.1)
            print()
            return True

    def copy_password(self):
        # copy to clipboard using pyperclip
        pyperclip.copy(self.passw)
        time.sleep(0.5)
        print("Password copied to clipboard.")
        print()

    def delete_password(self):
        passw_present = self.show_services()
        if not passw_present:
            print("You cannot delete a password if there aren't any.")
            return
        else:
            while True:
                print("Enter name of service you wish to delete.")
                self.service = input()
                print()
                print("Enter username for the service.")
                self.user_name = input()
                print()
                if (self.service, self.user_name) in self.rows:
                    break
                else:
                    print("No such combination of service and username exists, please re-enter.")
                    print()
                    continue
            self.get_hash_key()
            self.cur.execute('SELECT password from Passwords WHERE hash_key = ?', (self.hash_key,))
            self.passw = self.cur.fetchone()[0]
            while True:
                print("Enter password of service to delete.")
                pword = input()
                if pword == self.passw:
                    break
                    time.sleep(0.25)
                else:
                    print("Incorrect password, please re-enter.")
            self.cur.execute('DELETE FROM Passwords WHERE hash_key = ? and password = ?',
                             (self.hash_key, self.passw,))
            self.cur.execute('DELETE FROM User_Info WHERE service = ? and username = ?',
                             (self.service, self.user_name,))
            print("Deleted record.")

    def quit_program(self):
        self.randomize_order()
        print("Saving changes to database and quitting.")
        self.conn.close()
        time.sleep(0.5)
        sys.exit()

    def driver(self):
        print("Please enter the password.")
        while True:
            ad_pass = input()
            if ad_pass == self.admin_password:
                break
            else:
                print("Incorrect password, try again.")
                continue
        print("-"*20)
        print("Password Manager")
        while True:
            print('-'*20)
            print("Commands")
            print("sp: Store or Update an old password.")
            print("ac: Access the database and retrieve a saved password.")
            print("gp: Generate a password and store it.")
            print("dp: Delete a password from the record.")
            print("qt: Quit program.")
            print("-"*20)
            print("Please enter command")
            cmd = input()
            if cmd not in ['sp', 'ac', 'gp', 'qt', 'dp']:
                print("Invalid command, please re-enter.")
                continue
            else:
                if cmd == 'sp':
                    self.input_password()
                elif cmd == 'ac':
                    self.retrieve_password()
                elif cmd == 'gp':
                    self.create_password()
                elif cmd == 'dp':
                    self.delete_password()
                else:
                    self.quit_program()
            print("Hit enter to choose another command.")
            delay = input()


def main():
    try:
        obj = ManagePasswords()
    except KeyboardInterrupt:
        print("Exiting.")
        time.sleep(0.5)
        sys.exit()


if __name__ == '__main__':
    main()
