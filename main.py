import os
import requests
import time
import psutil
import ctypes
import winreg

# Check and install required modules
try:
    import requests
    import psutil
except ImportError:
    print("Required modules not found. Installing...")
    os.system("pip install requests psutil")
    print("Modules installed. Please run the script again.")
    exit()

# files to download
file_urls = [
    "https://github.com/musaalif6969/IDM-Registered-Version/raw/main/resources/IDMan.exe",
    "https://raw.githubusercontent.com/musaalif6969/IDM-Registered-Version/main/resources/win.reg"
]

# Destination directory to save files
download_path = "C:\\Windows\\Temp"
idm_exe_path = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"

def download_file(url, dest_folder):
    filename = url.split("/")[-1]
    dest_path = os.path.join(dest_folder, filename)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(dest_path, "wb") as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)

    return dest_path

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_colored(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")

def run_as_admin():
    shell32 = ctypes.windll.shell32
    if shell32.IsUserAnAdmin():
        return True

    print("Administration is required !")
    input("Press Enter to exit...")
    return False

def get_name_from_registry(key_path, value_name):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            return winreg.QueryValueEx(key, value_name)[0]
    except (FileNotFoundError, OSError, winreg.WindowsError):
        return None

def main():
    try:
        if not run_as_admin():
            return
        os.makedirs(download_path, exist_ok=True)

        print("Gathering Resources...")

        for url in file_urls:
            download_file(url, download_path)

        clear_console()

        print_colored("Done gathering resources!", 92)
        time.sleep(3)

        clear_console()

        if not os.path.exists(idm_exe_path):
            print_colored("Install IDM first !", 91)
            time.sleep(3)
            return 

        print_colored("Started Registering ...", 93) 

        #Kill IDMan.exe process
        idm_process_found = False
        for process in psutil.process_iter(['pid', 'name']):
            if "IDMan.exe" in process.info['name']:
                idm_process_found = True
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()
                except psutil.NoSuchProcess:
                    pass
                break

        clear_console()

        print_colored("Started Registering ...", 93)

        if idm_process_found:
            time.sleep(1)
            if not any("IDMan.exe" in process.info['name'] for process in psutil.process_iter(['name'])):
                print_colored("- IDM Closed", 92) 
            else:
                print_colored("- IDM Closed Already", 92) 
        else:
            print_colored("- IDM Closed Already", 92)  

        time.sleep(3)

        clear_console()

        #moving files and merging registry
        if os.path.exists(idm_exe_path):
            downloaded_idm_path = os.path.join(download_path, "IDMan.exe")
            os.replace(downloaded_idm_path, idm_exe_path)
            print_colored("- Registering ...", 91)
            os.system(f'reg import "{os.path.join(download_path, "win.reg")}"')
            time.sleep(3)

            clear_console()

            print_colored("IDM Registered Successfully !", 92) 

        #giv ur name
        first_name = input("Enter your First Name: ")
        last_name = input("Enter your Last Name: ")

        if first_name and last_name:
            registry_key_path = "SOFTWARE\\DownloadManager"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "FName", 0, winreg.REG_SZ, first_name)
                winreg.SetValueEx(key, "LName", 0, winreg.REG_SZ, last_name)

        clear_console()

        print_colored("First Name:", 94)
        retrieved_first_name = get_name_from_registry(registry_key_path, "FName")
        if retrieved_first_name is not None:
            print(retrieved_first_name)
        else:
            print_colored("Can't find registry", 91)

        print_colored("Last Name:", 94)
        retrieved_last_name = get_name_from_registry(registry_key_path, "LName")
        if retrieved_last_name is not None:
            print(retrieved_last_name)
        else:
            print_colored("Can't find registry", 91)

        time.sleep(4)

        clear_console()

        print_colored("IDM is registered! Bye :)", 92)  #bye

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
