# 生成身份证号
import random
import datetime

class CShengFenZheng:
    def __init__(self):
        self.coll_diqu = {}
        self.guishudi_a = []
        self._init_diqu()
    
    def _init_diqu(self):
        diqu_data = [
            "110000 北京市",
            "110100 北京市市辖区",
            "110101 北京市东城区",
            "110102 北京市西城区",
            "110105 北京市朝阳区",
            "110106 北京市丰台区",
            "110107 北京市石景山区",
            "110108 北京市海淀区",
            "120000 天津市",
            "120100 天津市市辖区",
            "120101 天津市和平区",
            "120102 天津市河东区",
            "120103 天津市河西区",
            "120104 天津市南开区",
            "130000 河北省",
            "130100 河北省石家庄市",
            "130200 河北省唐山市",
            "130300 河北省秦皇岛市",
            "130400 河北省邯郸市",
            "130500 河北省邢台市",
            "130600 河北省保定市",
            "140000 山西省",
            "140100 山西省太原市",
            "140200 山西省大同市",
            "140300 山西省阳泉市",
            "150000 内蒙古自治区",
            "150100 内蒙古自治区呼和浩特市",
            "150200 内蒙古自治区包头市",
            "210000 辽宁省",
            "210100 辽宁省沈阳市",
            "210200 辽宁省大连市",
            "210300 辽宁省鞍山市",
            "220000 吉林省",
            "220100 吉林省长春市",
            "220200 吉林省吉林市",
            "230000 黑龙江省",
            "230100 黑龙江省哈尔滨市",
            "230200 黑龙江省齐齐哈尔市",
            "310000 上海市",
            "310100 上海市市辖区",
            "320000 江苏省",
            "320100 江苏省南京市",
            "320200 江苏省无锡市",
            "320300 江苏省徐州市",
            "320500 江苏省苏州市",
            "330000 浙江省",
            "330100 浙江省杭州市",
            "330200 浙江省宁波市",
            "330300 浙江省温州市",
            "340000 安徽省",
            "340100 安徽省合肥市",
            "340200 安徽省芜湖市",
            "350000 福建省",
            "350100 福建省福州市",
            "350200 福建省厦门市",
            "360000 江西省",
            "360100 江西省南昌市",
            "370000 山东省",
            "370100 山东省济南市",
            "370200 山东省青岛市",
            "410000 河南省",
            "410100 河南省郑州市",
            "410200 河南省开封市",
            "410300 河南省洛阳市",
            "420000 湖北省",
            "420100 湖北省武汉市",
            "420200 湖北省黄石市",
            "430000 湖南省",
            "430100 湖南省长沙市",
            "430200 湖南省株洲市",
            "440000 广东省",
            "440100 广东省广州市",
            "440300 广东省深圳市",
            "440600 广东省佛山市",
            "450000 广西壮族自治区",
            "450100 广西壮族自治区南宁市",
            "450200 广西壮族自治区柳州市",
            "460000 海南省",
            "460100 海南省海口市",
            "500000 重庆市",
            "500100 重庆市市辖区",
            "510000 四川省",
            "510100 四川省成都市",
            "510300 四川省自贡市",
            "520000 贵州省",
            "520100 贵州省贵阳市",
            "530000 云南省",
            "530100 云南省昆明市",
            "540000 西藏自治区",
            "540100 西藏自治区拉萨市",
            "610000 陕西省",
            "610100 陕西省西安市",
            "620000 甘肃省",
            "620100 甘肃省兰州市",
            "630000 青海省",
            "630100 青海省西宁市",
            "640000 宁夏回族自治区",
            "640100 宁夏回族自治区银川市",
            "650000 新疆维吾尔自治区",
            "650100 新疆维吾尔自治区乌鲁木齐市",
        ]
        
        self.guishudi_a = [""] + diqu_data
        for item in diqu_data:
            parts = item.split(" ", 1)
            if len(parts) == 2:
                code, name = parts
                self.coll_diqu[code] = name
    
    def _get_yzm(self, id_str):
        yzm_list = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        jqyz_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        
        total = 0
        for i in range(17):
            total += int(id_str[i]) * jqyz_list[i]
        
        remainder = total % 11
        return yzm_list[remainder]
    
    def _rnd_left1_6(self):
        if not self.guishudi_a:
            return "110000"
        
        index = random.randint(1, len(self.guishudi_a) - 1)
        item = self.guishudi_a[index]
        parts = item.split(" ", 1)
        return parts[0]
    
    def _rnd_year_month_day(self):
        today = datetime.date.today()
        current_year = today.year
        
        year = random.randint(current_year - 100, current_year - 18)
        month = random.randint(1, 12)
        
        if month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                max_day = 29
            else:
                max_day = 28
        else:
            max_day = 30
        
        day = random.randint(1, max_day)
        
        return f"{year:04d}{month:02d}{day:02d}"
    
    def _rnd_sn(self):
        return f"{random.randint(1, 999):03d}"
    
    def rnd_sfz18(self):
        left6 = self._rnd_left1_6()
        ymd = self._rnd_year_month_day()
        sn = self._rnd_sn()
        
        first17 = left6 + ymd + sn
        yzm = self._get_yzm(first17)
        
        return first17 + yzm
    
    def sfz_yz(self, id_str):
        errors = []
        
        id_str = id_str.replace(" ", "").upper()
        
        if len(id_str) != 18:
            errors.append("位数不对")
        
        if len(id_str) >= 17:
            yzm = self._get_yzm(id_str[:17])
            if yzm != id_str[-1]:
                errors.append("验证码不对")
            
            cs_date = id_str[6:14]
            try:
                cs_year = int(cs_date[:4])
                cs_month = int(cs_date[4:6])
                cs_day = int(cs_date[6:8])
                
                if cs_month < 1 or cs_month > 12:
                    errors.append("出生月不对")
                else:
                    if cs_month in [1, 3, 5, 7, 8, 10, 12]:
                        max_day = 31
                    elif cs_month == 2:
                        if (cs_year % 4 == 0 and cs_year % 100 != 0) or (cs_year % 400 == 0):
                            max_day = 29
                        else:
                            max_day = 28
                    else:
                        max_day = 30
                    
                    if cs_day < 1 or cs_day > max_day:
                        errors.append("出生日有误")
            except:
                errors.append("日期格式错误")
        
        return "\n".join(errors) if errors else ""
    
    def get_diqu(self, id_str):
        id_str = id_str.replace(" ", "")
        
        if len(id_str) >= 6:
            prefix = id_str[:6]
            if prefix in self.coll_diqu:
                return self.coll_diqu[prefix]
        
        return "未知地区"


