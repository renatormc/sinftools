from pathlib import Path
import re

class SpiAnalyzer:
    def __init__(self, folder: Path):
        self.folder = folder

    def find_regex(self):
        candidates = [
            [r'(?P<timestamp>(\d{2}/\d{2}/\d{4})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)', r'^(\d{2}/\d{2}/\d{4}\s\d{1,2}:\d{2}\s)', 0],
            [r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',  r'^(\d{2}/\d{2}/\d{2}\s\d{1,2}:\d{2}\s)', 0],
            [r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\,\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)', r'^(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s)', 0],
            [r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2} ((PM)|(AM))))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)', r'^(\d{2}/\d{2}/\d{2}\s\d{1,2}:\d{2}\s(PM)|(AM))', 0]
        ]
        dir_ = self.folder / "chats_spi"
        
        for file in dir_.iterdir():
            with file.open("r", encoding="utf-8") as f:
                text = f.read()
            for i, item in enumerate(candidates):
                n = len(re.findall(item[0], text))
                candidates[i][2] += len(re.findall(item[1], text))
        res = max(candidates,key=lambda x: x[2])
        return res[0]

if __name__ == "__main__":
    obj = SpiAnalyzer(Path("D:\\test_report\\C4\\spi"))
    print(obj.find_regex())


