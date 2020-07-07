from pathlib import Path

class IpedConfigReader:

    def __init__(self, iped_folder):
        self.iped_folder = Path(iped_folder)


    def get_temp_folder(self):
        items = self.read_file(self.iped_folder / "LocalConfig.txt")
        return items['indexTemp']

    def read_file(self, file):
        file = Path(file)
        with file.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if not line.startswith("#") and line.strip() != '']
        items = {}
        for line in lines:
            try:
                key, value = line.split("=")
                items[key.strip()] = value.strip()
            except Exception as e:
                print(e)
        return items

if __name__ == "__main__":
    reader = IpedConfigReader(r'D:\portable\IPED-3.17\iped-3.17-snapshot')
    temp = reader.get_temp_folder()
    print(temp)
