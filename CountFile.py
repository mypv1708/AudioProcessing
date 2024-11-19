import os

def count_wav_files_by_folder(directory_path):
    # Biến lưu tổng số tệp .wav trong tất cả các thư mục
    total_wav_count = 0
    
    # Duyệt qua các tệp trong đường dẫn
    for root, dirs, files in os.walk(directory_path):
        wav_count = 0
        for file in files:
            # Kiểm tra nếu tệp có định dạng .wav
            if file.endswith('.wav'):
                wav_count += 1

        # Cộng số tệp .wav trong thư mục hiện tại vào tổng
        total_wav_count += wav_count

        # In ra đường dẫn của folder và số lượng file .wav trong folder đó
        print(f"Folder '{root}' có {wav_count} tệp .wav")
    
    # In tổng số tệp .wav
    print(f"Tổng số tệp .wav trong tất cả các folder: {total_wav_count}")


# Nhập đường dẫn từ người dùng
directory_path = input("Nhập đường dẫn cần kiểm tra: ")

# Đếm và in số lượng tệp .wav theo từng folder
count_wav_files_by_folder(directory_path)
