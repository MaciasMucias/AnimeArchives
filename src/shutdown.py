import os
import psutil
import time
# if the computer has booted up less than 0.75 hour ago, then shut it down (it's 4:15 AM after all)
# if it's running for longer then it should continue doing so or
f = open("D:\Informatyka\MalDB\Shutdown.log", "w+")
f.write("Shutown script start\n")
working_time_in_hours = (time.time() - psutil.boot_time()) / 3600
working_time_is_short = working_time_in_hours < 0.75
f.write(f"{working_time_in_hours=}\n{working_time_is_short=}\n")
if working_time_is_short:
    f.write("Shutting down\n")
    f.close()
    os.system("shutdown /s /t 1")
    quit()
else:
    f.write("Not shutting down\n")
    f.close()
    # Normally the alert is launched at login, but the pc isn't being turned off so display it now
    import Alert  # scuffed way to run a script