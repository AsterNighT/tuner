# Tuner

Tuner gives the pitch of what your computer is playing. But, it is now very inaccurate.

## How to run

```bash
python pitcher.py
```

## How it works

It reads from WASAPI loopback device (This part is from [pyaudiowpatch](https://github.com/s0d3s/PyAudioWPatch)). It then feeds the data to [crepe](https://github.com/marl/crepe) and gets a prediction.

## Known issues

1. It only works well on pure sound. Standard notes and pure vocal seem to be processible, while hard rock musics are not.
2. The results are not stable, and not easy to read.
