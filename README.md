Part 2A:

Structure: In general, the code seems completely messy and unstructured. Therefore, it is harder to find bugs (e.g. logical bugs) and security holes. Moreover, the programmer stopped writing comments, what is part of an important feature of a well written code. Our suggestion is to split the code in different files to improve the readability. In Addition, all import statements should be written on the top of the file and not somewhere in the middle. 

It is definitely needed to remove not used methods and domains. For example, we think that “\coffee” is not needable in a messaging app. Additionally, it is possible to call “\announcements”, however, there is in no possibility to create announcements at all. Therefore, we think that this function and the included database is not necessary. Furthermore, “/favicon.ico” and “/favicon.png” is also not used in the message program. 

The usernames, the passwords and the tokens are written in the file in clear text. Moreover, there is no encryption for the passwords and tokens. 
Furthermore, the code includes a todo for checking the password to the corresponding username, and it is still not finished. Therefore, it is possible to login, if you know the correct username. The corresponding password is here not needed. 

 
The user has the possibility to the all sent messages from the other users. Moreover, it does not make any sense for us that the user can change the “From” field because in this case he or she sends the message with the wrong name. Therefore, Bob can send a message to Alice over the name Chloe and Alice will think, that Chloe sent the message to her. 


Part 2B  :

Description

   The design created enhanced the security of the messaging system by setting clear restrictions on what a user could do. This is made by first requesting the user to log in and comparing their password with the one stored in the "login_data" database. After logging in, the user can send new messages, retrieve a specific message using the message ID, show all messages that the user has received, and reply to a message that the user has either sent or received before. 

  Messages are also stored in the database in 2 tables, the first table would include the message ID, sender's username, timestamp, the ID of the original message the which this message is replying, and the context of the message. The second table includes the message ID and a list of receivers of the users received this message.

  There are 3 buttons and 4 text bars in the design. The "show message" button will show all information related to the message of the ID written in the "Show MID" text bar. The "send" button creates a new message and sends it to all receivers written in the "Receiver" text bar. It also links this message to a previous message if there is an id written in the "Reply ID" text bar. Finally, the "Show all" button prints down a list of all the information related to all the messages received by the user. 

Assumptions and Techincal Details  :

1- Multiple receivers are separated with commas and that's why a username can only include letters, numbers, and underscore.

2- Show all will only show all messages received by the logged-in user 

3- Reply ID allows the user to reply to a specific message that is either sent by them or sent to them. 

4- Before showing the result of the search for a message, a line showing the format of the result is printed 

How to test (make sure to install all flask libraries before starting) : 
1- Open terminal 

2- Clone all files from github (command : git clone (the link ))

3-run using the command : flask run 

4-Connect to http://localhost:5000/ 


Answers to Questions : 

1- Who might attack the application? What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?

   was able to log in if only knew username 
2- What are the main attack vectors for the application?

 We have input fields , tried making them more secure (limiting what to be written)
 
 
3- What should we do (or what have you done) to protect against attacks?
 SQL ingection : check password , encrypt password 
 
4- What is the access control model?

5- How can you know that you security is good enough? 
