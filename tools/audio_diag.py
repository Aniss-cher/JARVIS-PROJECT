import sounddevice as sd
import json

def safe(obj):
    try:
        return json.dumps(obj)
    except Exception:
        return str(obj)

print('Host APIs:')
for api in sd.query_hostapis():
    print('-', api.get('name'))

print('\nDefault device indices:', sd.default.device)

devs = sd.query_devices()
print('\nDevices:')
for i,d in enumerate(devs):
    print(i, d['name'], 'in:', d['max_input_channels'], 'out:', d['max_output_channels'])

TARGET_SR = 24000
TARGET_CH = 1
DTYPE = 'int16'

print(f"\nChecking output-capable devices for {TARGET_SR}Hz, {TARGET_CH}ch, {DTYPE} support:")
for i,d in enumerate(devs):
    if d['max_output_channels'] > 0:
        try:
            sd.check_output_settings(device=i, samplerate=TARGET_SR, channels=TARGET_CH, dtype=DTYPE)
            ok = 'OK'
        except Exception as e:
            ok = f'ERROR: {e}'
        print(i, d['name'], '->', ok)

print('\nCurrent default output device index:', sd.default.device[1])
print('Default sample rate reported by default device:', devs[sd.default.device[1]]['default_samplerate'] if sd.default.device[1] is not None else 'N/A')
