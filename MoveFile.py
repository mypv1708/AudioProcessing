import os
import shutil

# Đường dẫn thư mục chứa các tệp âm thanh và thư mục Next
input_folder = r"Vui Vẻ"
next_folder = os.path.join(input_folder, "Next")

# Tạo thư mục Next nếu chưa có
if not os.path.exists(next_folder):
    os.makedirs(next_folder)

# Đọc các tên tệp đã lưu trong note.txt
with open("note.txt", "r", encoding="utf-8") as f:
    note_files = f.readlines()

# Lặp qua các tên tệp trong note.txt
for line in note_files:
    # Lấy tên tệp, bỏ ký tự xuống dòng
    filename = line.strip()
    
    # Kiểm tra nếu tệp tồn tại trong thư mục input_folder
    input_path = os.path.join(input_folder, filename)
    if os.path.exists(input_path):
        # Di chuyển tệp vào thư mục Next
        new_path = os.path.join(next_folder, filename)
        shutil.move(input_path, new_path)
        print(f"Đã di chuyển tệp {filename} từ {input_path} đến {new_path}")
    else:
        print(f"Tệp {filename} không tồn tại trong thư mục {input_folder}")
