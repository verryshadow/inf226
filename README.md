Part 2A:

Structure: In general, the code seems completely messy and unstructured. Therefore, it is harder to find bugs (e.g. logical bugs) and security holes. Moreover, the programmer stopped writing comments, what is part of an important feature of a well written code. Our suggestion is to split the code in different files to improve the readability. In Addition, all import statements should be written on the top of the file and not somewhere in the middle. 

It is definitely needed to remove not used methods and domains. For example, we think that “\coffee” is not needable in a messaging app. Additionally, it is possible to call “\announcements”, however, there is in no possibility to create announcements at all. Therefore, we think that this function and the included database is not necessary. Furthermore, “/favicon.ico” and “/favicon.png” is also not used in the message program. 

The usernames, the passwords and the tokens are written in the file in clear text. Moreover, there is no encryption for the passwords and tokens. 
Furthermore, the code includes a todo for checking the password to the corresponding username, and it is still not finished. Therefore, it is possible to login, if you know the correct username. The corresponding password is here not needed. 

 
The user has the possibility to the all sent messages from the other users. Moreover, it does not make any sense for us that the user can change the “From” field because in this case he or she sends the message with the wrong name. Therefore, Bob can send a message to Alice over the name Chloe and Alice will think, that Chloe sent the message to her. 

