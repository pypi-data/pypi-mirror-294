# GameDriver

Automate android games built on game engines other than Unity

## Install

```sh
pip install gamedriver
```

## Setup

```py
import os
import time

import gamedriver as gd
from gamedriver.settings import set_settings as set_gd_settings

# For example, we will use an adb client to provide the tap_xy and swipe
# functionality, and a scrcpy client to provide the image of the device screen.
import adbutils  # https://github.com/openatx/adbutils
import scrcpy  # https://github.com/leng-yue/py-scrcpy-client

# Recommend setting a SRC_DIR var in the project's top level __init__ file
# SRC_DIR = os.path.dirname(os.path.abspath(__file__))
from my_project import SRC_DIR


# Boilerplate for however you are providing adb tap + swipe, and get device
# screen functionality

# For example, the adb device is available on the standard port, 5555
serial = "127.0.0.1:5555"

# Initialization for this adb client
# Note there must be an adb server* (see the lib for specific behavior)
adb_client = adbutils.AdbClient()
adb_client.connect(serial)
adb_device = adb_client.device(serial)

# Initialization for this scrcpy client
scrcpy_client = scrcpy.Client(serial)
scrcpy_client.start(daemon_threaded=True)
# Wait for the server to spin up...
while scrcpy_client.last_frame is None:
    time.sleep(1)


# Set settings

# I'd recommend setting these settings at minimum
set_gd_settings(
    {
        # For example, next to our top level __init__ file we have a folder
        # "img" that contains all of our template images
        "img_path": os.path.join(SRC_DIR, "img"),
        "img_ext": ".png",
        "get_screen": lambda: scrcpy_client.last_frame,
        # Since we are streaming the screen using scrcpy, we can choose a very
        # high polling frequency. Screenshotting should use closer to 1+ seconds.
        "refresh_rate_ms": 10,
        "tap_xy": lambda x, y: adb_device.click(x, y),
        "swipe": lambda x1, y1, x2, y2, duration_ms: adb_device.swipe(
            x1, y1, x2, y2, duration_ms / 1_000
        ),
    }
)
```

For the full settings reference, see [settings.py](gamedriver/settings.py).

## Usage

### Cookbook

```py
# Recommend using this function by default
#
# Opens image <SRC_DIR>/img/buttons/confirm.png, searches the device screen for
# it, and taps it when it becomes visible.
gd.tap_img_when_visible("buttons/confirm")

# Wait until text/success is visible, then tap a different image
gd.wait_until_img_visible("text/success")
gd.tap_img("my-other-image")

# Keep tapping the image until it goes away or the timeout is reached
gd.tap_img_while_visible("buttons/back")

# Find all instances of an image, and do something with them
add_btns = list(gd.locate_all("buttons/add"))
if len(add_btns) > 3:
    gd.tap_box(add_btns[3])

# By default matching is in grayscale. However sometimes there is a need for
# color matching. For example, if the same button has different colors.
if not gd.touch_img_when_visible(
    # Wait until the button changes from disabled (gray) to enabled (blue).
    # Use a lower timeout in case this might not occur; then if it doesn't
    # we won't be waiting too long.
    "buttons/submit-blue", timeout_s=5, convert_to_grayscale=False
):
    raise Exception("Failed to submit")

# Perhaps you are missing matches or getting too many - try adjusting the
# threshold. For our default OpenCV match method, the threshold is a value in
# [0, 1], and lowering it makes matching more strict.
#
# The cancel button is not matching even though it is present. Loosen (raise)
# the threshold value since the match is of lower quality.
gd.touch_img_when_visible("buttons/cancel", threshold=0.1)

# Not recommended, but you can alternatively use a more implicit style.
#
# Maybe you need to tap whatever is at a location no matter what image it may be.
gd.tap_xy(500, 1000)
# Using an implicit wait avoids needing to have an image file to wait for.
# Hopefully you have a very good idea of about how long it should be.
gd.wait(0.1)
gd.tap_xy(750, 250)
gd.wait_until_img_visible("text/done")
gd.tap_xy(100, 100)
```

## API Documentation

// TODO

## FAQ

### Why only games, and why not Unity?

This can be used to automate other things, but using image matching for automation (this) should be an absolute last resort. For other use cases see [Appium](https://github.com/appium/appium), and in the Unity case the [Appium AltUnity plugin](https://github.com/headspinio/appium-altunity-plugin).

### Other PLs/platforms/_I need more_?

While I'm open to PRs, for the long term, effort is probably better directed at [integrating this project into the Appium images plugin](https://discuss.appium.io/t/images-plugin-support-and-design-limitations/43831). While it comes with challenges, especially of streaming the screens of various devices, integration with the WebDriver API would instantly provide support for many PLs and devices.
