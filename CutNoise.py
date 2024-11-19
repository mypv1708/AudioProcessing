import os
from pydub import AudioSegment

# Đường dẫn tới thư mục chứa các file âm thanh
input_folder = r"E:\Dataset21ad\Audio\Audio\Thân Thiện"
output_folder = r"E:\Dataset21ad\Audio\Audio\Thân Thiện"

# Tạo thư mục đầu ra nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Thời lượng cần cắt (tính bằng milliseconds)
cut_start_duration = 400  # Cắt đoạn đầu (0.4 giây)
cut_end_duration =  0 # Cắt đoạn cuối (0.6 giây)

for file_name in os.listdir(input_folder):
    if file_name.endswith("Thân thiện.wav"):
        file_path = os.path.join(input_folder, file_name)
        audio = AudioSegment.from_wav(file_path)
        
        # Thời lượng file gốc
        original_duration = len(audio)  # Tính bằng milliseconds
        
        # Đảm bảo không cắt vượt quá thời lượng file
        start = cut_start_duration
        end = original_duration - cut_end_duration
        
        if start >= end:
            print(f"Bỏ qua file {file_name}: Thời lượng quá ngắn để cắt.")
            continue
        
        # Cắt đoạn đầu và đoạn cuối
        trimmed_audio = audio[start:end]
        
        # Lưu file mới
        output_path = os.path.join(output_folder, file_name)
        trimmed_audio.export(output_path, format="wav")
        print(f"Processed: {file_name} -> {output_path}")

print("Hoàn thành cắt nhiễu.")
