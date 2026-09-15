"""
Every sound here is generated at startup, so the game needs no audio
files.
"""

import array
import functools
import math
import random

import pygame


def mixer_format():
    """
    (sample rate, channel count), or None when there is no audio device.
    """

    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()

        rate, _, channels = pygame.mixer.get_init()

        return rate, abs(channels)

    except pygame.error:
        return None


def to_sound(samples, channels):
    """
    Turn mono samples into a playable Sound.
    """

    buffer = array.array("h")

    for value in samples:

        clipped = max(-32767, min(32767, int(value)))

        for _ in range(channels):
            buffer.append(clipped)

    return pygame.mixer.Sound(buffer=buffer.tobytes())


@functools.lru_cache(maxsize=None)
def make_beep(frequency=880, duration_ms=80, volume=0.2):
    """
    The blip for eating food.
    """

    fmt = mixer_format()

    if fmt is None:
        return None

    rate, channels = fmt

    count = int(rate * duration_ms / 1000)
    period = rate / frequency
    amplitude = 32767 * volume

    samples = []

    for index in range(count):

        value = amplitude if (index % period) < period / 2 else -amplitude

        # Fade the tail out so the beep does not click.
        fade = min(1.0, (count - index) / (rate * 0.01))

        samples.append(value * fade)

    return to_sound(samples, channels)


@functools.lru_cache(maxsize=None)
def make_explosion(duration_ms=700, volume=0.55):
    """
    The bomb: a noise burst over a falling rumble.
    """

    fmt = mixer_format()

    if fmt is None:
        return None

    rate, channels = fmt

    count = int(rate * duration_ms / 1000)
    amplitude = 32767 * volume

    samples = []

    # Low sweep, dropping from a thud to nothing.
    phase = 0.0

    for index in range(count):

        position = index / count

        # Sharp attack, long decay.
        envelope = min(1.0, position * 60) * (1.0 - position) ** 2.2

        frequency = 120 * (1.0 - position * 0.75)
        phase += 2 * math.pi * frequency / rate

        rumble = math.sin(phase)
        noise = random.uniform(-1.0, 1.0)

        samples.append(amplitude * envelope * (0.55 * rumble + 0.45 * noise))

    return to_sound(samples, channels)


# Minor pentatonic, which is why it sounds a little uneasy. Each bar is
# eight eighth notes of melody over one bass root, all in semitones
# from A3.
BARS = [
    (0, [0, 7, 12, 7, 3, 10, 15, 10]),
    (3, [0, 7, 12, 7, 5, 12, 17, 12]),
    (-2, [-2, 5, 10, 5, 3, 10, 15, 10]),
    (0, [0, 7, 12, 7, 7, 12, 15, 19]),
]

NOTE_MS = 220


def pitch(semitones):

    return 220.0 * (2 ** (semitones / 12))


@functools.lru_cache(maxsize=None)
def make_music(volume=0.12):
    """
    A short chiptune loop for the background.
    """

    fmt = mixer_format()

    if fmt is None:
        return None

    rate, channels = fmt

    count = int(rate * NOTE_MS / 1000)
    amplitude = 32767 * volume

    cache = {}

    def note(melody_semitone, bass_semitone):
        """
        One eighth note: square-wave melody over a square bass.
        """

        key = (melody_semitone, bass_semitone)

        if key in cache:
            return cache[key]

        melody_period = rate / pitch(melody_semitone)
        bass_period = rate / pitch(bass_semitone - 12)

        block = []

        for index in range(count):

            position = index / count

            # Plucked shape, and a gap before the next note.
            envelope = min(1.0, position * 25) * max(0.0, 1.0 - position) ** 1.3

            melody = 1.0 if (index % melody_period) < melody_period / 2 else -1.0
            bass = 1.0 if (index % bass_period) < bass_period * 0.35 else -1.0

            block.append(amplitude * envelope * (0.55 * melody + 0.45 * bass))

        cache[key] = block

        return block

    samples = []

    for root, melody in BARS:

        for step in melody:
            samples.extend(note(step, root))

    return to_sound(samples, channels)
