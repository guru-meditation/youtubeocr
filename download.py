from pytube import YouTube
import ffmpeg
import random

#23456789112345678921234567893123456789412345678951234567896123456789712

# save a frame
def save_frame(in_filename, frame_num):
    out, err = (
        ffmpeg
        .input(in_filename)
        .filter_('select', 'gte(n,{})'.format(frame_num))
        .output("out%d.jpg" % frame_num, vframes=1)
        .run(capture_stdout=True)
    )
    return out

# youTube file
video =YouTube('https://www.youtube.com/watch?v=FQmupn3YSuY')

#setting the extension
extension="mp4"

# download by itag
#itag=18
#in_file = video.streams \
#    .filter(progressive=True, file_extension=extension) \
#    .get_by_itag(itag).download(filename=str(itag))

# download first one
in_file = video.streams \
    .filter(progressive=True, file_extension=extension) \
    .first().download()

# print out info about file
print("file name: " + in_file)
print("video title: " + video.title)
print("Video ID: " + video.video_id)
print("Age restricted: " + str(video.age_restricted))
print("Video thumbnail url: " + video.thumbnail_url)
print(" ")

# probing the file
dicRaw = ffmpeg.probe(in_file)

dic = next((stream for stream in dicRaw['streams'] if
  stream['codec_type'] == 'video'), None)

# grabbing info about video
width = int(dic['width'])
height = int(dic['height'])
frames = int(dic['nb_frames'])

# getting a random frame
frame = random.randint(0,frames)

# save random frame
out = save_frame(in_file, frame)

# save first frame
out = save_frame(in_file, 0)