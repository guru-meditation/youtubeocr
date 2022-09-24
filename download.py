from pytube import YouTube
import ffmpeg
import random
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# save a frame
def save_frame(in_filename, frame_num):
    out, err = (
        ffmpeg.input(in_filename)
            .filter_('select', 'gte(n,{})'.format(frame_num))
            .output("out%d.jpg" % frame_num, vframes=1)
            .run(capture_stdout=True)
    )
    return out


# youTube file
video = YouTube('https://www.youtube.com/watch?v=MfQ7ehVOkrg')

# setting the extension
extension = "mp4"

# download first one
# in_file = "fsx 2010-04-10 22-34-50-05avi.mp4"
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
frame = random.randint(0, frames)

# save random frame
out = save_frame(in_file, frame)

# save first frame
out = save_frame(in_file, 0)

# hack hack hack
numImageToScan = 0

img = Image.open("out%d.jpg" % numImageToScan).convert('L')
img.save("out%d.jpg" % numImageToScan)

print("Scanning " + "out%d.jpg" % numImageToScan)

# psm is page segmentation mode
# oem is engine type - only seem to have neural net installed.
for config in ['--psm 6 --oem 1']:
    print("Result [" + pytesseract.image_to_string(Image.open("out%d.jpg" % numImageToScan),
                                                   config=config,
                                                   lang='eng') + "]")

print("Scanned " + "out%d.jpg" % numImageToScan)
