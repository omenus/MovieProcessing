
# Import everything needed to edit video clips
from moviepy.editor import *
import numpy as np
from os import walk
from os import access, R_OK
from os.path import isfile


def check_file(path):
    file = path
    result = True
    try:
        assert isfile(file) and access(file, R_OK), "File {} doesn't exist or isn't readable".format(file)
    except AssertionError as AE:
        print(AE)
        result = False
    return result


def get_video_files(filter = ".avi", folder="."):
    f = []
    for (dirpath, dirnames, filenames) in walk(folder):
        f.extend(filenames)
        #f.extend(dirnames)
        break
    v = [file for file in f if file.endswith(filter)]
    return list(v)


def sortfn(frame):
    #print(frame)
    f = frame
    a = np.ndarray(shape=frame.shape)
    is_color = False
    for x in frame:
        t = list(x)
        t.sort(key=lambda z: z[0])
        a[x] = t
        for d in x:
            e, f, r = d
            if int(e) != int((int(f)+int(r))/2):
                is_color = True
        return is_color


class FindColoredScenes:
    def __init__(self, clip):
        self.frame_counter = 0
        self.start_end_frames = []
        self.c = clip
        self.fps = clip.fps

    def find_scenes(self):
        start_frame = False
        for f in self.c.iter_frames():
            self.frame_counter += 1
            isColor = sortfn(f)
            if isColor is True and start_frame is False:
                start_frame = True
                start_frame_at = self.frame_to_time()
                print(f"color on {self.frame_to_time()} s")
            if isColor is False and start_frame is True:
                start_frame = False
                end_frame_at = self.frame_to_time()-0.1
                self.start_end_frames.append((start_frame_at, end_frame_at))
                print(f"end color on {self.frame_to_time()}s")
        if start_frame:
            self.start_end_frames.append((start_frame_at, self.frame_to_time()))

    def frame_to_time(self):
        return (self.frame_counter/self.fps)

    def get_scenes(self):
        return self.start_end_frames

    def get_counter(self):
        return self.frame_counter


def create_clip(start, end, clip):
    new_clip = clip.subclip(start, end)
    new_clip.write_videofile(f"new_clip{start}{end}.mp4", codec = "libx264", fps=25)
    new_clip.close()


def open_file(clip):
    result = None
    try:
        clip = VideoFileClip(clip)
        clip.close()
        result = True
    except Exception:
        print(f"Can't open file: {clip}")
        result = False
    return result


def run():
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    try:
        print(get_video_files(".avi", folder='.\\files'))
        clip = VideoFileClip("test2.avi")
        print("Duration of video : ", clip.duration)
        print("FPS : ", clip.fps)
        scenes = FindColoredScenes(clip)
        print(f"frames {scenes.get_counter()}")
        scenes.find_scenes()
        [create_clip(x, y, clip) for x, y in scenes.get_scenes()]
    except OSError as e:
        print(e)


def move_file(file, unreadable_filex = ".\\UNREADABLE_FILES"):
    if not os.path.exists(unreadable_filex):
        os.mkdir(unreadable_filex)
    os.system("move " + file + " " + unreadable_filex + '\\')


def search_files():
    #folder = '.\\files'
    folder = 'I:\\FatsharkFilmy'
    unreadable_filex = "I:\\FatsharkFilmy\\UNREADABLE_FILES"
    file_liest = get_video_files(".AVI", folder)
    for file in file_liest:
        print(folder + '\\' + file)
        if open_file(folder + '\\' + file) is False:
            move_file(folder + '\\' + file, unreadable_filex)


#run()
if __name__ == "__main__":
    #run only if run as script - use shebang
    search_files()