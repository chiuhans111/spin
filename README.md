# Spin

A WebGL simulation of rotation and camera shutter effects (wagon-wheel, rolling shutter) with real-time speed-synchronized audio synthesis.

Live: [https://chiuhans111.github.io/spin/](https://chiuhans111.github.io/spin/)

## Setup

Run a simple local HTTP server:

```bash
# using Node.js
npx serve
```

## Features

- **Shutter Simulation**: Simulates global and rolling shutter delays in real-time.
- **Audio Synthesis**: Synthesizes mechanical hum, rattle, and wind noise using Web Audio API, dynamically matching the rotation speed (RPM).
- **Custom Textures**: Paste images from clipboard (`Ctrl + V`), drag and drop image files, or select from built-in presets.
- **HD Video Recording**: Record both the visual canvas and synthesized audio directly into `.mp4` (H.264 + AAC) or `.webm` files.
- **FPS & Physics Controls**: Fine-tune acceleration, max RPM, shutter speed, rolling delay, and target frame rate.

## How it works

### Physics & Rendering

1. **Polar & Linear RGB Mapping**: The input image is converted into polar coordinates $(r, \theta)$ and decoded to linear RGB space.
2. **Prefix Sum Integration**: The polar linear RGB pixels are transformed into a horizontal prefix sum table.
3. **Buffer Packing**: The prefix sums are stored across 3 separate integration buffers (to represent the range of integral values).
4. **General Motion Blur (LUT)**: These 3 buffers are combined into a Look-Up Table (LUT). The WebGL shader queries this LUT for any arbitrary range sum in $O(1)$ constant time, generalizing motion blur to any rotational speed.
5. **Small Blur Fallback**: For small rotation angles where prefix sum rounding errors might occur, the system falls back to fast brute-force sampling.

### Sound Synthesis

- **Wavetable Sonification**: A 1D density profile is extracted by integrating the source image's slices. This profile is loaded dynamically into an audio buffer as a custom wavetable. The Web Audio API cycles this wavetable, scaling playback rate and filters in real-time based on the active RPM.

## License

MIT / Public Domain.
