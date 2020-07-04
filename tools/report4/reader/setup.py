from cx_Freeze import setup, Executable

setup(name='nome-do-arquivo',
    version='1.0',
    description='descrição do programa',
    options={'build_exe': {'packages': ['matplotlib']}},
    executables = [Executable(
                   script='server.py',
                   base=None,
                   icon='reader_server\\resources\\icon.png'
                   )
                  ]
)