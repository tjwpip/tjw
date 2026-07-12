import os

def fix_pkg_info():
    pkg_info_path = os.path.join(os.path.dirname(__file__), "tjw.egg-info", "PKG-INFO")
    if not os.path.exists(pkg_info_path):
        print("PKG-INFO not found")
        return
    
    with open(pkg_info_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 删除废弃的字段
    new_lines = []
    for line in lines:
        if line.startswith("License-File:") or line.startswith("Dynamic: license-file"):
            continue
        new_lines.append(line)
    
    with open(pkg_info_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("Fixed PKG-INFO")

if __name__ == "__main__":
    fix_pkg_info()