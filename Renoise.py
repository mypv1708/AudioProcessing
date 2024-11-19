import wave
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
import os

# Đường dẫn thư mục đầu vào chứa các file WAV
input_folder = "E:\Dataset21ad\Vui Vẻ"  # Thay "InputAudioFolder" bằng đường dẫn thư mục của bạn
output_dir = "E:\Dataset21ad\AudioRenoised\Vui Vẻ"  # Thư mục để lưu các file đã xử lý
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

# Hàm xử lý một file WAV
def process_wav(input_file, output_dir):
    try:
        # Đọc file WAV
        with wave.open(input_file, 'rb') as wf:
            RATE = wf.getframerate()
            CHANNELS = wf.getnchannels()
            FRAMES = wf.getnframes()
            audio_data = wf.readframes(FRAMES)
        
        # Chuyển đổi dữ liệu thành mảng numpy
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        # Giảm nhiễu sử dụng noisereduce
        reduced_noise = nr.reduce_noise(y=audio_np, sr=RATE, prop_decrease=0.7)
        
        # Tạo đường dẫn đầu ra
        input_filename = os.path.basename(input_file)  # Lấy tên file (vd: example.wav)
        output_file = os.path.join(output_dir, input_filename)
        
        # Chuyển tín hiệu giảm nhiễu thành file audio
        reduced_audio = AudioSegment(
            reduced_noise.tobytes(),
            frame_rate=RATE,
            sample_width=audio_np.itemsize,  # Kích thước mẫu của âm thanh
            channels=CHANNELS
        )
        
        # Lưu tín hiệu giảm nhiễu vào file WAV
        reduced_audio.export(output_file, format="wav")
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

# Lặp qua tất cả các tệp .wav trong thư mục và các thư mục con
for dirpath, dirnames, filenames in os.walk(input_folder):
    for filename in filenames:
        if filename.endswith(".wav"):  # Chỉ xử lý file .wav
            input_file = os.path.join(dirpath, filename)
            process_wav(input_file, output_dir)

print("All WAV files processed and saved!")
