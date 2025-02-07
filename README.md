# RedditVideoMaker
A python script that automatically makes redditvideos

note; im new to coding, and it's probably not even perfect or efficient


You need visual studio code and python to run the script.

Download the file, put it in a folder with no other items inside of it, and open it using visual studio code, (make sure you have also opened the folder in visual studio explorer), after doing this, open the console (control + ~) and paste in these one after another:
python -m pip install praw
python -m pip install pyttsx3
python -m pip install selenium
python -m pip install moviepy
python -m pip install ffmpeg-python
python -m pip install pillow

Once installed, scroll down a bit to main(), and replace the username with your reddit username, password, client id and client secret, the default subreddit it checks is r/askreddit, with 1 submission and 3 comments.
