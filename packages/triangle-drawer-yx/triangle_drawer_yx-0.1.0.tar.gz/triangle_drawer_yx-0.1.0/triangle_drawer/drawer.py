from termcolor import colored

def draw_triangle(layers, color='white', inverted=False):
    """
    画一个带颜色的等腰三角形或倒等腰三角形。

    参数:
    layers: 三角形的层数
    color: 星号的颜色，默认值为'white'
    inverted: 是否绘制倒三角形，默认为False（正三角形）
    """
    if inverted:
        # 绘制倒三角形
        for i in range(layers, 0, -1):
            print(colored(' ' * (layers - i) + '* ' * i, color))
    else:
        # 绘制正三角形
        for i in range(1, layers + 1):
            print(colored(' ' * (layers - i) + '* ' * i, color))

# 示例调用
draw_triangle(5, 'cyan')  # 打印青色的正三角形
draw_triangle(3)  # 打印默认白色的正三角形
draw_triangle(5, 'red', inverted=True)  # 打印红色的倒三角形
draw_triangle(4, inverted=True)  # 打印默认白色的倒三角形
