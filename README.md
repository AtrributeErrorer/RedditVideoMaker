# RedditVideoMaker
A python script that automatically makes reddit videos

note; im new to coding, and it's probably not even perfect or efficient
Important Note: The Minecraft Gameplay file will not be provided, I recommend downloading this: https://www.youtube.com/watch?v=u7kdVe8q5zs

However, if you want to use your own, you must have it in the same folder as the reddit bot, and make sure the video is named to "Minecraft Parkour Gameplay No Copyright.mp4"

You need visual studio code and python to run the script.

Download the file, put it in a folder with no other items inside of it, and open it using visual studio code, (make sure you have also opened the folder in visual studio explorer), after doing this, open the console (control + ~) and paste in these one after another:

python -m pip install praw

python -m pip install pyttsx3

python -m pip install selenium

python -m pip install moviepy

python -m pip install ffmpeg-python

python -m pip install pillow

Once installed, scroll down a bit to main(), and replace the username with your reddit username, password, client id and client secret, the default subreddit it checks is r/askreddit, with 1 submission and 3 comments.
