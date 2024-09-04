from tkinter import Tk, Label, Entry, Button

from lynq import GLOBAL_LOGGER as logger

from lynq._backendutils.lynq.msie import pwsh

def run_process(entry: Entry) -> None:
    text: str = entry.get()

    if text.startswith("lynq://app/"):
        pwsh(f"python {text.removeprefix("lynq://app/")}.py")

    elif text.startswith("lynq://"):
        text = f"http://localhost:{text.removeprefix("lynq://")}/"

        pwsh(f"start {text}")

    elif (text.strip(">") == "exit") or (text == r"%exit"):
        logger.info("Exited Lynq RUNGUI.")

        entry.master.destroy()
        
        exit(0)

    elif (text.strip(">") == "ping") or (text == r"%ping"):
        logger.info("Ping received from Lynq RUNGUI.")

    elif text.startswith(">") or text.startswith("%"):
        pwsh(text.strip(">") if text.strip(">") != text else text.removeprefix("%"))

    else:
        pwsh(f"start {text}")

def run_gui() -> None:
    logger.info("Building Lynq RUNGUI terminal instance.")

    root: Tk = Tk()

    root.title("Run using Lynq")
    root.geometry("400x150")
    root.resizable(False, False)

    Label(root, text="Run a new process using Lynq").pack()
    entry: Entry = Entry(root, width=80)
    entry.pack(padx=10, pady=10)
    Button(root, text="Submit", command=lambda: run_process(entry)).pack(pady=10)

    logger.info("Completed build; launch sequence initiated.")

    root.mainloop()