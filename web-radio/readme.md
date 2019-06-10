Prepare
=======
```
$ sudo apt install mpc mpd  
$ sudo apt install libmpdclient-dev  
```
in case of an USB sound card, edit /usr/share/alsa/alsa.conf  
change the following lines from
```
defaults.ctl.card 0
defaults.pcm.card 0
```  
to
```
defaults.ctl.card 1
defaults.pcm.card 1
```
in case of USB sound card, ~/.asoundrc might look as follow
```
pcm.!default {
        type hw
        card 1
}

ctl.!default {
        type hw
        card 1
}
```

Build
=====

gcc webradio.c -o webradio -lmpdclient
