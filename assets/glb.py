import os

# 你的模型文件夹路径（不用改）
folder_path = r"F:\game\museum\assets"

# 检查文件夹是否存在
if not os.path.exists(folder_path):
    print(f"错误：文件夹不存在 {folder_path}")
    input("按回车退出")
    exit()

# 获取所有 glb 文件（排除已改名的数字文件，避免重复执行出错）
glb_files = []
for f in os.listdir(folder_path):
    if f.lower().endswith(".glb"):
        # 跳过已经是 01.glb / 02.glb 格式的文件
        if f[:-4].isdigit():
            continue
        glb_files.append(f)

glb_files.sort()  # 按字母排序

if not glb_files:
    print("没有找到需要重命名的 glb 文件！")
    input("按回车退出")
    exit()

# 开始重命名 + 记录名字
name_list = []
for index, old_name in enumerate(glb_files, start=1):
    # 新名字：01.glb, 02.glb...
    new_name = f"{index:02d}.glb"
    
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)
    
    # 重命名文件
    os.rename(old_path, new_path)
    
    # 记录到列表：1.名字.glb
    name_list.append(f"{index}.{old_name}")
    print(f"已重命名：{old_name} -> {new_name}")

# 写入 name.txt，格式：1.glb,2.glb...
txt_content = ",".join(name_list)
txt_path = os.path.join(folder_path, "name.txt")

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(txt_content)

print("\n✅ 完成！")
print(f"📄 名字列表已保存到：{txt_path}")
print(f"🔢 共处理 {len(glb_files)} 个文件")
input("\n按回车退出")