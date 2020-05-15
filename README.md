# Outline:
- An all-in-one password system to rule them all. It stores your passwords in an SQL database along with the services they access through  quasi-relational tables which use a hash (via the hashlib module) as the primary key and an invisible foreign key. The system stores your old passwords and generates new passwords, allowing to access all your login credentials securely via one single master password. A more detailed explanation lies below.

# Purpose:
- I had been desperately looking for a minimal password organiser and could not find any that offered the degree of security and ease I was looking for and therefore I built my own. The build was tremendously fun and introduced me to the world of cryptography through hashing and salting. I was also able to use my knowledge of SQL and relational databases in order to arrive at a perfect blend of security and ease of use using my primary key solution.

# Description:
- Understanding this project becomes immensely easier once the fundamental schema of the database is understood. The database houses 2 tables; one for passwords and a primary key and one for the service and username that the password accesses.
- Even though there is a primary key in this set-up, there surprisingly isn't any foreign key to point to the primary key but the foreign key is actually the combination of the service name, username and constant admin password (as a pseudo-salt) that is hashed, using a secure hashing algorithm (sha256) and the first 15 characters are logged in the passwords database as the primary key. This hashing is done by the get_hash_key method.

    ```python
    def get_hash_key(self):
    		hash = sha256(self.service.lower().encode('utf-8')+self.user_name.lower().encode('utf-8')
    									+ self.admin_password.lower().encode('utf-8')).hexdigest()
    		self.hash_key = hash[:15]
    ```
    
- The encoding helps ensure the same hash is generated when we try to access the password.
- The program makes it so that a user can choose to store an old password, create a new one, access all stored passwords or delete an old password.
- Each call takes in the service name and username, validates them when necessary and retrieves the password from the data base by generating the hash_key for the service and username as shown above and then querying the database where the primary key is the same as the first 15 characters of this hash key.
- Therefore the foreign key is generated for at each call and isn't stored anywhere adding immense security.
- Maintaining the user login info, service and username means that there is a potential threat as someone can brute force all the possible passwords and the possible login credentials but this threat is exponentially minimized as the password manager is used more as the number of possible combinations (the cartesian product of the service,username and the password) increases greatly.
- The password generator randomly chooses a user inputted number of characters from upper and lowercase letters, numbers and special characters(optional).
- The rest of the characters do as they are named.
- Built on the foundations of OOP, the program places modularity in high regard and therefore most methods are reused within the program.
