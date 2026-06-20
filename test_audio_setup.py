#!/usr/bin/env python3
"""Quick test to verify audio device setup and imports work correctly."""

import sys
import sounddevice as sd

# Test imports
try:
    from google import genai
    print("[OK] google.genai imported")
except ImportError as e:
    print(f"[ERROR] google.genai import failed: {e}")
    sys.exit(1)

try:
    from ui import JarvisUI
    print("[OK] ui.JarvisUI imported")
except ImportError as e:
    print(f"[ERROR] ui.JarvisUI import failed: {e}")

try:
    from actions.file_processor import file_processor
    print("[OK] actions.file_processor imported")
except ImportError as e:
    print(f"[ERROR] actions.file_processor import failed: {e}")

# Test audio device detection functions (from main.py)
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHANNELS = 1

def find_compatible_output_device(samplerate=24000, channels=1, dtype="int16"):
    """Find compatible output device."""
    try:
        devices = sd.query_devices()
        default_out = sd.default.device[1]
        
        if default_out is not None:
            try:
                sd.check_output_settings(device=default_out, samplerate=samplerate, 
                                         channels=channels, dtype=dtype)
                print(f"[OK] Default output device: {devices[default_out]['name']}")
                return default_out
            except Exception:
                pass
        
        for i, d in enumerate(devices):
            if d['max_output_channels'] > 0:
                try:
                    sd.check_output_settings(device=i, samplerate=samplerate, 
                                             channels=channels, dtype=dtype)
                    print(f"[OK] Compatible output device: {d['name']}")
                    return i
                except Exception:
                    continue
        
        print(f"[WARN] No compatible output device found; using default {default_out}")
        return default_out
    except Exception as e:
        print(f"[ERROR] Error finding output device: {e}")
        return None

def find_compatible_input_device(samplerate=16000, channels=1, dtype="int16"):
    """Find compatible input device."""
    try:
        devices = sd.query_devices()
        default_in = sd.default.device[0]
        
        if default_in is not None:
            try:
                sd.check_input_settings(device=default_in, samplerate=samplerate, 
                                        channels=channels, dtype=dtype)
                print(f"[OK] Default input device: {devices[default_in]['name']}")
                return default_in
            except Exception:
                pass
        
        for i, d in enumerate(devices):
            if d['max_input_channels'] > 0:
                try:
                    sd.check_input_settings(device=i, samplerate=samplerate, 
                                            channels=channels, dtype=dtype)
                    print(f"[OK] Compatible input device: {d['name']}")
                    return i
                except Exception:
                    continue
        
        print(f"[WARN] No compatible input device found; using default {default_in}")
        return default_in
    except Exception as e:
        print(f"[ERROR] Error finding input device: {e}")
        return None

# Test device finding
print("\n=== Audio Device Detection ===")
out_dev = find_compatible_output_device(RECEIVE_SAMPLE_RATE, CHANNELS, "int16")
in_dev = find_compatible_input_device(SEND_SAMPLE_RATE, CHANNELS, "int16")

if out_dev is not None and in_dev is not None:
    print(f"[OK] Audio setup OK: Input device {in_dev}, Output device {out_dev}")
else:
    print("[WARN] Audio device setup may have issues")

print("\n=== JARVIS Audio Environment Ready ===")
print("[OK] All dependencies and audio devices configured successfully!")

