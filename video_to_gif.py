import ffmpeg
#install ffmpef from https://github.com/BtbN/FFmpeg-Builds/releases to PATH
import os
def video_to_gif(path):
    for filename in os.listdir(path):
        if filename.endswith(('.mp4','MP4')):
            name = filename.split('.')[0]
            print(f'{path}{filename}')
            stream = ffmpeg.input(f'{path}/{filename}')
            stream = ffmpeg.filter(stream,"fps",fps=5)
            stream = ffmpeg.output(stream,f'{path}/{name}.gif')
            ffmpeg.run(stream)

video_to_gif('test')
