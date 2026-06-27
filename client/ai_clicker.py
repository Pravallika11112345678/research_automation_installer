import time
import io
import requests
import pyautogui
from pywinauto import Desktop

print("[*] Advanced AI Network Client Bot Started...")

SERVER_URL = "http://127.0.0.1:5000/predict"

actions = [
    "click next button",
    "click install button",
    "click i agree button",
    "click finish button"
]

agreement_done = False
finish_clicked = False

# ---------------- FIND INSTALLER WINDOW ----------------
def get_installer_window():
    windows = Desktop(backend="uia").windows()
    for win in windows:
        try:
            title = win.window_text().lower()
            if any(word in title for word in [
                "setup",
                "installer",
                "wizard",
                "advanced ip scanner",
                "7-zip",
                "select setup language"
            ]):
                print(f"[✔] Installer Found: {title}")
                return win
        except:
            pass
    return None

# ---------------- SAFE BUTTON CLICK ----------------
def click_button(win, keywords):
    try:
        buttons = win.descendants(control_type="Button")
        for btn in buttons:
            try:
                text = btn.window_text().lower().strip()
                print("[BUTTON]:", text)
                if not btn.is_enabled():
                    continue

                # NEVER CLICK CANCEL
                if "cancel" in text:
                    continue

                if any(word in text for word in keywords):
                    btn.click_input()
                    print(f"[✔] CLICKED: {text}")
                    time.sleep(2)
                    return True
            except:
                continue
    except:
        pass
    return False

# ---------------- ACCEPT AGREEMENT ----------------
def select_agreement(win):
    global agreement_done
    if agreement_done:
        return False
    try:
        radios = win.descendants(control_type="RadioButton")
        for rb in radios:
            try:
                text = rb.window_text().lower()
                print("[RADIO]:", text)
                if "accept" in text and "not" not in text:
                    rb.select()
                    print("[✔] AGREEMENT ACCEPTED")
                    agreement_done = True
                    time.sleep(1)
                    return True
            except:
                continue
    except:
        pass
    return False

# ---------------- NETWORK AI SCREEN ANALYSIS ----------------
def get_ai_action(win):
    try:
        rect = win.rectangle()
        image = pyautogui.screenshot(region=(
            rect.left,
            rect.top,
            rect.width(),
            rect.height()
        ))

        # Convert screenshot to bytes stream in-memory (Avoids writing to disk)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Build HTTP multi-part payload structure
        files = {'image': ('screenshot.png', img_byte_arr, 'image/png')}
        data = {'labels': ",".join(actions)}

        # Delegate heavy inference to Marcus's Server
        response = requests.post(SERVER_URL, files=files, data=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return result["prediction"], result["confidence"]
        
        print(f"[Client Warning] Server returned status: {response.status_code}")
        return "unknown", 0

    except Exception as e:
        print(f"[AI Fetch Exception]: {e}")
        return "unknown", 0

# ---------------- MAIN LOOP ----------------
while True:
    try:
        # REFRESH WINDOW EACH LOOP
        win = get_installer_window()
        if not win:
            print("[!] Waiting for installer...")
            time.sleep(2)
            continue

        win.set_focus()

        # ---------------- ACCEPT AGREEMENT ----------------
        if select_agreement(win):
            click_button(win, ["next"])
            continue

        # ---------------- NEXT ----------------
        if click_button(win, ["next"]):
            continue

        # ---------------- INSTALL ----------------
        if click_button(win, ["install"]):
            continue

        # ---------------- YES ----------------
        if click_button(win, ["yes"]):
            continue

        # ---------------- OK ----------------
        if click_button(win, ["ok"]):
            continue

        # ---------------- FINISH ----------------
        if click_button(win, ["finish"]):
            print("[✔] FINISH CLICKED")
            finish_clicked = True
            time.sleep(3)
            continue

        # ---------------- LAUNCH APP ----------------
        if click_button(win, ["launch", "run"]):
            print("[✔] APP LAUNCHED")
            time.sleep(3)
            continue

        # ---------------- CLOSE ONLY AFTER FINISH ----------------
        if finish_clicked:
            if click_button(win, ["close"]):
                print("[✔] INSTALLER CLOSED")
                break

        # ---------------- AI OUTPUT ----------------
        action, conf = get_ai_action(win)
        print(f"[AI Response Target]: {action} (Confidence: {conf:.2f})")
        
        # Real-world click implementation hooks go here based on server text matches...
        time.sleep(2)

    except Exception as e:
        print("[ERROR]:", e)
        time.sleep(2)

print("[✔] BOT COMPLETED")
