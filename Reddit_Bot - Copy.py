#You must installed these dependencies to run this file.
import praw #python -m pip install praw
import pyttsx3 #python -m pip install pyttsx3
import selenium #python -m pip install selenium
import moviepy #python -m pip install moviepy
#python -m pip install ffmpeg-python
from PIL import Image #python -m pip install pillow
from io import BytesIO
from praw.models import MoreComments
engine = pyttsx3.init()
from moviepy import *
import numpy as np
import random
import os
import glob
import re
import time as t



from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
def ScreenShot(elementName, url, submissionCounter, commentCounter, replyCounter):
    if(commentCounter == 0 and replyCounter == 0):
        driver = webdriver.Firefox()
        driver.fullscreen_window()
        driver.get(url)
        container = driver.find_element(By.ID, elementName)
        container.screenshot("title " + str(submissionCounter) + " comment " + str(commentCounter) + " reply " + str(replyCounter) + ".png")
        driver.quit()
    else:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.fullscreen_window()
        driver.get(url)
        def get_scroll_dimension(axis):
              return driver.execute_script(f"return document.body.parentNode.scroll{axis}")
        widthPage = get_scroll_dimension("Width")
        heightPage = get_scroll_dimension("Height")
        driver.set_window_size(widthPage, heightPage)
        driver.implicitly_wait(10)
        container = driver.find_element(By.ID, elementName)
        location = container.location
        size = container.size
        png = driver.get_screenshot_as_png()
        driver.quit()
        print(f"Location: {location}, Size: {size}")

        im = Image.open(BytesIO(png))
        
        left = location['x'] - 40
        top = location['y'] - 50
        right = location['x'] + size['width']
        bottom = location['y'] + size['height'] + 30
        
        im = im.crop((left, top, right, bottom))
        im.save("title " + str(submissionCounter) + " comment " + str(commentCounter) + " reply " + str(replyCounter) + ".png")
        # im.close()

        
limitReached = False
fps = 24
time = 0 #Don't change this
clips = []
maximumTimeSeconds = 60 #Max time you want your video to be
def main():
    global limitReached
    username = "your username"
    password = "your password"
    client_id = "your client id"
    client_secret = "your client secret"
    howManySubmissions = 1
    howManyComments = 3
    howManyReplies = 0 #Probably don't do this, i'm not inclined to fix it (uni work)
    
    

    reddit_instance = praw.Reddit(
        client_id = client_id, 
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent = "test_bot")

    subreddit = reddit_instance.subreddit("AskReddit")
    top_submissions = subreddit.hot()
    submissionCounter = 0
    replyBodyCheck = ""
    commentBodyCheck = ""
    replyCounter = 0
    for submission in top_submissions:
        if(limitReached == False):
            url = submission.url
            commentCounter = 0
            submissionCounter += 1
            engine.save_to_file(submission.title, "title " + str(submissionCounter) + " comment " + str(commentCounter) + " reply " + str(replyCounter) + ".mp3")
            engine.runAndWait()
            ScreenShot("t3_" + submission.id, url, submissionCounter, commentCounter, replyCounter)
            clips.append(MakeRedditVideo(submissionCounter, commentCounter, replyCounter))
            for comment in submission.comments:
                replyCounter = 0
                try:
                    if comment.body != commentBodyCheck and len(comment.body.split()) <= 100 and commentCounter <= howManyComments:
                        commentCounter += 1
                        engine.save_to_file(comment.body,"title " + str(submissionCounter) + " comment " + str(commentCounter) + " reply " + str(replyCounter) + ".mp3")
                        engine.runAndWait()
                        commentBodyCheck = comment.body
                        ScreenShot("t1_" + comment.id + "-comment-rtjson-content", url, submissionCounter, commentCounter, replyCounter)
                        clips.append(MakeRedditVideo(submissionCounter, commentCounter, replyCounter))
                        for replies in comment.replies:
                            try: 
                                if comment.replies != replyBodyCheck and len(replies.body.split()) <= 100 and replyCounter != howManyReplies and replyCounter < howManyComments:
                                        if isinstance(replies, MoreComments):
                                            continue
                                        else:
                                            replyCounter += 1
                                            replyBodyCheck = replies.body
                                            engine.save_to_file(replies.body,"title " + str(submissionCounter) + " comment " + str(commentCounter) + " reply " + str(replyCounter) + ".mp3")
                                            engine.runAndWait()
                                            ScreenShot("t1_" + replies.id + "-comment-rtjson-content", url, submissionCounter, commentCounter, replyCounter)
                                            clips.append(MakeRedditVideo(submissionCounter, commentCounter, replyCounter))
                                            if replyCounter == howManyReplies:
                                                break
                            except AttributeError:
                                print("ATTRIBUTE_ERROR (Ignore)")
                                replyCounter = howManyReplies
                            except:
                                replyCounter = replyCounter
                except AttributeError:
                    print("ATTRIBUTE_ERROR (Ignore)")
                    commentCounter += 1
                except:
                    commentCounter = commentCounter
                if(howManyComments == commentCounter):
                    break
            if(howManySubmissions == submissionCounter):
                break
        else:
            break

    



