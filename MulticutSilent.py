import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa
import soundfile as sf

def split_and_save_audio(input_audio, output_dir, min_silence_len=800, silence_thresh=-58):
    audio = AudioSegment.from_wav(input_audio)
    
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Tìm thấy {len(chunks)} đoạn âm thanh.")
    
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f"chunk_{i+1}.wav")
        chunk.export(output_path, format="wav")
        print(f"Lưu đoạn âm thanh {i+1} tại: {output_path}")

def process_audio_files(input_folder, output_folder, sr=16000, top_db=18):
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load file âm thanh
            y, sr = librosa.load(input_path, sr=sr)

            # Cắt bỏ đoạn im lặng
            y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)

            # Lưu file đã xử lý
            sf.write(output_path, y_trimmed, sr)
            print(f"Đã xử lý và lưu: {output_path}")

    print("Hoàn tất xử lý tất cả file.")



input_audio_path = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\Thân Thiện\Thân Thiện_Câu 6_TEST.wav"
output_directory = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\Thân Thiện\Processed\Câu6"
output_folder = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\Thân Thiện\Processed\Câu6_Cut10"

split_and_save_audio(input_audio_path, output_directory)
process_audio_files(output_directory, output_folder, sr=16000, top_db=18)

