# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import os

queue_module_path = os.path.join('src', 'coreClasses', 'queue_cython.pyx')

extensions = [
    Extension("src.coreClasses.queue_cython", # Nombre del módulo a importar
              [queue_module_path],
              language="c") # Especificar lenguaje C
]

setup(
    name="TaskManager Core", # Nombre del paquete
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"} # Asegurar Python 3
    ),
    # Necesario para incluir paquetes Python normales junto con extensiones
    packages=['src', 'src.coreClasses', 'src.GUIClasses'],
    zip_safe=False,
)

