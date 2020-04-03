import os
import time
import json
import shutil
import re
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


                ###############################################################################
                #                                                                             #
                #          DownLoadsORGanizer                                                 #
                #                                                                             #
                #          Purpose: Module intended to monitor your downloads folder          #
                #                   and organize files based on their file extension          #
                #                   This is not intended to behave recursively, yet.          #
                #                                                                             #
                ###############################################################################


# The folder to watch
watch_folder = "C:/Users/Matthew/Downloads"

# Destination IMAGE folder and regex of common IMAGE filetypes
images_folder       = R"C:/Users/Matthew/Pictures"
image_exts          = '(\.)+(AI|BMP|EPS|GIF|HEIF|INDD|JPG|PNG|PSD|RAW|SVG|TIFF|WEBP)'

# Destination VIDEO folder and regex of common VIDEO filetypes
videos_folder       = R"C:/Users/Matthew/Videos"
video_exts          = '(\.)+(3g2|3gp|amv|asf|avi|drc|f4a|f4b|f4p|f4v|flv|flv|flv|gif|gifv|m2ts|m2v|m4p|m4v|m4v|mkv|mng|mov|mp2|mp4|mpe|mpeg|mpg|mpg|mpv|MTS|mxf|nsv|ogg|ogv|qt|rm|rmvb|roq|svi|ts|vob|webm|wmv|yuv)'

# Destination DOCUMENT folder and regex of common DOCUMENT filetypes
documents_folder    = R"C:/Users/Matthew/Documents"
docs_exts           = '(\.)+(csv|dat|doc|docx|ged|key|keychain|log|msg|odt|pages|pps|ppt|pptx|rtf|sdf|tar|tax2016|tax2019|tex|txt|vcf|wpd|wps|xml)'

# Destination MUSIC folder and regex of common VIDEO filetypes
music_folder        = R"C:/Users/Matthew/Music"
music_exts          = '(\.)+(3gp|8svx|aa|aac|aax|act|aiff|alac|amr|ape|au|awb|cda|dct|dss|dvf|flac|gsm|iklax|ivs|m4a|m4b|m4p|mmf|mp3|mpc|msv|nmf|nsf|oga|mogg|opus|ra|rm|raw|rf64|sln|tta|voc|vox|wav|webm|wma|wv)'

# create filesystemeventhandler class
class MyHandler(FileSystemEventHandler):

    # set constant buffer size to 64kb chunks
    BUFF_SIZE = 65536

    # on event, perform organization
    def on_created(self, event):
        self.organizeFiles()
    
    def on_modified(self, event):
        self.organizeFiles()



    def organizeFiles(self):
        # iterate through each file within the watch_folder
        for filename in os.listdir(watch_folder):

            # construct the original file's path
            src = watch_folder + "/" + filename

            # make sure it's a file and not a directory
            if os.path.isfile(os.path.join(watch_folder, filename)):

                # capture the file extension to test against
                ext = os.path.splitext(filename)[-1].lower()

                # perform filetype checks
                # check if it's an image
                if re.match(image_exts, ext, re.IGNORECASE):
                        new_destination = images_folder + "/"

                # check if it's a video
                elif re.match(video_exts, ext, re.IGNORECASE):
                    new_destination = videos_folder + "/"

                # check if it's a document
                elif re.match(docs_exts, ext, re.IGNORECASE):
                    new_destination = documents_folder + "/"

                # check if it's music
                elif re.match(music_exts, ext, re.IGNORECASE):
                    new_destination = music_folder + "/"

                # if it's none of those, skip that file
                else:
                    continue

                self.renameFile(src, new_destination, filename)

    def renameFile(self, src, destination, fileName):
        
        # if the new destination doesn't have a file of the same name, move it there
        if not os.path.exists(destination + fileName):
            os.rename(src, destination + fileName)
            
        # otherwise, hash the file bit by bit (to accommodate large file sizes) and append last 5 characters of hash to the filename
        else:
            md5 = hashlib.md5()
            with open(src, 'rb') as f:
                while True:
                    data = f.read(MyHandler.BUFF_SIZE)
                    if not data:
                        break
                    md5.update(data)
                fileName = md5.hexdigest()[-5:] + fileName
                f.close()

            # call renameFile again passing the same src, destination, but newly altered name and test again
            self.renameFile(src, destination, fileName)



event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, watch_folder)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()

observer.join()



# TODO substitute string /s with path objects 
