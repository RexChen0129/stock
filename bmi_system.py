"""
BMI 系统 - 计算身体质量指数并提供健康建议
"""

def get_user_input():
    """获取用户的身高和体重输入"""
    print("\n" + "="*50)
    print("欢迎使用 BMI 计算系统")
    print("="*50)
    
    while True:
        try:
            height_cm = float(input("\n请输入您的身高 (厘米): "))
            if height_cm <= 0:
                print("❌ 身高必须大于0，请重新输入。")
                continue
            
            # 将厘米转换为米
            height = height_cm / 100
            
            weight = float(input("请输入您的体重 (公斤): "))
            if weight <= 0:
                print("❌ 体重必须大于0，请重新输入。")
                continue
            
            return height, weight
        except ValueError:
            print("❌ 输入错误，请输入有效的数字。")


def calculate_bmi(height, weight):
    """计算BMI值"""
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi):
    """根据BMI值返回分类和健康建议"""
    if bmi < 18.5:
        category = "偏瘦"
        advice = "• 增加营养摄入，多吃高热量食物\n• 进行适度的力量训练以增加肌肉\n• 定期体检以排除其他健康问题"
    elif 18.5 <= bmi < 24.9:
        category = "正常"
        advice = "• 保持现有的健康生活方式\n• 继续均衡饮食和规律运动\n• 每年进行一次体检"
    elif 25 <= bmi < 29.9:
        category = "超重"
        advice = "• 增加有氧运动，每周至少150分钟\n• 减少高热量食物和糖分摄入\n• 咨询营养师制定合理的饮食计划"
    else:  # bmi >= 30
        category = "肥胖"
        advice = "• 立即咨询医生或营养师\n• 制定科学的减肥计划\n• 增加体育运动，循序渐进\n• 改变不良饮食习惯"
    
    return category, advice


def display_result(height, weight, bmi, category, advice):
    """显示计算结果和健康建议"""
    height_cm = height * 100  # 将米转换回厘米显示
    print("\n" + "="*50)
    print("📊 BMI 计算结果")
    print("="*50)
    print(f"身高: {height_cm:.0f} 厘米")
    print(f"体重: {weight} 公斤")
    print(f"BMI值: {bmi}")
    print(f"分类: {category}")
    print("\n" + "-"*50)
    print("💡 健康建议：")
    print("-"*50)
    print(advice)
    print("="*50 + "\n")


def show_bmi_chart():
    """显示BMI分类表"""
    print("\n" + "="*50)
    print("📈 BMI 分类标准")
    print("="*50)
    print("BMI < 18.5        ➜ 偏瘦")
    print("18.5 ≤ BMI < 24.9 ➜ 正常")
    print("25 ≤ BMI < 29.9   ➜ 超重")
    print("BMI ≥ 30          ➜ 肥胖")
    print("="*50 + "\n")


def main():
    """主程序"""
    show_bmi_chart()
    
    while True:
        height, weight = get_user_input()
        bmi = calculate_bmi(height, weight)
        category, advice = get_bmi_category(bmi)
        display_result(height, weight, bmi, category, advice)
        
        again = input("是否继续计算？ (输入 'y' 继续，其他任何键退出): ").strip().lower()
        if again != 'y':
            print("\n感谢使用 BMI 计算系统，再见！👋\n")
            break


if __name__ == "__main__":
    main()
