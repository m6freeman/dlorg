import time
import re
from pathlib import Path
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
watch_folder = Path.home() / 'Downloads'

# Destination DOCUMENT folder and regex of common DOCUMENT filetypes
documents_folder    = Path.home() / 'Documents'
docs_exts           = '(\.)+(csv|dat|doc|docx|ged|key|keychain|log|msg|odt|pages|pps|ppt|pptx|rtf|sdf|tar|tax2016|tax2019|tex|txt|vcf|wpd|wps|xml)'

# Destination IMAGE folder and regex of common IMAGE filetypes
images_folder       = Path.home() / 'Pictures'
image_exts          = '(\.)+(ai|bmp|eps|gif|heif|indd|jpg|png|psd|raw|svg|tiff|webp)'

# Destination MUSIC folder and regex of common MUSIC filetypes
music_folder        = Path.home() / 'Music'
music_exts          = '(\.)+(3gp|8svx|aa|aac|aax|act|aiff|alac|amr|ape|au|awb|cda|dct|dss|dvf|flac|gsm|iklax|ivs|m4a|m4b|m4p|mmf|mp3|mpc|msv|nmf|nsf|oga|mogg|opus|ra|rm|rf64|sln|tta|voc|vox|wav|wma|wv)'

# Destination VIDEO folder and regex of common VIDEO filetypes
videos_folder       = Path.home() / 'Videos'
video_exts          = '(\.)+(3g2|3gp|amv|asf|avi|drc|f4a|f4b|f4p|f4v|flv|flv|flv|gif|gifv|m2ts|m2v|m4p|m4v|mkv|mng|mov|mp2|mp4|mpe|mpeg|mpg|mpv|mts|mxf|nsv|ogg|ogv|qt|rm|rmvb|roq|svi|ts|vob|webm|wmv|yuv)'

# define filesystemeventhandler derived handler class
class MyHandler(FileSystemEventHandler) :



    # set constant buffer size to 64kb chunks
    BUFF_SIZE = 65536

    # on event, perform organization
    def on_created(self, event):
        self.organize_files(watch_folder)
    


    # The purpose of this method is to iterate through each file within a directory,
    # parse it's file extension, and move the file into it's appropriate folder.
    def organize_files(self, watch_folder):

        # iterate through each file within the watch_folder
        files = (each_file for each_file in watch_folder.iterdir() if each_file.is_file())

        for each_file in files :

            # capture the file extension to test against
            ext = each_file.suffix.lower()

            # perform filetype checks
            # check if it's a document
            if re.match(docs_exts, ext, re.IGNORECASE) :
                destination = documents_folder

            # check if it's an image
            elif re.match(image_exts, ext, re.IGNORECASE) :
                destination = images_folder

            # check if it's music
            elif re.match(music_exts, ext, re.IGNORECASE) :
                destination = music_folder

            # check if it's a video
            elif re.match(video_exts, ext, re.IGNORECASE) :
                destination = videos_folder

            # if it's none of those, skip that file
            else :
                continue

            # pass the destination folder and relevant file information to be moved
            self.rename_file(each_file, destination)


    # The purpose of this method is to take the destination folder and file to be moved
    # and rename the file with some of it's hash if a file of the same name already exists
    def rename_file(self, file_to_sort, destination) :
        
        # check if a file by the same name exists in the destination folder and 
        # append a character to the end of the name until it no longer matches
        while Path.exists(Path.joinpath(destination, file_to_sort.name)):
            file_to_sort = file_to_sort.rename(Path.joinpath(watch_folder,file_to_sort.stem + "_" + file_to_sort.suffix))
        
        # then move the file from watch_folder to it's destination
        file_to_sort.rename(Path.joinpath(destination, file_to_sort.name))



event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, watch_folder.as_posix())
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()

observer.join()


## TODO exception handling everywhere