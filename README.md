# raspberry-examples

Source code snippets and examples for Raspberry Pi.  
> Examples...  
> ...should be easy to undestand.  
> ...should use libraries already available on the Raspberry Pi (no installation needed, no third party libraries if possible)  

:warning: Attention :warning:  
_But nevertheless, might contain failures or become invalid after some time._  
_Think twice using the GPIO pins at your Raspberry Pi. I am not responsible if your Pi will be damaged._

**Download / clone the repository to your computer:**
```
git clone https://github.com/StMaHa/raspberry-examples.git
```
**To update already cloned repository, do the following steps:**
```
cd raspberry-examples
git fetch
git rebase
````
## GPIO pin Header
**:warning: ATTENTION :warning:**  
Allways keep in mind, that the current of the GPIO pins is limited and should not be exceeded.  
Also the voltage of the GPIO pins is limited. The voltage of an input pin must not exceed 3.3V.  
If a device, which needs higher voltage (e.g. 5V), should be connected to the Raspberry Pi, please use a voltage devider or a level shifter.  
For the correct limits please have a look to the official Raspberry Pi web pages.  
![GPIO pin header](https://github.com/StMa-Ha/raspberry-examples/blob/master/GPIO.jpg)

# LICENSE

See the [LICENSE](LICENSE.md) file for license rights and limitations.

----
<sup>(c) Raspberry Pi is a trademark of the Raspberry Pi Foundation.</sup>
