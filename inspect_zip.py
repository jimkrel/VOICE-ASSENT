import zipfile
import os

zip_path = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu\thiet-ke-ui-ux-tieng-viet.zip"
print(f"Path: {zip_path}")
if os.path.exists(zip_path):
    print(f"File exists, size={os.path.getsize(zip_path)} bytes")
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            print(f"  {info.filename} ({info.file_size} bytes)")
else:
    print("File does not exist!")
    # Check parent directory
    parent = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu"
    if os.path.exists(parent):
        print(f"Parent directory contents: {os.listdir(parent)}")
    else:
        print(f"Parent directory does not exist: {parent}")
