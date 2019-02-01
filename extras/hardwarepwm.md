---
layout: plugin

id: hardwarepwm
title: OctoPrint-Hardwarepwm
description: TODO
author: Dario Rostirolla
license: AGPLv3

date: 2019-02-01

homepage: https://github.com/you/OctoPrint-Hardwarepwm
source: https://github.com/you/OctoPrint-Hardwarepwm
archive: https://github.com/you/OctoPrint-Hardwarepwm/archive/master.zip

tags:
- hardware pwm
- control
- pwm
- leds

screenshots:
- url: settingsPage.png
  alt: settings page
  caption: Settings page
- url: tabPage.png
  alt: tab page
  caption: Tab page
- ...

featuredimage: tabPage.png

compatibility:

  octoprint:
  - 1.2.0

  os:
  - linux

---

Plugin that uses the PIGPIO library for hardware PWM, thus creating a flicker free pwm signal for LED strip dimming. Requires you to install pigpio through apt-get and to start/enable the pigpiod daemon.
