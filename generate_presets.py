import os
import math
from PIL import Image


def generate_preset(name, width, height, generator_func):
    img = Image.new('RGB', (width, height), color='black')
    pixels = img.load()
    center_x = (width-1) / 2
    center_y = (height-1) / 2

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            r = math.sqrt(dx*dx + dy*dy)

            max_r = (width / 2) * 0.95
            if r <= max_r:
                # angle from 0 to 2PI
                theta = math.atan2(dy, dx)
                if theta < 0:
                    theta += 2 * math.pi

                # Normalize r from 0 to 1
                norm_r = r / max_r

                val = generator_func(theta, norm_r)
                val_byte = int(max(0, min(255, val * 255)))
                pixels[x, y] = (val_byte, val_byte, val_byte)

    if not os.path.exists('presets'):
        os.makedirs('presets')

    img.save(f'presets/{name}.png')

# 1. Sine Wave: smooth 360 gradient


def sine_gen(theta, r):
    # (sin(theta) + 1) / 2 gives 0.0 to 1.0
    return (math.sin(theta) + 1.0) / 2.0

# 2. Square Wave: half white, half black


def square_gen(theta, r):
    return 1.0 if theta < math.pi else 0.0

# 3. Sawtooth Wave: 360 degree linear wrap


def saw_gen(theta, r):
    return theta / (2 * math.pi)

# 4. Major Chord (4:5:6)


def chord_gen(theta, r):
    ratios = [8, 10, 12, 15]

    id = r * len(ratios)
    ind = int(id) % len(ratios)
    f = id - ind

    if abs(f - 0.5) < 0.4:
        return (math.sin(ratios[ind] * theta) + 1.0) / 2.0
    return 0.0


if __name__ == "__main__":
    # print("Generating preset_sine.png...")
    # generate_preset('preset_sine', 1024, 1024, sine_gen)

    # print("Generating preset_square.png...")
    # generate_preset('preset_square', 1024, 1024, square_gen)

    # print("Generating preset_sawtooth.png...")
    # generate_preset('preset_sawtooth', 1024, 1024, saw_gen)

    print("Generating preset_chord.png...")
    generate_preset('preset_chord', 1024, 1024, chord_gen)

    print("Done!")
