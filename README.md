# X56-Indicator

This is a GUI and haptic indicator for Logitech X56 HOTAS system.

Since X56 doesn’t have detent, it’s sometimes hard to control the throttle in competitive environment. A sudden move could accidentally engage the afterburner or to shut off the engine, especially in combat simulations. A minimum distraction indicator, in both desktop and VR mode, would help to understand the current throttle status. Thus, this project is made.

In an update, haptic feed back is added. With 5 break-out module of Taptic Engine from iPhone 7 Plus and a Bluetooth module MH-M38, it’s easy to create an audio based haptic feed back actuator. This project generates mono low-frequency sound for driving the module, with the help of specialized sound mixing tools like Voicemeeter, it can be mixed with gaming sound, allowing vibration on the stick and haptic virtual detent on the throttle.

## Disclaimer

This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this software.  If not, see <http://www.gnu.org/licenses/>.

## Credit

This project is achieved with Python, and Python library ``pygame``. Part of the code is inspired by the official guide of ``pygame``.

## Usage

### Running the program

Run the program with:

```Python
python main.py [-m] [-z]
```

The ``-m`` is for center-based throttle profiles, and should be followed by a float number to indicate the center position. Some games have two-way throttle, mostly space flight sim or other games with both forward and reverse movement ability. When using this parameter, the profile should be set up **the same way** as normal throttle profile, **do not use negative number** to represent the reversing part. The ``-z`` is for normal profiles. Either one of these parameters must be set.

After running you should get a window showing the bars indicating throttle position. This project is designed for Logitech X56 throttle, so if you’re using any other throttle device make sure to change the searching criteria and the axis number of the device.

If you hope to use it in VR, there’re tools like ``Desktop+`` that can show a window from desktop at somewhere you designate. Refer to their guides and manuals for further details on how to do so.

### Configuration profile

This program requires a configuration profile located at the same place as the Python script named ``profile.txt`` to run. In it are details of the throttle profile, including different percentages of different throttle positions, and the desired color. The format of the configuration file should be:

```Config
[Position][Haptic] [Name] [Percentage] [R] [G] [B]
```

Separated with space, and in the order from idle to maximum. Each item should be separated with new line. The haptic option can be P(positive), N(negative), D(detent) or left empty. A positive detent means the detent only triggers when the throttle moves forward, like it would at the afterburner position; vice versa, a negative detent resembles the detent between idle and off position. A normal detent triggers both way, like what you would expect in a space sim. For example, if idle on left throttle is 15%, with negative detent, and the color should be red, then the configuration file should be:

```Config
LN idle 0.15 255 0 0
```

### Build and install the vibration module

Still waiting for my components. I’ll update this when I receive them.

## Version history

- V1.0: Program is runnable, no exception handling ability. User is required to ensure all input is correct.
- V2.0: Added center-based indication for two-way throttle control.
- V3.0: Added haptic virtual detent feed back.

## Future plans

- Finish exception handling and optimization.
- Add GUI start up mode for shortcut start up.
- Add support for electromagnetic detent mod.
