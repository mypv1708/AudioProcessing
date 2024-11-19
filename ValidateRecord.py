import os
import pyaudio
import wave
import librosa
import soundfile as sf

# Cài đặt thông số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 4
CHUNK = 1024
RATE = 18000
WAVE_OUTPUT_FILENAME = "Validate.wav"

# Khởi tạo PyAudio
p = pyaudio.PyAudio()

# Mở stream ghi âm
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("*Recording")

frames = []

# Ghi âm trong RECORD_SECONDS
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("*Done recording")

# Kết thúc stream ghi âm
stream.stop_stream()
stream.close()
p.terminate()

# Lưu âm thanh vào file WAV tạm thời
temp_wave_filename = "temp_record.wav"
wf = wave.open(temp_wave_filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Tự động cắt đoạn yên lặng
output_filename = WAVE_OUTPUT_FILENAME  # File đầu ra sau khi cắt khoảng lặng
try:
    # Load âm thanh từ file WAV tạm thời
    y, sr = librosa.load(temp_wave_filename, sr=RATE)

    # Cắt khoảng lặng
    y_trimmed, _ = librosa.effects.trim(y, top_db=30)

    # Lưu âm thanh đã cắt vào file đầu ra
    sf.write(output_filename, y_trimmed, sr)
    print(f"Đã ghi âm và lưu file sau khi cắt khoảng lặng: {output_filename}")

finally:
    # Xóa file WAV tạm thời
    if os.path.exists(temp_wave_filename):
        os.remove(temp_wave_filename)
