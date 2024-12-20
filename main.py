from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import librosa
import soundfile as sf
import numpy as np
import pandas as pd
from keras.models import model_from_json

# Tạo ứng dụng FastAPI
app = FastAPI()

# Load model đã huấn luyện
json_file_path = r'saved_models/emotion_detection_cnn.json'
weights_file_path = r'saved_models/emotion_detection_cnn.weights.h5'

with open(json_file_path, 'r') as json_file:
    loaded_model_json = json_file.read()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(weights_file_path)

# Thông số xử lý âm thanh
res_type_s = 'kaiser_best'
duration_s = None
sample_rate_s = 16000
sample_rate_mfcc = 16000
offset_s = 0.0
n_mfcc = 40
axis_mfcc = 1
emotions = ['Cáu Giận', 'Lạnh Lùng', 'Mệt Mỏi', 'Thân Thiện', 'Vui Vẻ']

# Hàm trích xuất đặc trưng
def extract_features(file_path):
    X, sample_rate = librosa.load(file_path, 
                                  res_type=res_type_s, 
                                  duration=duration_s, 
                                  sr=sample_rate_s, 
                                  offset=offset_s)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate_mfcc, n_mfcc=n_mfcc)
    mfccs_mean = np.mean(mfccs, axis=axis_mfcc)
    return mfccs_mean

# Dự đoán cảm xúc từ file WAV
def predict_emotion(file_path):
    try:
        features = extract_features(file_path)
        features_df = pd.DataFrame([features])
        prediction = loaded_model.predict(features_df)
        predicted_class = np.argmax(prediction, axis=1)
        return emotions[predicted_class[0]]
    except Exception as e:
        return f"Error: {e}"

# API nhận file WAV và xử lý
@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Lưu file tạm thời
        temp_input_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(temp_input_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Chia file thành các đoạn âm thanh
        temp_output_dir = "temp/output_chunks"
        os.makedirs(temp_output_dir, exist_ok=True)
        audio = AudioSegment.from_wav(temp_input_path)
        chunks = split_on_silence(
            audio,
            min_silence_len=800,
            silence_thresh=-58
        )

        chunk_paths = []
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(temp_output_dir, f"chunk_{i+1}.wav")
            chunk.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)

        # Xử lý cắt đoạn âm thanh không còn khoảng lặng
        processed_output_dir = "temp/processed"
        os.makedirs(processed_output_dir, exist_ok=True)
        for chunk_path in chunk_paths:
            y, sr = librosa.load(chunk_path, sr=sample_rate_s)
            y_trimmed, _ = librosa.effects.trim(y, top_db=18)
            output_path = os.path.join(processed_output_dir, os.path.basename(chunk_path))
            sf.write(output_path, y_trimmed, sr)

        # Dự đoán cảm xúc từng file
        predictions = []
        emotion_durations = {emotion: 0 for emotion in emotions}
        total_duration = 0

        for file_name in os.listdir(processed_output_dir):
            if file_name.endswith(".wav"):
                file_path = os.path.join(processed_output_dir, file_name)

                # Tính thời lượng của đoạn âm thanh
                y, sr = librosa.load(file_path, sr=sample_rate_s)
                duration = librosa.get_duration(y=y, sr=sr)
                total_duration += duration

                emotion = predict_emotion(file_path)
                predictions.append({
                    "file": file_name,
                    "emotion": emotion,
                    "duration": duration,
                })

                emotion_durations[emotion] += duration
        
        # Tính phần trăm cảm xúc
        emotion_percentages = {
        emotion: round((duration / total_duration) * 100, 2)
            for emotion, duration in emotion_durations.items()
            if duration > 0
        }

        # Trả về kết quả JSON
        return JSONResponse(content={"predictions_details": predictions,"emotion_percentages": emotion_percentages})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Dọn dẹp tệp tạm
        if os.path.exists("temp"):
            for root, dirs, files in os.walk("temp", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
