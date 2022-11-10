# Part 2A:

Structure: In general, the code seems completely messy and unstructured. Therefore, it is harder to find bugs (e.g. logical bugs) and security holes. Moreover, the programmer stopped writing comments, what is part of an important feature of a well written code. Our suggestion is to split the code in different files to improve the readability. In Addition, all import statements should be written on the top of the file and not somewhere in the middle. 

It is definitely needed to remove not used methods and domains. For example, we think that “\coffee” is not needable in a messaging app. Additionally, it is possible to call “\announcements”, however, there is in no possibility to create announcements at all. Therefore, we think that this function and the included database is not necessary. Furthermore, “/favicon.ico” and “/favicon.png” is also not used in the message program. 

The usernames, the passwords and the tokens are written in the file in clear text. Moreover, there is no encryption for the passwords and tokens. 
Furthermore, the code includes a todo for checking the password to the corresponding username, and it is still not finished. Therefore, it is possible to login, if you know the correct username. The corresponding password is here not needed. 

 
The user has the possibility to the all sent messages from the other users. Moreover, it does not make any sense for us that the user can change the “From” field because in this case he or she sends the message with the wrong name. Therefore, Bob can send a message to Alice over the name Chloe and Alice will think, that Chloe sent the message to her. 


# Part 2B  :

## Description

The design created enhanced the security of the messaging system by setting clear restrictions on what a user could do. This is made by first requesting the user to log in and comparing their password with the one stored in the "login_data" database. After logging in, the user can send new messages, retrieve a specific message using the message ID, show all messages that the user has received, and reply to a message that the user has either sent or received before. 

Messages are also stored in the database in 2 tables, the first table would include the message ID, sender's username, timestamp, the ID of the original message the which this message is replying, and the context of the message. The second table includes the message ID and a list of receivers of the users received this message.

There are 3 buttons and 4 text bars in the design. The "show message" button will show all information related to the message of the ID written in the "Show MID" text bar. The "send" button creates a new message and sends it to all receivers written in the "Receiver" text bar. It also links this message to a previous message if there is an id written in the "Reply ID" text bar. Finally, the "Show all" button prints down a list of all the information related to all the messages received by the user. 

## Assumptions and Techincal Details 

1- Multiple receivers are separated with commas and that's why a username can only include letters, numbers, and underscore.

2- Show all will only show all messages received by the logged-in user 

3- Reply ID allows the user to reply to a specific message that is either sent by them or sent to them. 

4- Before showing the result of the search for a message, a line showing the format of the result is printed 



## How to test 

1- Open terminal 

2-Install all flask libraries using commands mentioned here: https://git.app.uib.no/inf226/22h/login-server

3- Clone all files from github (command: git clone (the link ))

4-run using the command: flask run 

5-Connect to http://localhost:5000/

6-Login as one of the users "alice" (password: "password123") or "bob" (password: "bananas")


## Answers to Questions 

### Question 1

#### Who might attack the application? 
An attacker could be for example a person who is interested in confidential chats between other users. Moreover, the attacker could be a person who wants to hide some sent messages by deleting the databases. Furthermore, the attacker could be a person who wants to pretend to be someone else. 

#### What can an attacker do? What damage could be done? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?

The previous application included various attack points due to the lack of security. Below, we have split the possible attacks in the CIA-Triad. 

##### Confidentiality
Starting with the lack of a logging-in check system, anyone could have attacked the application since everyone was able to log in when they only knew the username. There was no checking of the password. We found in the code a "Todo Line" for implementing the password check. This harms the confidentiality of the application. To solve this security leak, we implemented a logging function and added a user database because the password with the dependent username was hardcoded in the given code. Moreover, the password was not encrypted. Therefore, we added an encryption mechanism that includes salting and encrypting the password with "sha256". 
Furthermore, in the old application, a user could view all sent messages of all users. Therefore, we limited the viewed messages to only the messages received from the current user. 

##### Integrity
The old application offers the possibility to change the sender's name. Therefore, an attacker could pretend to be someone else. We solved this leak of security by limiting the sender to the current user. Moreover, we removed the sender field for the user. 
Moreover, a possible attacker was able to insert new elements into the database by SQL injections. We prevented SQL injections with prepared statements. 

##### Availability
After testing the old application, we realized that SQL injections were possible. With an SQL injection, the attacker was able to delete all databases. We have mentioned above the solution we used to prevent SQL injections. 

### Question 2

#### What are the main attack vectors for the application?
The input fields available in the application are the main attack vectors for the application. Moreover, the URL bar is a potential attack vector because the attacker could perform requests that he or she is not allowed to.
Since we implemented sessions, an attacker could steal the session data to pretend to be a certain user. In addition, a thief of the device with the running application could use as well the session data of the user.
 
 
### Question 3
#### What should we do (or what have you done) to protect against attacks?
Due to the fact, that the input fields are mandatory in our application, we were not able to delete them without destroying the main function of the application :D
However, we restricted what a user can write into these fields based on the functionality of each field. For example, we changed the search field to a search by ID field. Therefore, the field only accepts numbers. Furthermore, as mentioned above, we also secured our input fields against SQL injections. 
In addition, we make sure that only logged-in users can perform requests by the URL bar and that in our application are no URLs that can execute malicious actions. 

 
### Question 4
#### What is the access control model?
Since our program is not that big and we do not have different roles, we decided to use access control lists as our access control model. Our access control model subjects are the users, the objects are messages, and the actions are sending and reading messages that belong to the subject (user). We do not distinguish between different roles. 

### Question 5 
#### How can you know that your security is good enough? 
Good question. Is this even possible? How should I know that someone is not sitting right now in the cellar and discovers a new attacker way? 
However, we made our best to secure our application based on the knowledge we have about the current and most popular attacker ways. 
In general, security is a process and not a state. It is a concern, not a feature, meaning that the whole process of developing software should be aware of security, it should not only be seen as a feature that you add afterward but it should be the main core of the design.
