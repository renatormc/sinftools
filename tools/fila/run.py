import importlib.util
import sys
from subprocess import CalledProcessError
from uteis import get_error_string
spec = importlib.util.spec_from_file_location("module.name", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

try:
    module.main()
    print("SINF: Processo finalizado com sucesso!")
except CalledProcessError as e:
    print(e.output.decode("cp1252"))
except Exception as e:
    print(get_error_string(e))
