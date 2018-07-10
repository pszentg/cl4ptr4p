import pyaudio
import struct
import math
from main.servo_controller import ServoController
import main.servo_types
import time

INITIAL_TAP_THRESHOLD = 0.25
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
INPUT_BLOCK_TIME = 0.03
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.30/INPUT_BLOCK_TIME


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    #for debug purposes
    #print(math.sqrt( sum_squares / count ))

    return math.sqrt( sum_squares / count )


class AudioController(object):
    def __init__(self):
        self.input_frames_per_block = 0
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1
        self.quietcount = 0
        self.errorcount = 0
        self.controller = ServoController(main.servo_types.SG90)
        self.tap_count = 0
        self.previous_tap_time = time.time()

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print("Device %d: %s" % (i, devinfo["name"]))

            for keyword in ["mic","input","usb"]:
                if keyword in devinfo["name"].lower():
                    print("Found an input: device %d - %s" % (i, devinfo["name"]))
                    device_index = i
                    return device_index

        if device_index is None:
            print("No preferred input found; using default input device.")

        return device_index

    def open_mic_stream(self):
        device_index = self.find_input_device()
        device_info = self.pa.get_device_info_by_index(device_index)

        self.input_frames_per_block = int(device_info["defaultSampleRate"] * INPUT_BLOCK_TIME)

        stream = self.pa.open(format=FORMAT,
                              channels=device_info["maxInputChannels"],
                              rate=int(device_info["defaultSampleRate"]),
                              input=True,
                              input_device_index=device_index,
                              frames_per_buffer=self.input_frames_per_block)

        return stream

    def tap_detected(self):
        print("tapped")
        # switch off with 2 claps, max 1 sec between the claps
        if time.time() - self.previous_tap_time >= 1:
            self.tap_count = 0
        self.tap_count += 1

        if self.tap_count % 2 == 0:
            self.controller.switch_on()
            print("lamp switched on")

        # switch off if the last clap was more than a sec ago
        elif self.tap_count % 2 == 1:
            print("lamp switched off")
            self.controller.switch_off()

        self.previous_tap_time = time.time()

    def listen(self):
        try:
            # won't throw an exception if there was an input buffer overflow
            block = self.stream.read(self.input_frames_per_block, False)
        except Exception as e:
            self.errorcount += 1
            print("(%d) Error recording: %s" % (self.errorcount, e))
            self.noisycount = 1
            return

        amplitude = get_rms(block)
        if amplitude > self.tap_threshold:
            # noisy block
            self.quietcount = 0
            self.noisycount += 1
        else:
            # quiet block.

            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.tap_detected()
            self.noisycount = 0
            self.quietcount += 1
