#!/usr/bin/env python3
"""
翰墨精英 (Elite Business) - 华为表盘图片资源生成器
为 HUAWEI WATCH GT 系列生成 454x454 分辨率的表盘图片素材

设计风格（参照蓝白商务表盘）：
- 白色/银色渐变底色（中心白，边缘略灰）
- 蓝色阿拉伯数字 1-12
- 蓝色小圆点分钟刻度环
- 深色指针带蓝色光泽
- 天气信息上方居中，带竖线分隔
- 左右两个细边框日期面板（农历+公历）
- 居中数字时间 + 步数/距离数据行 + 心率
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ========== 常量定义 ==========
SIZE = 454
CENTER = SIZE // 2
RADIUS = SIZE // 2

# 颜色定义 —— 蓝白商务色系
WHITE = (255, 255, 255, 255)
SILVER_LIGHT = (245, 245, 248, 255)
SILVER_MID = (225, 228, 232, 255)
SILVER_EDGE = (200, 204, 210, 255)

BLUE_NUM = (45, 75, 145, 255)          # 数字蓝（阿拉伯数字）
BLUE_DOT = (60, 95, 165, 255)          # 圆点蓝（分钟刻度）
BLUE_TICK = (50, 80, 150, 255)         # 刻度蓝（整点刻度线）
BLUE_BORDER = (70, 105, 170, 255)      # 边框蓝（面板边框）
BLUE_TEXT = (55, 85, 155, 255)         # 文字蓝（面板内文字）
BLUE_HAND = (25, 35, 60, 255)         # 指针深蓝/近黑
BLUE_HAND_LIGHT = (50, 70, 120, 255)  # 指针蓝色高光

DARK_TEXT = (30, 30, 40, 255)          # 深色文字（数字时间等）
GRAY_TEXT = (110, 115, 125, 255)       # 灰色文字（辅助信息）
LIGHT_SEP = (170, 175, 185, 255)      # 浅灰分隔线

RED_HEART = (200, 50, 60, 255)        # 心率红
TRANSPARENT = (0, 0, 0, 0)

# 输出路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, "watchface", "watchface", "res")
PREVIEW_DIR = os.path.join(BASE_DIR, "watchface", "preview")
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def ensure_dirs():
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


def pt(cx, cy, r, angle_deg):
    """圆上坐标（0度=12点方向，顺时针）"""
    a = math.radians(angle_deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def load_font(paths, size, fallback_size=None):
    for fp in paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    try:
        return ImageFont.truetype("DejaVuSans", size)
    except Exception:
        return ImageFont.load_default()


SANS_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]
SANS_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
CN_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


# ================================================================
# 背景：白银渐变圆盘
# ================================================================
def generate_background():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # 从中心到边缘的径向渐变：白色 → 浅银色
    for r in range(RADIUS, 0, -1):
        t = r / RADIUS  # 1.0=边缘, 0.0=中心
        # 边缘稍暗，中心纯白
        gray = int(255 - t * t * 35)  # 255 → ~220
        color = (gray, gray, min(gray + 3, 255), 255)
        draw.ellipse(
            [CENTER - r, CENTER - r, CENTER + r, CENTER + r],
            fill=color
        )

    img.save(os.path.join(RES_DIR, "background", "bg_main.png"))
    print("  [OK] bg_main.png")
    return img


# ================================================================
# 刻度环：蓝色小圆点（分钟） + 蓝色短线（整点）
# ================================================================
def generate_tick_ring():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    dot_radius = RADIUS - 22  # 圆点环半径

    for i in range(60):
        angle = i * 6
        x, y = pt(CENTER, CENTER, dot_radius, angle)

        if i % 5 == 0:
            # 整点位置：稍大的蓝色圆点
            r = 3
            draw.ellipse([x - r, y - r, x + r, y + r], fill=BLUE_DOT)

            # 加一条向内的短刻度线
            x1, y1 = pt(CENTER, CENTER, dot_radius - 8, angle)
            x2, y2 = pt(CENTER, CENTER, dot_radius - 18, angle)
            draw.line([(x1, y1), (x2, y2)], fill=BLUE_TICK, width=2)
        else:
            # 分钟位置：小蓝色圆点
            r = 1.5
            draw.ellipse([x - r, y - r, x + r, y + r], fill=BLUE_DOT)

    img.save(os.path.join(RES_DIR, "background", "tick_ring.png"))
    print("  [OK] tick_ring.png")
    return img


# ================================================================
# 阿拉伯数字 1-12（蓝色，无衬线）
# ================================================================
def generate_numerals():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    font_num = load_font(SANS_BOLD_PATHS, 36)
    text_r = RADIUS - 58  # 数字环半径

    for h in range(1, 13):
        angle = h * 30
        x, y = pt(CENTER, CENTER, text_r, angle)
        text = str(h)
        bbox = draw.textbbox((0, 0), text, font=font_num)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - tw / 2, y - th / 2 - 2), text,
                  fill=BLUE_NUM, font=font_num)

    img.save(os.path.join(RES_DIR, "background", "numerals.png"))
    print("  [OK] numerals.png")
    return img


# ================================================================
# 内圈细装饰环
# ================================================================
def generate_inner_ring():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    r = RADIUS - 80
    draw.ellipse(
        [CENTER - r, CENTER - r, CENTER + r, CENTER + r],
        outline=(200, 205, 215, 80), width=1
    )
    img.save(os.path.join(RES_DIR, "background", "inner_ring.png"))
    print("  [OK] inner_ring.png")
    return img


# ================================================================
# 中心装饰帽（深蓝金属感）
# ================================================================
def generate_center_cap():
    s = 20
    img = Image.new("RGBA", (s, s), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, s - 1, s - 1], fill=BLUE_HAND)
    draw.ellipse([3, 3, s - 4, s - 4], fill=BLUE_HAND_LIGHT)
    draw.ellipse([6, 6, s - 7, s - 7], fill=BLUE_HAND)
    img.save(os.path.join(RES_DIR, "background", "center_cap.png"))
    print("  [OK] center_cap.png")
    return img


# ================================================================
# 指针 —— 经典锥形，深蓝/黑色
# ================================================================
def generate_hour_hand():
    w, h = 28, 130
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    cx = w // 2
    # 主体：宽锥形
    points = [
        (cx, 0),             # 尖端
        (cx + 7, h - 30),    # 右宽
        (cx + 5, h - 10),    # 右尾
        (cx - 5, h - 10),    # 左尾
        (cx - 7, h - 30),    # 左宽
    ]
    draw.polygon(points, fill=BLUE_HAND)
    # 中心高光线
    draw.line([(cx, 8), (cx, h - 35)], fill=BLUE_HAND_LIGHT, width=1)
    img.save(os.path.join(RES_DIR, "hands", "hour_hand.png"))
    print("  [OK] hour_hand.png")


def generate_minute_hand():
    w, h = 20, 170
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    cx = w // 2
    points = [
        (cx, 0),
        (cx + 5, h - 35),
        (cx + 3, h - 10),
        (cx - 3, h - 10),
        (cx - 5, h - 35),
    ]
    draw.polygon(points, fill=BLUE_HAND)
    draw.line([(cx, 6), (cx, h - 40)], fill=BLUE_HAND_LIGHT, width=1)
    img.save(os.path.join(RES_DIR, "hands", "minute_hand.png"))
    print("  [OK] minute_hand.png")


def generate_second_hand():
    w, h = 8, 195
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    cx = w // 2
    # 极细蓝色秒针
    draw.line([(cx, 0), (cx, h - 35)], fill=BLUE_HAND_LIGHT, width=1)
    # 尾部配重
    draw.line([(cx, h - 35), (cx, h - 8)], fill=BLUE_HAND_LIGHT, width=2)
    draw.ellipse([cx - 3, h - 12, cx + 3, h - 6], fill=BLUE_HAND_LIGHT)
    img.save(os.path.join(RES_DIR, "hands", "second_hand.png"))
    print("  [OK] second_hand.png")


# ================================================================
# 图标
# ================================================================
def generate_icon_heart():
    s = 16
    img = Image.new("RGBA", (s, s), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw.ellipse([1, 2, 7, 8], fill=RED_HEART)
    draw.ellipse([7, 2, 13, 8], fill=RED_HEART)
    draw.polygon([(2, 7), (7, 13), (12, 7)], fill=RED_HEART)
    img.save(os.path.join(RES_DIR, "icons", "ic_heart.png"))
    print("  [OK] ic_heart.png")


def generate_separator():
    img = Image.new("RGBA", (2, 20), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw.line([(1, 2), (1, 18)], fill=LIGHT_SEP, width=1)
    img.save(os.path.join(RES_DIR, "icons", "separator.png"))
    print("  [OK] separator.png")


# ================================================================
# 天气图标（简洁蓝灰风格）
# ================================================================
def generate_weather_icons():
    size = 32
    cloud_c = (160, 165, 175, 255)
    sun_c = (240, 190, 50, 255)
    rain_c = (80, 130, 200, 255)
    snow_c = (190, 200, 220, 255)
    fog_c = (170, 175, 185, 255)

    icons = {
        "0": "sunny", "1": "cloudy", "2": "overcast", "3": "rain",
        "4": "snow", "5": "fog", "6": "wind", "7": "haze",
    }

    for code, name in icons.items():
        img = Image.new("RGBA", (size, size), TRANSPARENT)
        d = ImageDraw.Draw(img)

        if name == "sunny":
            d.ellipse([8, 8, 24, 24], fill=sun_c)
            for a in range(0, 360, 45):
                x1, y1 = pt(16, 16, 10, a)
                x2, y2 = pt(16, 16, 14, a)
                d.line([(x1, y1), (x2, y2)], fill=sun_c, width=2)
        elif name == "cloudy":
            d.ellipse([4, 4, 16, 16], fill=sun_c)
            d.ellipse([10, 12, 22, 22], fill=cloud_c)
            d.ellipse([15, 9, 28, 22], fill=cloud_c)
            d.rectangle([12, 17, 27, 24], fill=cloud_c)
        elif name == "overcast":
            d.ellipse([3, 8, 17, 20], fill=cloud_c)
            d.ellipse([12, 5, 28, 19], fill=cloud_c)
            d.rectangle([8, 14, 26, 22], fill=cloud_c)
        elif name == "rain":
            d.ellipse([5, 3, 16, 13], fill=cloud_c)
            d.ellipse([12, 1, 26, 13], fill=cloud_c)
            d.rectangle([8, 8, 24, 15], fill=cloud_c)
            for rx in [10, 16, 22]:
                d.line([(rx, 18), (rx - 2, 27)], fill=rain_c, width=2)
        elif name == "snow":
            d.ellipse([5, 3, 16, 13], fill=cloud_c)
            d.ellipse([12, 1, 26, 13], fill=cloud_c)
            d.rectangle([8, 8, 24, 15], fill=cloud_c)
            for sx in [10, 17, 24]:
                d.ellipse([sx - 2, 20, sx + 2, 24], fill=snow_c)
        elif name == "fog":
            for fy in [8, 15, 22]:
                d.line([(5, fy), (27, fy)], fill=fog_c, width=2)
        elif name == "wind":
            for wy, wl in [(10, 22), (17, 18), (24, 20)]:
                d.line([(5, wy), (5 + wl, wy)], fill=fog_c, width=2)
        elif name == "haze":
            for hy in [7, 14, 21]:
                d.line([(4, hy), (28, hy)], fill=(180, 170, 150, 160), width=3)

        img.save(os.path.join(RES_DIR, "weather", f"{code}.png"))
    print("  [OK] weather icons (8)")


def generate_week_icons():
    font = load_font(CN_PATHS, 14)
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    for i, day in enumerate(weekdays):
        img = Image.new("RGBA", (50, 20), TRANSPARENT)
        d = ImageDraw.Draw(img)
        text = f"周{day}"
        bbox = d.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((50 - tw) / 2, (20 - th) / 2), text, fill=BLUE_TEXT, font=font)
        img.save(os.path.join(RES_DIR, "icons", "week", f"{i + 1}.png"))
    print("  [OK] week icons (7)")


# ================================================================
# 完整预览图合成
# ================================================================
def generate_preview():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)

    # 叠加背景层
    for lp in ["background/bg_main.png", "background/tick_ring.png",
               "background/numerals.png", "background/inner_ring.png"]:
        fp = os.path.join(RES_DIR, lp)
        if os.path.exists(fp):
            layer = Image.open(fp).convert("RGBA")
            img = Image.alpha_composite(img, layer)

    draw = ImageDraw.Draw(img)

    # 字体
    fn_small = load_font(SANS_PATHS, 14)
    fn_medium = load_font(SANS_PATHS, 16)
    fn_bold = load_font(SANS_BOLD_PATHS, 15)
    fn_time = load_font(SANS_BOLD_PATHS, 32)
    fn_cn = load_font(CN_PATHS, 15)
    fn_cn_s = load_font(CN_PATHS, 13)
    fn_data = load_font(SANS_PATHS, 13)

    # ---- 天气区域（上方居中，12点下方）----
    # 布局：[天气图标] [竖线] [温度 + 温度范围]
    #                [天气描述文字]
    weather_y = 128
    # 天气描述文字（居中）
    _draw_centered(draw, "晴雾", fn_cn_s, GRAY_TEXT, CENTER - 30, weather_y)
    # 竖线分隔
    draw.line([(CENTER - 8, weather_y + 2), (CENTER - 8, weather_y + 30)],
              fill=LIGHT_SEP, width=1)
    # 温度
    _draw_text(draw, "24°C", fn_bold, DARK_TEXT, CENTER + 2, weather_y)
    # 温度范围
    _draw_text(draw, "-10/36", fn_small, GRAY_TEXT, CENTER + 2, weather_y + 17)

    # ---- 左面板（9点方向）：农历 / 时辰 ----
    lp_x, lp_y = 82, 210
    lp_w, lp_h = 108, 44
    draw.rounded_rectangle(
        [lp_x, lp_y, lp_x + lp_w, lp_y + lp_h],
        radius=4, outline=BLUE_BORDER, width=1
    )
    # 上行：农历
    _draw_centered(draw, "十月十八", fn_cn, BLUE_TEXT,
                   lp_x + lp_w // 2, lp_y + 4)
    # 分隔线
    draw.line([(lp_x + 10, lp_y + lp_h // 2),
               (lp_x + lp_w - 10, lp_y + lp_h // 2)],
              fill=(180, 190, 210, 100), width=1)
    # 下行：时辰
    _draw_centered(draw, "巳时", fn_cn_s, GRAY_TEXT,
                   lp_x + lp_w // 2, lp_y + 24)

    # ---- 右面板（3点方向）：星期 / 日期 ----
    rp_x, rp_y = 264, 210
    rp_w, rp_h = 108, 44
    draw.rounded_rectangle(
        [rp_x, rp_y, rp_x + rp_w, rp_y + rp_h],
        radius=4, outline=BLUE_BORDER, width=1
    )
    _draw_centered(draw, "星期五", fn_cn, BLUE_TEXT,
                   rp_x + rp_w // 2, rp_y + 4)
    draw.line([(rp_x + 10, rp_y + rp_h // 2),
               (rp_x + rp_w - 10, rp_y + rp_h // 2)],
              fill=(180, 190, 210, 100), width=1)
    _draw_centered(draw, "10-18", fn_medium, GRAY_TEXT,
                   rp_x + rp_w // 2, rp_y + 24)

    # ---- 数字时间（中下方）----
    time_text = "10:27"
    bbox = draw.textbbox((0, 0), time_text, font=fn_time)
    tw = bbox[2] - bbox[0]
    draw.text(((SIZE - tw) / 2, 278), time_text, fill=DARK_TEXT, font=fn_time)

    # ---- 数据行：步数 + 距离 ----
    data_y = 320
    data_text = "7651 步数"
    bbox1 = draw.textbbox((0, 0), data_text, font=fn_cn_s)
    tw1 = bbox1[2] - bbox1[0]

    sep_text = " | "
    bbox_sep = draw.textbbox((0, 0), sep_text, font=fn_data)
    tw_sep = bbox_sep[2] - bbox_sep[0]

    dist_text = "距离 3.66 km"
    bbox2 = draw.textbbox((0, 0), dist_text, font=fn_cn_s)
    tw2 = bbox2[2] - bbox2[0]

    total_w = tw1 + tw_sep + tw2
    start_x = (SIZE - total_w) / 2
    draw.text((start_x, data_y), data_text, fill=DARK_TEXT, font=fn_cn_s)
    draw.text((start_x + tw1, data_y), sep_text, fill=LIGHT_SEP, font=fn_data)
    draw.text((start_x + tw1 + tw_sep, data_y), dist_text,
              fill=DARK_TEXT, font=fn_cn_s)

    # ---- 心率 ----
    hr_y = 345
    # 心形小图标
    heart_icon = os.path.join(RES_DIR, "icons", "ic_heart.png")
    if os.path.exists(heart_icon):
        hi = Image.open(heart_icon).convert("RGBA")
        img.paste(hi, (CENTER - 20, hr_y), hi)
    hr_text = "103"
    draw = ImageDraw.Draw(img)  # refresh after paste
    draw.text((CENTER - 2, hr_y), hr_text, fill=RED_HEART, font=fn_bold)

    # ---- 绘制指针 ----
    # 时针 10:27 → (10 + 27/60)*30 = 313.5°
    hour_angle = (10 + 27 / 60) * 30
    _draw_tapered_hand(img, CENTER, CENTER, hour_angle,
                       length=95, tail=18, base_w=7, tip_w=1.5,
                       color=BLUE_HAND, highlight=BLUE_HAND_LIGHT)

    # 分针 27分 → 27*6 = 162°
    min_angle = 27 * 6
    _draw_tapered_hand(img, CENTER, CENTER, min_angle,
                       length=135, tail=22, base_w=5, tip_w=1,
                       color=BLUE_HAND, highlight=BLUE_HAND_LIGHT)

    # 秒针 45秒 → 270°
    sec_angle = 45 * 6
    _draw_thin_hand(img, CENTER, CENTER, sec_angle,
                    length=150, tail=30, color=BLUE_HAND_LIGHT)

    # 中心帽
    cap_path = os.path.join(RES_DIR, "background", "center_cap.png")
    if os.path.exists(cap_path):
        cap = Image.open(cap_path).convert("RGBA")
        img.paste(cap, (CENTER - 10, CENTER - 10), cap)

    # 保存
    preview_rgb = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    preview_rgb.paste(img, mask=img.split()[3])
    preview_rgb.save(os.path.join(PREVIEW_DIR, "cover.jpg"), "JPEG", quality=95)

    thumb = preview_rgb.resize((120, 120), Image.Resampling.LANCZOS)
    thumb.save(os.path.join(PREVIEW_DIR, "icon_small.jpg"), "JPEG", quality=90)

    img.save(os.path.join(DOCS_DIR, "preview_full.png"))
    print("  [OK] preview images")
    return img


def _draw_text(draw, text, font, color, x, y):
    draw.text((x, y), text, fill=color, font=font)


def _draw_centered(draw, text, font, color, cx, y):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, y), text, fill=color, font=font)


def _draw_tapered_hand(img, cx, cy, angle_deg, length, tail, base_w, tip_w,
                       color, highlight):
    """绘制锥形指针（宽底窄尖）"""
    draw = ImageDraw.Draw(img)
    a = math.radians(angle_deg - 90)
    perp = a + math.pi / 2

    # 尖端
    tip_x = cx + length * math.cos(a)
    tip_y = cy + length * math.sin(a)

    # 底部两侧（最宽处，在中心附近）
    bl_x = cx - base_w * math.cos(perp) + 5 * math.cos(a)
    bl_y = cy - base_w * math.sin(perp) + 5 * math.sin(a)
    br_x = cx + base_w * math.cos(perp) + 5 * math.cos(a)
    br_y = cy + base_w * math.sin(perp) + 5 * math.sin(a)

    # 尖端两侧
    tl_x = tip_x - tip_w * math.cos(perp)
    tl_y = tip_y - tip_w * math.sin(perp)
    tr_x = tip_x + tip_w * math.cos(perp)
    tr_y = tip_y + tip_w * math.sin(perp)

    # 尾部
    tail_x = cx - tail * math.cos(a)
    tail_y = cy - tail * math.sin(a)
    tail_l_x = tail_x - 3 * math.cos(perp)
    tail_l_y = tail_y - 3 * math.sin(perp)
    tail_r_x = tail_x + 3 * math.cos(perp)
    tail_r_y = tail_y + 3 * math.sin(perp)

    # 绘制完整指针形状
    points = [
        (tl_x, tl_y), (bl_x, bl_y),
        (tail_l_x, tail_l_y), (tail_r_x, tail_r_y),
        (br_x, br_y), (tr_x, tr_y)
    ]
    draw.polygon(points, fill=color)

    # 中线高光
    mid_x = cx + (length * 0.15) * math.cos(a)
    mid_y = cy + (length * 0.15) * math.sin(a)
    end_x = cx + (length * 0.85) * math.cos(a)
    end_y = cy + (length * 0.85) * math.sin(a)
    draw.line([(mid_x, mid_y), (end_x, end_y)], fill=highlight, width=1)


def _draw_thin_hand(img, cx, cy, angle_deg, length, tail, color):
    """绘制细秒针"""
    draw = ImageDraw.Draw(img)
    a = math.radians(angle_deg - 90)
    tip_x = cx + length * math.cos(a)
    tip_y = cy + length * math.sin(a)
    tail_x = cx - tail * math.cos(a)
    tail_y = cy - tail * math.sin(a)
    draw.line([(tail_x, tail_y), (tip_x, tip_y)], fill=color, width=1)


# ================================================================
# 主程序
# ================================================================
def main():
    print("=" * 60)
    print("  翰墨精英 - 蓝白商务表盘资源生成器")
    print("  目标: 454x454 (HWHD02)")
    print("=" * 60)

    ensure_dirs()

    print("\n[1/4] 背景图层...")
    generate_background()
    generate_tick_ring()
    generate_numerals()
    generate_inner_ring()
    generate_center_cap()

    print("\n[2/4] 指针...")
    generate_hour_hand()
    generate_minute_hand()
    generate_second_hand()

    print("\n[3/4] 图标...")
    generate_icon_heart()
    generate_separator()
    generate_weather_icons()
    generate_week_icons()

    print("\n[4/4] 预览图...")
    generate_preview()

    print("\n" + "=" * 60)
    print("  完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