def MakeRedditVideo(submissionCount, commentCount, replyCount):
    global time
    global limitReached
    audio = AudioFileClip(f"title {submissionCount} comment {commentCount} reply {replyCount}.mp3")
    if (time + audio.duration) < maximumTimeSeconds:
        image = ImageClip(f"title {submissionCount} comment {commentCount} reply {replyCount}.png").with_duration(audio.duration)
        image = image.with_effects([vfx.Resize(width=1080)])  #, height = 245
        time += audio.duration
        video = image.with_audio(audio)
        video.write_videofile(f"title {submissionCount} comment {commentCount} reply {replyCount}.mp4", fps=fps)
        return (f"title {submissionCount} comment {commentCount} reply {replyCount}.mp4")
    else:
        limitReached = False
        print("TIME LIMIT REACHED")
        return


def finalizeClips(clips):
    global fps
    global time
    filtered_list = [item for item in clips if item is not None]
    clips = filtered_list
    video = VideoFileClip("Minecraft Parkour Gameplay No Copyright.mp4")
    randomnumber = random.randint(0, int(video.duration - time))
    video = video.subclipped(randomnumber, randomnumber + time)
    resized_video = video.resized(height=1920)
    cropped_video = resized_video.cropped(x_center=resized_video.size[0]/2, width=1080, height=1920)
    MinecraftCropped = CompositeVideoClip([cropped_video])
    MinecraftCropped.write_videofile('trimmed_video.mp4', threads=8, preset="ultrafast", fps = fps)
    clips.insert(0, ("trimmed_video.mp4"))
    currentDuration = 0
    for i in range(1,len(clips)):
        temp1 = VideoFileClip(clips[0])
        temp2 = VideoFileClip(clips[0+i])
        temp2 = temp2.with_start(currentDuration)
        final_export = CompositeVideoClip([temp1, temp2.with_position("center")]) #.with_position("center")
        final_export.write_videofile(f"final_clip.mp4", threads=8, preset="ultrafast", fps = fps)
        currentDuration += VideoFileClip(clips[i]).duration
        tempVideo = VideoFileClip("final_clip.mp4")
        tempVideo.write_videofile(f"temp.mp4", threads=8, preset="ultrafast", fps = fps)
        clips[0] = "temp.mp4"

def DeleteTrash():
    all_files = os.listdir()
    title_files = [file for file in all_files if re.match(r"title .*", file)]
    os.remove("temp.mp4")
    os.remove("trimmed_video.mp4")
    # Combine all files to delete
    files_to_delete = title_files

    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except OSError as e:
            print(f"Error deleting {file}: {e}")


main()
#clips = ["title 1 comment 0 reply 0.mp4","title 1 comment 1 reply 0.mp4","title 1 comment 2 reply 0.mp4","title 1 comment 3 reply 0.mp4"]
finalizeClips(clips)
t.sleep(1)
DeleteTrash()
print("DONE!")