import zipfile
import os

zip_path = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu\thiet-ke-ui-ux-tieng-viet.zip"
out_dir = r"E:\VoiceAI\extracted_ui_design"

os.makedirs(out_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(out_dir)

print(f"Extracted to {out_dir}")
for root, dirs, files in os.walk(out_dir):
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, out_dir)
        print(f"  {rel} ({os.path.getsize(p)} bytes)")
