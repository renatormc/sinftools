from pathlib import Path

res = Path("D:\\teste_report2").glob('**/*/*/sinf_thumbs')
for item in res:
    print(item)

