import os
from pathlib import Path

# Check if any errors occurred during execution of requesting user list
path = Path(r"D:\Informatyka\MalDB\Error.log")
if os.path.getsize(path) > 0:
    import ctypes

    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    # Display an message to the user
    Mbox('Error', 'An error occured while trying to read anime from MAL ', 0)
