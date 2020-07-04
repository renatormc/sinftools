from pathlib import Path

text = "\n".join([str(entry.absolute()) for entry in Path(".").iterdir() if entry.suffix == ".E01"])
print(text)
input("\nTecle algo para sair.")