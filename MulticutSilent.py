import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

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

input_audio_path = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\TEST\TEST.wav"
output_directory = r"C:\Users\Kin Tu\Documents\RecordProcessing\Audio\TEST\Processed"

split_and_save_audio(input_audio_path, output_directory)
