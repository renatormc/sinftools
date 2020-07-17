from pathlib import Path
import click
import sys
import markers

def create_subfolders(folder_name):
    extracao = folder_name / "extracao"
    extracao.mkdir()
    data = {
        'type': 'hash_partial',
        'subtype': 'iped_images'
    }
    markers.mark_folder(extracao, data)
    processamento = folder_name / "processamento" 
    processamento.mkdir()
    data = {
        'type': 'hash_partial',
        'subtype': 'iped_results'
    }
    markers.mark_folder(processamento, data)
    return

if len(sys.argv) == 1:
    print("You need to specify the folders names separeted by white space")
    sys.exit()


current_directory = Path(".")

print("Creating directories")
for argument in sys.argv[1:]:
    directory = current_directory / argument
    if directory.exists():
        print(f"The directory \"{directory}\" already exists.")
        sys.exit()
    directory.mkdir()
    create_subfolders(directory)
print("Folders created.")

        
