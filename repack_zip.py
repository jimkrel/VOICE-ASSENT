import os
import zipfile
import shutil

src_dir = r"E:\VoiceAI\extracted_ui_design"
zip_path = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu\thiet-ke-ui-ux-tieng-viet.zip"
backup_path = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu\thiet-ke-ui-ux-tieng-viet.backup.zip"
extracted_folder = r"C:\Users\jinnr\OneDrive\Desktop\Tài liệu\thiet-ke-ui-ux-tieng-viet"

# 1. Backup original zip if not already backed up
if not os.path.exists(backup_path) and os.path.exists(zip_path):
    shutil.copy2(zip_path, backup_path)
    print(f"Created backup at {backup_path}")

# 2. Build the new zip file from src_dir
if os.path.exists(zip_path):
    os.remove(zip_path)

print(f"Compressing updated files from {src_dir} into {zip_path}...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src_dir):
        # Exclude node_modules or .next if any
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.next' in dirs:
            dirs.remove('.next')
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, src_dir)
            z.write(full_path, rel_path)

print(f"Zip created successfully! Size: {os.path.getsize(zip_path)} bytes")

# 3. Also synchronize to unzipped folder on Desktop so user can inspect directly
if os.path.exists(extracted_folder):
    shutil.rmtree(extracted_folder)
os.makedirs(extracted_folder, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extracted_folder)

print(f"Extracted updated project to {extracted_folder}")
