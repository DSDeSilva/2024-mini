#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

# Twinkle Twinkle Little Star

playtone(523, .3)  # C
playtone(523, .3)  # C
playtone(783, .3)  # G
playtone(783, .3)  # G
playtone(880, .3)  # A
playtone(880, .3)  # A
playtone(783, .6)  # G

playtone(698, .3)  # F
playtone(698, .3)  # F
playtone(659, .3)  # E
playtone(659, .3)  # E
playtone(587, .3)  # D
playtone(587, .3)  # D
playtone(523, .6)  # C

playtone(783, .3)  # G
playtone(783, .3)  # G
playtone(698, .3)  # F
playtone(698, .3)  # F
playtone(659, .3)  # E
playtone(659, .3)  # E
playtone(587, .6)  # D

playtone(783, .3)  # G
playtone(783, .3)  # G
playtone(698, .3)  # F
playtone(698, .3)  # F
playtone(659, .3)  # E
playtone(659, .3)  # E
playtone(587, .6)  # D

playtone(523, .3)  # C
playtone(523, .3)  # C
playtone(783, .3)  # G
playtone(783, .3)  # G
playtone(880, .3)  # A
playtone(880, .3)  # A
playtone(783, .6)  # G

playtone(698, .3)  # F
playtone(698, .3)  # F
playtone(659, .3)  # E
playtone(659, .3)  # E
playtone(587, .3)  # D
playtone(587, .3)  # D
playtone(523, .6)  # C

# Turn off the PWM
quiet()
