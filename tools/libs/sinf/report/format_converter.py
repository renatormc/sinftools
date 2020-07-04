import os
import subprocess
import re
sinftools_dir = os.getenv("SINFTOOLS")
ffmped_path = f'{sinftools_dir}\\extras\\ffmpeg-20181107-0c6d4e7-win64-static\\bin\\ffmpeg.exe'

class FormatConverter:
    def __init__(self):
        self.overwrite = False
        self.max_dim = 100000
        self.movie_convert_extension = "mp4"
        self.image_convert_extension = "jpg"

    def exec_command(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        text = "".join([line.decode("ansi") for line in p.stdout.readlines()])
        return text
      
    def get_movie_info(self, filename):
        info = {"shape": None, "fps": None}
        output = self.exec_command(f"{ffmped_path} -i {filename} -hide_banner")
        res = re.search(r'(\d+x\d+),', output)
        if res:
            info['shape'] = tuple([int(a) for a in res.group(1).split("x")])
        res = re.search(r'(\d+(\.\d+)?) fps,', output)
        if res:
            info['fps'] = float(res.group(1))
        return info


    def convert(self, filename):
        
        ext = filename.split(".")[-1].lower()
        if len(ext) > 5:
            return {"resize": False, "shape": None, "filename": filename, "converted": False, "extension_changed": False}
        if ext == "heic":
            pass
            # return self.convert_image(filename)
        if ext == "mov":
            return self.convert_movie2(filename, ext, change_extension=True)
        if ext == "3gp":
            return self.convert_movie2(filename, ext, change_extension=True)
        if ext == "mp4":
            return self.convert_movie2(filename, ext, change_extension=False)
        return {"resize": False, "shape": None, "filename": filename, "converted": False, "extension_changed": False}


    def heic2jpg(self, filename):
        return filename


    # def convert_movie(self, filename, ext, change_extension=False):
    #     info = self.get_movie_info(filename)
    #     if info['shape'] is not None:
    #         resize = False
    #         rate = 1
    #         if info['shape'][0] > info['shape'][1]:
    #             if info['shape'][0] > self.max_dim:
    #                 resize = True
    #                 rate = self.max_dim/info['shape'][0]
    #         else:
    #             if info['shape'][1] > self.max_dim:
    #                 resize = True
    #                 rate = self.max_dim/info['shape'][1]
    #         if resize:
    #             print(f"convertendo arquivo {filename}")
    #             w = int(int(info['shape'][0]*rate)/2)*2
    #             h = int(int(info['shape'][1]*rate)/2)*2
    #             shape = (h,w)
    #             ext_size = len(ext)
    #             basename = filename[:-ext_size-1]
    #             newname = f"{basename}_converted.{self.movie_convert_extension}" if change_extension else f"{basename}_converted.{ext}"
    #             cmd = f"{ffmped_path} -y -i \"{filename}\" -filter:v scale={w}:{h} -c:a copy \"{newname}\""
    #             self.exec_command(cmd)
    #             if self.overwrite:
    #                 os.remove(filename)
    #             return {"resize": resize, "shape": shape, "filename": newname, "converted": True, "extension_changed": change_extension}
    #         elif change_extension:
    #             print(f"convertendo arquivo {filename}")
    #             shape = (info['shape'][1], info['shape'][0])
    #             newname = filename
    #             cmd = f"{ffmped_path} -y -i \"{filename}\" \"{newname}\""
    #             self.exec_command(cmd)
    #             if self.overwrite:
    #                 os.remove(filename)
    #             return {"resize": resize, "shape": shape, "filename": newname, "converted": True, "extension_changed": change_extension}
    #     return {"resize": False, "shape": None, "filename": filename, "converted": False, "extension_changed": change_extension}


    def convert_movie2(self, filename, ext, change_extension=False):
        #Verificar se é preciso mudar o tamanho
        info = self.get_movie_info(filename)
        resize = False
        shape = None
        if info['shape'] is not None:
            rate = 1
            if info['shape'][0] > info['shape'][1]:
                if info['shape'][0] > self.max_dim:
                    resize = True
                    rate = self.max_dim/info['shape'][0]
            else:
                if info['shape'][1] > self.max_dim:
                    resize = True
                    rate = self.max_dim/info['shape'][1]
            shape = (info['shape'][1], info['shape'][0])
           

        #Efetuar conversão
        if resize or change_extension:
            print(f"convertendo arquivo {filename}")
            ext_size = len(ext)
            basename = filename[:-ext_size-1]
            newname = f"{basename}_converted.{self.movie_convert_extension}" if change_extension else f"{basename}_converted.{ext}"
            if resize:
                w = int(int(info['shape'][0]*rate)/2)*2
                h = int(int(info['shape'][1]*rate)/2)*2
                shape = (h,w)
                cmd = f"{ffmped_path} -y -i \"{filename}\" -filter:v scale={w}:{h} -c:a copy \"{newname}\""
            else:
                cmd = f"{ffmped_path} -y -i \"{filename}\" \"{newname}\""
            self.exec_command(cmd)
            if self.overwrite:
                os.remove(filename)
            return {"resize": resize, "shape": shape, "filename": newname, "converted": True, "extension_changed": change_extension}

        return {"resize": False, "shape": None, "filename": filename, "converted": False, "extension_changed": change_extension}

    def convert_image(self, filename, ext):
        return {"resize": False, "shape": None, "filename": filename, "converted": False, "extension_changed": False}

if __name__ == "__main__":
    format_converter = FormatConverter()
    res = format_converter.get_movie_info(r'C:\Users\renato\Desktop\temp\Relatório Iphone\Apple_iPhone 7 Plus (A1784)\chats\WhatsApp\attachments122\1890f6f8-4d12-48d0-bc13-cd40e0783466_converted.mp4')
    print(res)
