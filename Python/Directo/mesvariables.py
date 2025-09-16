from pathlib import Path

DOM = "https://shahhid4u.com/"

dwn_cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]
cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear
NB = 50

ses_path = Path("datas/Seasons")
eps_path = Path("datas/Episodes")
lib_path = Path("Library")
