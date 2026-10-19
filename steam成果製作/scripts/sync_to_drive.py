import os, shutil

drive_root = r"G:\我的雲端硬碟\steam社群申請"
local_root = r"d:\antui\steam成果製作"

files_map = {
    "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx": ["總核銷清冊.docx", "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx"],
    "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf": ["總核銷清冊.pdf", "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf"],
    "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx": ["成果總表.docx", "活動成果總表.docx", "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx"],
    "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf": ["成果總表.pdf", "活動成果總表.pdf", "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf"],
}

# 1. Root of Google Drive
for src_fn, dst_names in files_map.items():
    src_path = os.path.join(local_root, src_fn)
    if os.path.exists(src_path):
        for dst_fn in dst_names:
            dst_path = os.path.join(drive_root, dst_fn)
            shutil.copy2(src_path, dst_path)
            print(f"Copied to Drive root: {dst_fn} ({os.path.getsize(dst_path)} bytes)")

# 2. Dedicated subfolder: 總核銷清冊與成果總表
sub_dir = os.path.join(drive_root, "總核銷清冊與成果總表")
os.makedirs(sub_dir, exist_ok=True)
for src_fn, dst_names in files_map.items():
    src_path = os.path.join(local_root, src_fn)
    if os.path.exists(src_path):
        for dst_fn in dst_names:
            dst_path = os.path.join(sub_dir, dst_fn)
            shutil.copy2(src_path, dst_path)
            print(f"Copied to Drive subfolder: {dst_fn}")

print("Sync completed!")
