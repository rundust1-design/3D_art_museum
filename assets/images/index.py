import os
import shutil

SRC_DIR = r"F:\game\museum\assets\images\new_images"
DST_DIR = r"F:\game\museum\assets\images"
TXT_PATH = r"F:\game\museum\assets\images\name.txt"
SUFFIX = (".jpg", ".jpeg", ".png", ".bmp")

def get_max_serial():
    if not os.path.exists(TXT_PATH):
        return 1
    max_num = 0
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            num_str = line.split(".",1)[0]
            if num_str.isdigit():
                n = int(num_str)
                if n>max_num:
                    max_num = n
    return max_num + 1

def run():
    idx = get_max_serial()
    files = [f for f in os.listdir(SRC_DIR) if f.lower().endswith(SUFFIX)]
    if not files:
        print("无图片")
        return

    for old_name in files:
        # 拆分原文件名与后缀
        _, ext = os.path.splitext(old_name)
        # 文件新名：序号.后缀（放到目标目录）
        new_file_name = f"{idx}{ext}"
        src = os.path.join(SRC_DIR, old_name)
        dst = os.path.join(DST_DIR, new_file_name)
        shutil.move(src, dst)
        # txt记录：序号.原全名（保存对应关系）
        txt_line = f"{idx}.{old_name}"
        with open(TXT_PATH, "a", encoding="utf-8") as f:
            f.write(txt_line+"\n")
        print(f"{old_name} → 文件:{new_file_name} | 存档:{txt_line}")
        idx += 1
    print("\n处理完毕")

if __name__ == "__main__":
    run()
