import os
import tempfile
import codecs
import json
sinftools_dir = os.getenv("SINFTOOLS")

script_dir =  os.path.dirname(os.path.realpath(__file__))

answer_file = os.path.join(tempfile.gettempdir(), 'answaers.json')

def get_answaers(config):
    if  isinstance(config, str) and os.path.exists(config):
        config_file = config
    else:
        tempjsonfile = os.path.join(tempfile.gettempdir(), 'tempjsonfile.json')
        with codecs.open(tempjsonfile, "w", "utf-8") as f:
            f.write(json.dumps(config, ensure_ascii=False, indent=4))
        config_file = tempjsonfile
    script_path = os.path.join(script_dir, "fill.py")
    if os.path.exists(answer_file):
        os.remove(answer_file)
    cmd = f"s-py \"{script_path}\" \"{config_file}\" \"{answer_file}\""
    os.system(cmd)
    if os.path.exists(answer_file):
        with codecs.open(answer_file, "r", "utf-8") as f:
            response = json.load(f)
        return response