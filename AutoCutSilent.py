import os
import librosa
import soundfile as sf

input_folder = r"ValidateAudio\Thân Thiện"
output_folder = r"ValidateAudioProcessed\Thân Thiện"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if ".wav" in filename and filename.endswith(".wav"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        y, sr = librosa.load(input_path, sr=16000)

        y_trimmed, _ = librosa.effects.trim(y, top_db=26)

        sf.write(output_path, y_trimmed, sr)
        print(f"Đã xử lý và lưu: {output_path}")

print("Hoàn tất xử lý tất cả các tệp chứa 'Mệt Mỏi'.")