# ==================== 测试菜单 ====================
def print_menu():
    print("=" * 50)
    print("          身份证工具测试菜单")
    print("=" * 50)
    print(" 1. 随机生成单个身份证")
    print(" 2. 批量生成身份证")
    print(" 3. 验证身份证有效性")
    print(" 4. 查询身份证归属地")
    print(" 5. 生成并验证（组合测试）")
    print(" 6. 显示API调用示例")
    print(" 0. 退出")
    print("=" * 50)

def generate_single(sfz):
    print("\n--- 随机生成身份证 ---")
    new_id = sfz.rnd_sfz18()
    print(f"生成结果: {new_id}")
    print(f"格式美化: {new_id[:6]} {new_id[6:14]} {new_id[14:]}")
    print(f"归属地: {sfz.get_diqu(new_id)}")
    verify_result = sfz.sfz_yz(new_id)
    print(f"验证状态: {'✓ 验证通过' if verify_result == '' else f'✗ 验证失败: {verify_result}'}")
    print("-" * 40)

def generate_batch(sfz):
    print("\n--- 批量生成身份证 ---")
    try:
        count = int(input("请输入生成数量: "))
        if count <= 0:
            print("数量必须大于0")
            return
        if count > 100:
            print("单次最多生成100个")
            count = 100
        
        print(f"\n正在生成 {count} 个身份证...")
        for i in range(count):
            new_id = sfz.rnd_sfz18()
            diqu = sfz.get_diqu(new_id)
            print(f"{i+1:3d}. {new_id} - {diqu}")
    except ValueError:
        print("请输入有效数字")
    print("-" * 40)

