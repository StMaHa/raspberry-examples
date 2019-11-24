# Example and exercise to build a alarm system
# First exercise
# sudo apt update
# sudo apt install fswebcam ssmtp mpack
#
# setup smtp:
# sudo nano /etc/ssmtp/ssmtp.conf
#
# Add following line to ssmtp.conf
#  root=username@gmail.com
#  mailhub=smtp.gmail.com
#  rewriteDomain=gmail.com
#  AuthUser=username
#  AuthPass=password
#  FromLineOverride=YES
#  UseTLS=YES
fswebcam alarm.jpg
# mpack -s "RPi ALARM" alarm.jpg username@gmail.com


