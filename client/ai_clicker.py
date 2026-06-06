import time
import pyautogui
from pywinauto import Desktop
import torch
import clip

print("[*] Advanced AI Installer Bot Started...")

device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------- LOAD AI MODEL ----------------
model, preprocess = clip.load(
    "ViT-B/32",
    device=device,
    download_root="."
)

actions = [
    "click next button",
    "click install button",
    "click i agree button",
    "click finish button"
]

text_tokens = clip.tokenize(actions).to(device)

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

                # IMPORTANT FIX
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


# ---------------- AI SCREEN ANALYSIS ----------------
def get_ai_action(win):

    try:

        rect = win.rectangle()

        image = pyautogui.screenshot(region=(
            rect.left,
            rect.top,
            rect.width(),
            rect.height()
        ))

        image_input = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():

            image_features = model.encode_image(image_input)

            text_features = model.encode_text(text_tokens)

            similarity = (
                image_features @ text_features.T
            ).softmax(dim=-1)

            index = similarity.argmax().item()

            confidence = similarity[0][index].item()

        return actions[index], confidence

    except:
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

        print(f"[AI]: {action} ({conf:.2f})")

        time.sleep(2)

    except Exception as e:

        print("[ERROR]:", e)

        time.sleep(2)

print("[✔] BOT COMPLETED")