def verify_id(sfz):
    print("\n--- 验证身份证 ---")
    id_str = input("请输入18位身份证号: ").strip().replace(" ", "")
    
    if len(id_str) == 0:
        print("输入不能为空")
        return
    
    print(f"\n待验证身份证: {id_str}")
    result = sfz.sfz_yz(id_str)
    
    if result == "":
        print("✓ 验证通过！")
        print(f"归属地: {sfz.get_diqu(id_str)}")
        if len(id_str) >= 18:
            print(f"出生日期: {id_str[6:10]}年{id_str[10:12]}月{id_str[12:14]}日")
            print(f"性别: {'男' if int(id_str[16]) % 2 == 1 else '女'}")
    else:
        print(f"✗ 验证失败")
        print(f"错误信息:\n{result}")
    print("-" * 40)

def query_diqu(sfz):
    print("\n--- 查询归属地 ---")
    id_str = input("请输入身份证号（至少前6位）: ").strip().replace(" ", "")
    
    if len(id_str) < 6:
        print("至少需要输入6位")
        return
    
    diqu = sfz.get_diqu(id_str)
    print(f"\n身份证号: {id_str}")
    print(f"归属地: {diqu}")
    print("-" * 40)

def combined_test(sfz):
    print("\n--- 生成并验证（组合测试） ---")
    print("测试流程: 生成 → 验证 → 查询归属地")
    print("-" * 40)
    
    for i in range(5):
        print(f"\n测试 {i+1}:")
        new_id = sfz.rnd_sfz18()
        print(f"  生成: {new_id}")
        
        verify_result = sfz.sfz_yz(new_id)
        status = "✓ 通过" if verify_result == "" else "✗ 失败"
        print(f"  验证: {status}")
        
        diqu = sfz.get_diqu(new_id)
        print(f"  归属地: {diqu}")
    print("\n" + "-" * 40)

def show_examples():
    print("\n--- API调用示例 ---")
    print("""
# ==================== 基础用法 ====================
from createsfz import CShengFenZheng

# 1. 创建实例
sfz = CShengFenZheng()

# 2. 生成随机身份证
new_id = sfz.rnd_sfz18()
print(f"生成的身份证: {new_id}")

# 3. 验证身份证
result = sfz.sfz_yz("65432219850106181X")
if result == "":
    print("验证通过")
else:
    print(f"验证失败: {result}")

# 4. 查询归属地
diqu = sfz.get_diqu("110101199001011234")
print(f"归属地: {diqu}")

# ==================== 完整示例 ====================
sfz = CShengFenZheng()

# 生成并验证
id_card = sfz.rnd_sfz18()
print(f"身份证: {id_card}")
print(f"归属地: {sfz.get_diqu(id_card)}")
print(f"验证: {'通过' if sfz.sfz_yz(id_card) == '' else '失败'}")

# 解析身份证信息
if len(id_card) == 18:
    print(f"出生日期: {id_card[6:10]}-{id_card[10:12]}-{id_card[12:14]}")
    print(f"性别: {'男' if int(id_card[16]) % 2 == 1 else '女'}")
""")
    print("-" * 40)

def main():
    sfz = CShengFenZheng()
    
    while True:
        print_menu()
        try:
            choice = int(input("请选择操作 [0-6]: "))
            
            if choice == 0:
                print("感谢使用，再见！")
                break
            elif choice == 1:
                generate_single(sfz)
            elif choice == 2:
                generate_batch(sfz)
            elif choice == 3:
                verify_id(sfz)
            elif choice == 4:
                query_diqu(sfz)
            elif choice == 5:
                combined_test(sfz)
            elif choice == 6:
                show_examples()
            else:
                print("无效选项，请输入0-6")
            
            if choice != 0:
                input("\n按回车键继续...")
        except ValueError:
            print("请输入有效数字")

# 主函数
if __name__ == "__main__":
    main()