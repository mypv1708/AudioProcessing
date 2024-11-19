import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import matplotlib.cm as cm

# Đường dẫn thư mục chứa các tệp âm thanh
input_folder = r"E:\Dataset21ad\Audio\Mệt Mỏi"

# File để lưu tên các tệp âm thanh không vừa ý
note_file = "note.txt"

# Hàm để lưu tên file không vừa ý vào file note.txt
def mark_file(event, filename):
    with open(note_file, "a", encoding="utf-8") as f:  # Specify utf-8 encoding
        f.write(f"{filename}\n")
    print(f"{filename} đã được lưu vào {note_file}")

# Lặp qua tất cả các tệp trong thư mục
for filename in os.listdir(input_folder):
    # Chỉ xử lý các tệp .wav
    if filename.endswith(".wav"):
        input_path = os.path.join(input_folder, filename)
        
        # Load file âm thanh
        y, sr = librosa.load(input_path, sr=16000)
        
        # Tính toán spectrogram
        S = librosa.stft(y)
        S_db = librosa.amplitude_to_db(abs(S), ref=np.max)
        
        # Hiển thị spectrogram với các cài đặt cải tiến
        fig, ax = plt.subplots(figsize=(6, 4))  # Tăng kích thước hình ảnh
        img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', cmap='plasma', ax=ax)  # Dùng colormap đẹp hơn
        
        # Tạo colorbar từ mappable
        cbar = fig.colorbar(img, ax=ax, format='%+2.0f dB')
        cbar.set_label('Intensity (dB)', fontsize=12, weight='bold')  # Nhãn cho colorbar
        
        ax.set_ylim(0, 8000)  # Giới hạn tần số hiển thị để dễ nhìn hơn
        ax.set_title(f"Spectrogram - {filename}", fontsize=16, weight='bold', color='darkblue')  # Tiêu đề nổi bật
        ax.set_xlabel("Time (s)", fontsize=14, weight='bold', color='darkgreen')
        ax.set_ylabel("Frequency (Hz)", fontsize=14, weight='bold', color='darkgreen')
        ax.tick_params(axis='both', labelsize=12, colors='black')
        ax.grid(True, linestyle='--', alpha=0.5)  # Thêm grid nhẹ để dễ quan sát
        
        # Thêm nút để đánh dấu file âm thanh
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])  # Vị trí nút
        button = Button(ax_button, 'Mark', color='red', hovercolor='orange')
        button.on_clicked(lambda event, filename=filename: mark_file(event, filename))

        # Center the figure on the screen
        mngr = plt.get_current_fig_manager()
        mngr.window.geometry("+%d+%d" % (100, 100))  # Change 100, 100 to your desired position

        plt.tight_layout()
        plt.show()
