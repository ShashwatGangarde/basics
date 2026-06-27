import wave
import struct
import math

# Audio configuration
sample_rate = 44100.0
duration = 1.0 # 1 second beep
frequency = 1000.0 # 1000 Hz

# Create a wave file
wave_file = wave.open('alarm.wav', 'w')
wave_file.setnchannels(1) # mono
wave_file.setsampwidth(2) # 2 bytes
wave_file.setframerate(sample_rate)

# Generate sound data
for i in range(int(sample_rate * duration)):
    value = int(32767.0 * math.sin(frequency * math.pi * float(i) / float(sample_rate)))
    data = struct.pack('<h', value)
    wave_file.writeframesraw(data)

wave_file.close()
print("Generated alarm.wav")
