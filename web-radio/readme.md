sudo apt install mpc mpd  
sudo apt install libmpdclient-dev  

edit /usr/share/alsa/alsa.conf  
change the following line from  
```
defaults.ctl.card 0
defaults.pcm.card 0
```  
to
```
defaults.ctl.card 1
defaults.pcm.card 1
```

gcc webradio.c -o webradio -lmpdclient
