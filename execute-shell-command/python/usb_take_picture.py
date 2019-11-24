import os

# sudo apt update
# sudo apt install fswebcam
#
shell_stdout = os.popen("fswebcam picture.jpg").read()
print("Take picture: ", shell_stdout)