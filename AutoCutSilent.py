import os
import librosa
import soundfile as sf

input_folder = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\Thân Thiện\Processed\Câu5"
output_folder = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\Thân Thiện\Processed\Câu5_Cut4"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if ".wav" in filename and filename.endswith(".wav"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        y, sr = librosa.load(input_path, sr=16000)

        y_trimmed, _ = librosa.effects.trim(y, top_db=19)

        sf.write(output_path, y_trimmed, sr)
        print(f"Đã xử lý và lưu: {output_path}")

print("Hoàn tất xử lý")
