# cl4ptr4p
simple python project to control the lights in the room with your claps.


## Getting started
The following ingredients were used for this recipe:

* RPi 3 Model B with Stretch installed
* [SG90 servo](https://www.amazon.de/gp/product/B07236KYVC/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)
* [USB Sound card](https://www.amazon.de/gp/product/B0037AOUUQ/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)
* [A small microphone](https://www.amazon.de/gp/product/B004YEWC22/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)

After hooking the stuff together, make sure to check:
* the PWM cable on the servo (colored orange) is hooked to GPIO17 (PIN 11) on the RPi
* you have the codecs, the RPi recognizes the USB sound card ($ arecord --list-devices)

### Dependencies
* `pip3 install pyaudio`

Assuming you're using a NOOBS raspbian, the rest should be installed as is (including Python3)

## License
This project is licensed under the GNU GPL 3.0 License - see [here](https://github.com/pszentgyorgyi/cl4ptr4p/blob/master/LICENSE)

## Future Improvements
* fine tuning the pre-filtering of the audio (eg. running the feed through an implementation of the Goertzel algorithm) - it recognizes any noise, not only claps
* reduce background noise
* unit tests
