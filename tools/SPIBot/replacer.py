from pathlib import Path

replace_items = {
    'da tarde': 'PM',
    'da manhã': 'AM',
    'da noite': 'PM',
    'da madrugada': 'AM'
}

def adjust_timestamp():
    for entry in Path("EXTRATOR").iterdir():
        if entry.is_dir():
            for entry2 in entry.iterdir():
                if entry2.name.startswith("CHAT_") and entry2.name.endswith(".txt"):
                    with entry2.open("r", encoding="utf-8") as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines):
                        parts = line.split("-")
                        for key, value in replace_items.items():
                            parts[0] = parts[0].replace(key, value)
                        new_line = "-".join(parts)
                        lines[i] = new_line
                    with entry2.open("w", encoding="utf-8") as f:
                        lines = f.writelines(lines)