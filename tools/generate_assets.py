#!/usr/bin/env python3
"""
翰墨精英 (Elite Business) - 华为表盘图片资源生成器
为 HUAWEI WATCH GT 系列生成 454x454 分辨率的表盘图片素材

设计风格：
- 白色/米白色底色，金色点缀
- 罗马数字时标
- 精细刻度环
- 优雅指针
- 商务数据面板
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# ========== 常量定义 ==========
SIZE = 454                    # 表盘分辨率
CENTER = SIZE // 2            # 中心点
RADIUS = SIZE // 2            # 半径

# 颜色定义
WHITE = (255, 255, 255, 255)
OFF_WHITE = (248, 245, 240, 255)       # 米白色表底
CREAM = (245, 240, 232, 255)           # 浅奶油色面板背景
GOLD = (201, 169, 110, 255)            # 金色（主色调）
GOLD_DARK = (168, 135, 80, 255)        # 深金色
GOLD_LIGHT = (220, 195, 150, 255)      # 浅金色
DARK_NAVY = (26, 26, 46, 255)          # 深藏青（文字主色）
CHARCOAL = (60, 60, 70, 255)           # 深灰
MEDIUM_GRAY = (102, 102, 102, 255)     # 中灰
LIGHT_GRAY = (200, 195, 188, 255)      # 浅灰
RED_ACCENT = (212, 55, 74, 255)        # 红色（心率）
GREEN_ACCENT = (74, 155, 90, 255)      # 绿色（电池）
BLUE_STEEL = (80, 100, 130, 255)       # 钢蓝色（秒针）
TRANSPARENT = (0, 0, 0, 0)

# 输出路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, "watchface", "watchface", "res")
PREVIEW_DIR = os.path.join(BASE_DIR, "watchface", "preview")
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def ensure_dirs():
    """确保所有输出目录存在"""
    dirs = [
        os.path.join(RES_DIR, "background"),
        os.path.join(RES_DIR, "hands"),
        os.path.join(RES_DIR, "icons"),
        os.path.join(RES_DIR, "icons", "week"),
        os.path.join(RES_DIR, "weather"),
        PREVIEW_DIR,
        DOCS_DIR,
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def draw_circle_point(cx, cy, radius, angle_deg):
    """计算圆上指定角度的点坐标（0度为12点方向，顺时针）"""
    angle_rad = math.radians(angle_deg - 90)
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)
    return x, y


# ========== 背景图生成 ==========
def generate_background():
    """生成表盘主背景 (bg_main.png)"""
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 外圈 - 深色边框
    draw.ellipse([2, 2, SIZE - 3, SIZE - 3], fill=CHARCOAL)
    # 金色外环
    draw.ellipse([6, 6, SIZE - 7, SIZE - 7], fill=GOLD)
    # 浅金色过渡环
    draw.ellipse([10, 10, SIZE - 11, SIZE - 11], fill=GOLD_LIGHT)
    # 白色表面
    draw.ellipse([16, 16, SIZE - 17, SIZE - 17], fill=OFF_WHITE)

    img.save(os.path.join(RES_DIR, "background", "bg_main.png"))
    print("  [OK] bg_main.png")
    return img


def generate_tick_ring():
    """生成刻度环 (tick_ring.png)"""
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    for i in range(60):
        angle = i * 6  # 每分钟6度
        if i % 5 == 0:
            # 整点刻度 - 粗长金色
            inner_r = RADIUS - 38
            outer_r = RADIUS - 20
            width = 3
            color = GOLD_DARK
        elif i % 1 == 0:
            # 分钟刻度 - 细短灰色
            inner_r = RADIUS - 28
            outer_r = RADIUS - 20
            width = 1
            color = LIGHT_GRAY

        x1, y1 = draw_circle_point(CENTER, CENTER, inner_r, angle)
        x2, y2 = draw_circle_point(CENTER, CENTER, outer_r, angle)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

    img.save(os.path.join(RES_DIR, "background", "tick_ring.png"))
    print("  [OK] tick_ring.png")
    return img


def generate_roman_numerals():
    """生成罗马数字时标 (roman_numerals.png)"""
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    numerals = {
        12: "XII", 1: "I", 2: "II", 3: "III",
        4: "IV", 5: "V", 6: "VI", 7: "VII",
        8: "VIII", 9: "IX", 10: "X", 11: "XI"
    }

    # 尝试加载字体
    font_large = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            font_large = ImageFont.truetype(fp, 32)
            break
    if font_large is None:
        try:
            font_large = ImageFont.truetype("DejaVuSerif-Bold", 32)
        except Exception:
            font_large = ImageFont.load_default()

    text_radius = RADIUS - 58

    for hour, numeral in numerals.items():
        angle = hour * 30
        x, y = draw_circle_point(CENTER, CENTER, text_radius, angle)

        bbox = draw.textbbox((0, 0), numeral, font=font_large)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        draw.text((x - tw / 2, y - th / 2), numeral,
                  fill=DARK_NAVY, font=font_large)

    img.save(os.path.join(RES_DIR, "background", "roman_numerals.png"))
    print("  [OK] roman_numerals.png")
    return img


def generate_inner_ring():
    """生成内圈装饰 (inner_ring.png)"""
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 内圈细金色装饰环
    r_inner = RADIUS - 75
    draw.ellipse(
        [CENTER - r_inner, CENTER - r_inner,
         CENTER + r_inner, CENTER + r_inner],
        outline=GOLD_LIGHT, width=1
    )

    # 四个方位的小菱形装饰点
    for angle in [0, 90, 180, 270]:
        x, y = draw_circle_point(CENTER, CENTER, r_inner, angle)
        diamond_size = 4
        draw.polygon([
            (x, y - diamond_size),
            (x + diamond_size, y),
            (x, y + diamond_size),
            (x - diamond_size, y),
        ], fill=GOLD)

    img.save(os.path.join(RES_DIR, "background", "inner_ring.png"))
    print("  [OK] inner_ring.png")
    return img


def generate_center_cap():
    """生成表冠中心装饰 (center_cap.png)"""
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 外圈金色
    draw.ellipse([0, 0, 23, 23], fill=GOLD)
    # 内圈深色
    draw.ellipse([3, 3, 20, 20], fill=CHARCOAL)
    # 中心金色小点
    draw.ellipse([8, 8, 15, 15], fill=GOLD)

    img.save(os.path.join(RES_DIR, "background", "center_cap.png"))
    print("  [OK] center_cap.png")
    return img


# ========== 指针生成 ==========
def generate_hour_hand():
    """生成时针 (hour_hand.png)"""
    w, h = 28, 140
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    cx = w // 2
    # 指针主体 - 深藏青宽体箭头形
    points = [
        (cx - 6, h - 15),        # 左下（尾部）
        (cx - 7, h - 25),        # 左侧宽处
        (cx - 5, 30),            # 左侧中段
        (cx - 2, 8),             # 左侧尖端
        (cx, 0),                 # 尖端
        (cx + 2, 8),             # 右侧尖端
        (cx + 5, 30),            # 右侧中段
        (cx + 7, h - 25),        # 右侧宽处
        (cx + 6, h - 15),        # 右下（尾部）
    ]
    draw.polygon(points, fill=DARK_NAVY)

    # 金色中线装饰
    draw.line([(cx, 15), (cx, h - 30)], fill=GOLD, width=2)

    # 配重圆形尾部
    draw.ellipse([cx - 5, h - 15, cx + 5, h - 5], fill=DARK_NAVY)

    img.save(os.path.join(RES_DIR, "hands", "hour_hand.png"))
    print("  [OK] hour_hand.png")


def generate_minute_hand():
    """生成分针 (minute_hand.png)"""
    w, h = 20, 180
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    cx = w // 2
    # 指针主体 - 深藏青细长箭头形
    points = [
        (cx - 4, h - 20),
        (cx - 5, h - 30),
        (cx - 3, 25),
        (cx - 1, 5),
        (cx, 0),
        (cx + 1, 5),
        (cx + 3, 25),
        (cx + 5, h - 30),
        (cx + 4, h - 20),
    ]
    draw.polygon(points, fill=DARK_NAVY)

    # 金色中线
    draw.line([(cx, 12), (cx, h - 35)], fill=GOLD, width=1)

    # 配重
    draw.ellipse([cx - 3, h - 20, cx + 3, h - 14], fill=DARK_NAVY)

    img.save(os.path.join(RES_DIR, "hands", "minute_hand.png"))
    print("  [OK] minute_hand.png")


def generate_second_hand():
    """生成秒针 (second_hand.png)"""
    w, h = 8, 200
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    cx = w // 2
    # 秒针主体 - 钢蓝色极细
    draw.line([(cx, 0), (cx, h - 40)], fill=BLUE_STEEL, width=2)

    # 秒针尾部 - 稍粗的配重
    draw.line([(cx, h - 40), (cx, h - 10)], fill=BLUE_STEEL, width=3)

    # 配重圆
    draw.ellipse([cx - 4, h - 18, cx + 4, h - 10], fill=BLUE_STEEL)

    # 尖端小圆
    draw.ellipse([cx - 2, 0, cx + 2, 4], fill=RED_ACCENT)

    img.save(os.path.join(RES_DIR, "hands", "second_hand.png"))
    print("  [OK] second_hand.png")


# ========== 图标生成 ==========
def generate_icon_steps():
    """生成步数图标"""
    size = 20
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 简化的脚步图标 - 两个椭圆
    draw.ellipse([3, 2, 9, 10], fill=GOLD)
    draw.ellipse([10, 8, 16, 16], fill=GOLD)

    img.save(os.path.join(RES_DIR, "icons", "ic_steps.png"))
    print("  [OK] ic_steps.png")


def generate_icon_calories():
    """生成卡路里图标"""
    size = 20
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 火焰图标
    points = [
        (10, 1),
        (14, 7),
        (15, 12),
        (13, 17),
        (10, 19),
        (7, 17),
        (5, 12),
        (6, 7),
    ]
    draw.polygon(points, fill=(255, 140, 50, 255))
    # 内焰
    draw.ellipse([8, 10, 12, 16], fill=(255, 200, 80, 255))

    img.save(os.path.join(RES_DIR, "icons", "ic_calories.png"))
    print("  [OK] ic_calories.png")


def generate_icon_distance():
    """生成距离图标"""
    size = 20
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 定位针图标
    draw.ellipse([5, 2, 15, 12], outline=GOLD, width=2)
    draw.ellipse([8, 5, 12, 9], fill=GOLD)
    draw.polygon([(6, 10), (10, 18), (14, 10)], fill=GOLD)

    img.save(os.path.join(RES_DIR, "icons", "ic_distance.png"))
    print("  [OK] ic_distance.png")


def generate_icon_heart():
    """生成心率图标"""
    size = 18
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 心形
    draw.ellipse([1, 2, 9, 10], fill=RED_ACCENT)
    draw.ellipse([8, 2, 16, 10], fill=RED_ACCENT)
    draw.polygon([(2, 8), (9, 16), (16, 8)], fill=RED_ACCENT)

    img.save(os.path.join(RES_DIR, "icons", "ic_heart.png"))
    print("  [OK] ic_heart.png")


def generate_icon_battery():
    """生成电池图标"""
    size = 18
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 电池外框
    draw.rectangle([1, 4, 14, 14], outline=GREEN_ACCENT, width=1)
    # 电池正极
    draw.rectangle([14, 7, 16, 11], fill=GREEN_ACCENT)
    # 电量填充
    draw.rectangle([3, 6, 10, 12], fill=GREEN_ACCENT)

    img.save(os.path.join(RES_DIR, "icons", "ic_battery.png"))
    print("  [OK] ic_battery.png")


def generate_separator():
    """生成分隔符"""
    img = Image.new("RGBA", (2, 16), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw.line([(1, 2), (1, 14)], fill=LIGHT_GRAY, width=1)

    img.save(os.path.join(RES_DIR, "icons", "separator.png"))
    print("  [OK] separator.png")


# ========== 天气图标 ==========
def generate_weather_icons():
    """生成天气图标集"""
    weather_types = {
        "0": "sunny",      # 晴
        "1": "cloudy",     # 多云
        "2": "overcast",   # 阴
        "3": "rain",       # 雨
        "4": "snow",       # 雪
        "5": "fog",        # 雾
        "6": "wind",       # 风
        "7": "haze",       # 霾
    }

    size = 40
    sun_yellow = (255, 200, 50, 255)
    cloud_gray = (180, 180, 190, 255)
    rain_blue = (100, 150, 220, 255)
    snow_white = (220, 230, 245, 255)

    for idx, (code, name) in enumerate(weather_types.items()):
        img = Image.new("RGBA", (size, size), TRANSPARENT)
        draw = ImageDraw.Draw(img)

        if name == "sunny":
            # 太阳
            draw.ellipse([10, 10, 30, 30], fill=sun_yellow)
            for angle in range(0, 360, 45):
                x1, y1 = draw_circle_point(20, 20, 12, angle)
                x2, y2 = draw_circle_point(20, 20, 17, angle)
                draw.line([(x1, y1), (x2, y2)], fill=sun_yellow, width=2)

        elif name == "cloudy":
            # 太阳 + 云
            draw.ellipse([5, 5, 20, 20], fill=sun_yellow)
            draw.ellipse([12, 14, 28, 28], fill=cloud_gray)
            draw.ellipse([18, 12, 36, 30], fill=cloud_gray)
            draw.rectangle([14, 22, 34, 30], fill=cloud_gray)

        elif name == "overcast":
            # 云
            draw.ellipse([4, 10, 22, 26], fill=cloud_gray)
            draw.ellipse([14, 6, 34, 24], fill=cloud_gray)
            draw.rectangle([10, 18, 32, 28], fill=cloud_gray)

        elif name == "rain":
            # 云 + 雨滴
            draw.ellipse([6, 4, 20, 16], fill=cloud_gray)
            draw.ellipse([14, 2, 30, 16], fill=cloud_gray)
            draw.rectangle([10, 10, 28, 18], fill=cloud_gray)
            for rx in [12, 18, 24]:
                draw.line([(rx, 22), (rx - 2, 32)], fill=rain_blue, width=2)

        elif name == "snow":
            # 云 + 雪花
            draw.ellipse([6, 4, 20, 16], fill=cloud_gray)
            draw.ellipse([14, 2, 30, 16], fill=cloud_gray)
            draw.rectangle([10, 10, 28, 18], fill=cloud_gray)
            for sx in [12, 20, 28]:
                draw.ellipse([sx - 2, 24, sx + 2, 28], fill=snow_white)
                draw.ellipse([sx - 2, 32, sx + 2, 36], fill=snow_white)

        elif name == "fog":
            for fy in [10, 18, 26]:
                draw.line([(6, fy), (34, fy)], fill=cloud_gray, width=3)

        elif name == "wind":
            for wy, wlen in [(12, 30), (20, 24), (28, 28)]:
                draw.line([(6, wy), (6 + wlen, wy)], fill=MEDIUM_GRAY, width=2)
                # 弯曲尾部
                draw.arc([6 + wlen - 6, wy - 4, 6 + wlen + 2, wy + 4],
                         -90, 90, fill=MEDIUM_GRAY, width=2)

        elif name == "haze":
            for hy in [8, 16, 24, 32]:
                alpha = 180 - hy * 3
                haze_color = (160, 150, 130, max(alpha, 80))
                draw.line([(4, hy), (36, hy)], fill=haze_color, width=3)

        img.save(os.path.join(RES_DIR, "weather", f"{code}.png"))
    print("  [OK] weather icons (8 types)")


# ========== 星期图标 ==========
def generate_week_icons():
    """生成星期文字图标"""
    weekdays_cn = ["一", "二", "三", "四", "五", "六", "日"]

    # 尝试加载中文字体
    font = None
    cn_font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for fp in cn_font_paths:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 16)
            break
    if font is None:
        font = ImageFont.load_default()

    for i, day in enumerate(weekdays_cn):
        img = Image.new("RGBA", (50, 22), TRANSPARENT)
        draw = ImageDraw.Draw(img)

        text = f"周{day}"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((50 - tw) / 2, (22 - th) / 2 - 1), text,
                  fill=DARK_NAVY, font=font)

        img.save(os.path.join(RES_DIR, "icons", "week", f"{i + 1}.png"))
    print("  [OK] week icons (7 days)")


# ========== 预览图 ==========
def generate_preview():
    """生成表盘预览合成图"""
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)

    # 叠加各层
    layers = [
        "background/bg_main.png",
        "background/tick_ring.png",
        "background/roman_numerals.png",
        "background/inner_ring.png",
    ]

    for layer_path in layers:
        full_path = os.path.join(RES_DIR, layer_path)
        if os.path.exists(full_path):
            layer = Image.open(full_path).convert("RGBA")
            img = Image.alpha_composite(img, layer)

    draw = ImageDraw.Draw(img)

    # 加载字体
    font_medium = None
    font_small = None
    cn_font = None

    serif_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ]
    sans_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    cn_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    ]

    for fp in serif_paths:
        if os.path.exists(fp):
            font_medium = ImageFont.truetype(fp, 30)
            font_small = ImageFont.truetype(fp, 16)
            break
    if font_medium is None:
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    for fp in cn_paths:
        if os.path.exists(fp):
            cn_font = ImageFont.truetype(fp, 16)
            break
    if cn_font is None:
        cn_font = font_small

    # 天气区域
    weather_icon = os.path.join(RES_DIR, "weather", "0.png")
    if os.path.exists(weather_icon):
        wi = Image.open(weather_icon).convert("RGBA")
        img.paste(wi, (165, 118), wi)

    draw.text((210, 122), "24°C", fill=DARK_NAVY, font=font_small)
    draw.text((180, 158), "晴", fill=MEDIUM_GRAY, font=cn_font)

    # 日期面板（左）
    draw.rounded_rectangle([80, 200, 200, 254], radius=6,
                           fill=CREAM, outline=GOLD, width=1)
    draw.text((105, 204), "周五", fill=DARK_NAVY, font=cn_font)
    draw.text((100, 228), "02-06", fill=DARK_NAVY, font=font_small)

    # 日期面板（右）
    draw.rounded_rectangle([254, 200, 374, 254], radius=6,
                           fill=CREAM, outline=GOLD, width=1)
    draw.text((275, 204), "正月初九", fill=GOLD, font=cn_font)
    draw.text((285, 228), "巳时", fill=MEDIUM_GRAY, font=cn_font)

    # 数字时间
    font_digital = None
    for fp in sans_paths:
        if os.path.exists(fp):
            font_digital = ImageFont.truetype(fp, 34)
            break
    if font_digital is None:
        font_digital = font_medium

    time_text = "10:42"
    bbox = draw.textbbox((0, 0), time_text, font=font_digital)
    tw = bbox[2] - bbox[0]
    draw.text(((SIZE - tw) / 2, 288), time_text, fill=DARK_NAVY, font=font_digital)

    # 数据行 - 步数 | 卡路里 | 距离
    data_y = 338
    # 步数
    step_icon = os.path.join(RES_DIR, "icons", "ic_steps.png")
    if os.path.exists(step_icon):
        si = Image.open(step_icon).convert("RGBA")
        img.paste(si, (105, data_y), si)
    draw.text((128, data_y), "7645", fill=DARK_NAVY, font=font_small)

    # 分隔符
    draw.line([(202, data_y + 2), (202, data_y + 16)], fill=LIGHT_GRAY, width=1)

    # 卡路里
    cal_icon = os.path.join(RES_DIR, "icons", "ic_calories.png")
    if os.path.exists(cal_icon):
        ci = Image.open(cal_icon).convert("RGBA")
        img.paste(ci, (212, data_y), ci)
    draw.text((235, data_y), "328", fill=DARK_NAVY, font=font_small)

    # 分隔符
    draw.line([(285, data_y + 2), (285, data_y + 16)], fill=LIGHT_GRAY, width=1)

    # 距离
    dist_icon = os.path.join(RES_DIR, "icons", "ic_distance.png")
    if os.path.exists(dist_icon):
        di = Image.open(dist_icon).convert("RGBA")
        img.paste(di, (295, data_y), di)
    draw.text((318, data_y), "3.66", fill=DARK_NAVY, font=font_small)

    # 心率 + 电池行
    hl_y = 368
    heart_icon = os.path.join(RES_DIR, "icons", "ic_heart.png")
    if os.path.exists(heart_icon):
        hi = Image.open(heart_icon).convert("RGBA")
        img.paste(hi, (160, hl_y), hi)
    draw.text((182, hl_y), "97", fill=RED_ACCENT, font=font_small)

    bat_icon = os.path.join(RES_DIR, "icons", "ic_battery.png")
    if os.path.exists(bat_icon):
        bi = Image.open(bat_icon).convert("RGBA")
        img.paste(bi, (244, hl_y), bi)
    draw.text((265, hl_y), "80%", fill=GREEN_ACCENT, font=font_small)

    # 步数进度弧
    arc_bbox = [CENTER - 210, CENTER - 210, CENTER + 210, CENTER + 210]
    # 背景弧
    draw.arc(arc_bbox, 135, 225, fill=(*GOLD_LIGHT[:3], 100), width=3)
    # 进度弧 (假设76%进度)
    progress_angle = 135 + int(90 * 0.76)
    draw.arc(arc_bbox, 135, progress_angle, fill=GOLD, width=3)

    # 绘制指针
    # 时针 - 10:42 位置
    hour_angle = (10 + 42 / 60) * 30  # = 315度
    _draw_hand(img, CENTER, CENTER, hour_angle, 100, 6, DARK_NAVY, GOLD)

    # 分针 - 42分位置
    min_angle = 42 * 6  # = 252度
    _draw_hand(img, CENTER, CENTER, min_angle, 140, 4, DARK_NAVY, GOLD)

    # 秒针 - 30秒位置
    sec_angle = 30 * 6  # = 180度
    _draw_hand(img, CENTER, CENTER, sec_angle, 160, 2, BLUE_STEEL, None)

    # 中心装饰
    cap_img = os.path.join(RES_DIR, "background", "center_cap.png")
    if os.path.exists(cap_img):
        cap = Image.open(cap_img).convert("RGBA")
        img.paste(cap, (215, 215), cap)

    # 保存预览图
    # 转换为JPG（预览图需要JPG格式）
    preview_rgb = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    preview_rgb.paste(img, mask=img.split()[3])
    preview_rgb.save(os.path.join(PREVIEW_DIR, "cover.jpg"), "JPEG", quality=95)

    # 缩略图 (120x120)
    thumbnail = preview_rgb.resize((120, 120), Image.Resampling.LANCZOS)
    thumbnail.save(os.path.join(PREVIEW_DIR, "icon_small.jpg"), "JPEG", quality=90)

    # 同时保存PNG用于文档
    img.save(os.path.join(DOCS_DIR, "preview_full.png"))

    print("  [OK] cover.jpg, icon_small.jpg, preview_full.png")
    return img


def _draw_hand(img, cx, cy, angle_deg, length, width, color, accent_color):
    """在预览图上绘制指针"""
    draw = ImageDraw.Draw(img)
    angle_rad = math.radians(angle_deg - 90)

    # 指针末端（指向方向）
    end_x = cx + length * math.cos(angle_rad)
    end_y = cy + length * math.sin(angle_rad)

    # 指针尾端（反方向）
    tail_len = length * 0.15
    tail_x = cx - tail_len * math.cos(angle_rad)
    tail_y = cy - tail_len * math.sin(angle_rad)

    draw.line([(tail_x, tail_y), (end_x, end_y)], fill=color, width=width)

    # 金色中线
    if accent_color:
        mid_x = cx + (length * 0.3) * math.cos(angle_rad)
        mid_y = cy + (length * 0.3) * math.sin(angle_rad)
        end2_x = cx + (length * 0.85) * math.cos(angle_rad)
        end2_y = cy + (length * 0.85) * math.sin(angle_rad)
        draw.line([(mid_x, mid_y), (end2_x, end2_y)],
                  fill=accent_color, width=max(1, width - 2))


# ========== 主程序 ==========
def main():
    print("=" * 60)
    print("  翰墨精英 (Elite Business) - 表盘资源生成器")
    print("  目标分辨率: 454x454 (HWHD02)")
    print("=" * 60)

    ensure_dirs()

    print("\n[1/5] 生成背景图层...")
    generate_background()
    generate_tick_ring()
    generate_roman_numerals()
    generate_inner_ring()
    generate_center_cap()

    print("\n[2/5] 生成指针...")
    generate_hour_hand()
    generate_minute_hand()
    generate_second_hand()

    print("\n[3/5] 生成图标...")
    generate_icon_steps()
    generate_icon_calories()
    generate_icon_distance()
    generate_icon_heart()
    generate_icon_battery()
    generate_separator()

    print("\n[4/5] 生成天气和星期图标...")
    generate_weather_icons()
    generate_week_icons()

    print("\n[5/5] 生成预览图...")
    generate_preview()

    print("\n" + "=" * 60)
    print("  所有资源生成完成!")
    print(f"  资源目录: {RES_DIR}")
    print(f"  预览目录: {PREVIEW_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
