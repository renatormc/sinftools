import cv2
import os
import numpy as np
from PIL import Image
from pathlib import Path
from uuid import uuid4


class ThumbsGenerator:
    def __init__(self, folder):
        self.folder = Path(folder)
        if not self.folder.exists():
            os.mkdir(self.folder)
            os.system(f"attrib +h {self.folder}")
            open(self.folder / '.reportignore', 'a').close()
        os.environ['FFREPORT'] = "level=quiet"

    def set_config(self, n_rows, n_cols, thumb_size, extension):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.thumb_size = thumb_size
        self.thumb_extension = extension

    def video_to_frames(self, video_filename):
        n = self.n_rows * self.n_cols
        cap = cv2.VideoCapture(video_filename)
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        frames = []
        if cap.isOpened() and video_length > 0:
            frame_ids = [0]
            if video_length >= n:
                step = 1 / (n - 1)
                frame_ids = [round(video_length * step * i) for i in range(n)]
            count = 0
            success, image = cap.read()
            while success:
                if count in frame_ids:
                    frames.append(image)
                success, image = cap.read()
                count += 1
        return frames

    def generate_name(self):
        return f"{self.folder}\\{uuid4()}{self.thumb_extension}"
        

    def image_to_thumb(self, img):
        height, width, channels = img.shape
        if (width >= self.thumb_size):
            r = (self.thumb_size + 0.0) / width
            max_size = (self.thumb_size, int(height * r))
            try:
                return cv2.resize(img, max_size, interpolation=cv2.INTER_AREA)
            except:
                return None

    def generate_video_thumb(self, filename):
        filename = str(filename)
        n = self.n_rows * self.n_cols
        frames = self.video_to_frames(filename)
        thumb_parts = [self.image_to_thumb(frame) for frame in frames]
        if thumb_parts:
            rows = []
            for i in range(0, len(thumb_parts), self.n_cols):
                rows.append(thumb_parts[i:i + self.n_cols])
            try:
                imgs = []
                for row in rows:
                    img = np.concatenate(tuple(row), axis=1)
                    imgs.append(img)
                img = np.concatenate(tuple(imgs), axis=0)
                filename = self.generate_name()
                cv2.imwrite(filename, img)
                return filename
            except Exception as e:
                pass

    def generate_image_thumb(self, filename):
        filename = str(filename)
        img = cv2.imread(filename)
        if img is not None:
            thumb = self.image_to_thumb(img)
            if thumb is not None:
                thumb_filename = self.generate_name()
                cv2.imwrite(thumb_filename, thumb)
                return thumb_filename

        # Try PIL if it didn' work with opencv
        try:
            im = Image.open(filename)
            im.thumbnail((self.thumb_size, self.thumb_size))
            thumb_filename = self.generate_name()
            im.save(thumb_filename)
            return thumb_filename
        except:
            pass


if __name__ == '__main__':
    os.chdir(r'C:\wamp64\www\laudos\Motorola GSM_XT925 RAZR')
    thumbs_generator = ThumbsGenerator()
    res = thumbs_generator.generate_video_thumb(
        r'C:\wamp64\www\laudos\Motorola GSM_XT925 RAZR\files\Video\VID-20140625-WA0003.mp4', 90)
    print(res)
