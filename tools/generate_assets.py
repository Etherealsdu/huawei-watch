#!/usr/bin/env python3
"""
翰墨精英 (Elite Business) - 华为表盘图片资源生成器
精确复刻蓝白商务表盘，指针前部改为红色
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

SIZE = 454
CX, CY = SIZE // 2, SIZE // 2
R = SIZE // 2

# 颜色
BLUE = (50, 85, 155, 255)
BLUE_LIGHT = (75, 115, 180, 255)
BLUE_DARK = (35, 60, 120, 255)
DARK = (25, 30, 45, 255)
DARK_TEXT = (30, 35, 50, 255)
GRAY = (120, 125, 135, 255)
LIGHT_GRAY = (180, 185, 195, 255)
RED = (200, 40, 50, 255)
RED_HEART = (210, 50, 55, 255)
TRANS = (0, 0, 0, 0)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "watchface", "watchface", "res")
PREV = os.path.join(BASE, "watchface", "preview")
DOCS = os.path.join(BASE, "docs")

SANS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
SANS_B = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
CN = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
      "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
      "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"]


def font(paths, sz):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def polar(cx, cy, r, deg):
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def dirs():
    for d in [RES + "/background", RES + "/hands", RES + "/icons",
              RES + "/icons/week", RES + "/weather", PREV, DOCS]:
        os.makedirs(d, exist_ok=True)


# ========== 背景：白→银渐变 ==========
def bg():
    img = Image.new("RGBA", (SIZE, SIZE), TRANS)
    d = ImageDraw.Draw(img)
    for r in range(R, 0, -1):
        t = (r / R) ** 2
        v = int(255 - t * 30)
        d.ellipse([CX - r, CY - r, CX + r, CY + r], fill=(v, v, v + 2, 255))
    img.save(f"{RES}/background/bg_main.png")
    print("  bg_main.png")
    return img


# ========== 刻度：小蓝方点 + 整点刻度线 ==========
def ticks():
    img = Image.new("RGBA", (SIZE, SIZE), TRANS)
    d = ImageDraw.Draw(img)
    dot_r = R - 20

    for i in range(60):
        ang = i * 6
        x, y = polar(CX, CY, dot_r, ang)
        if i % 5 == 0:
            # 整点：大方点
            s = 3
            d.rectangle([x - s, y - s, x + s, y + s], fill=BLUE)
            # 内侧短线
            x1, y1 = polar(CX, CY, dot_r - 7, ang)
            x2, y2 = polar(CX, CY, dot_r - 16, ang)
            d.line([(x1, y1), (x2, y2)], fill=BLUE, width=2)
        else:
            # 分钟：小方点
            s = 1.5
            d.rectangle([x - s, y - s, x + s, y + s], fill=BLUE_LIGHT)

    img.save(f"{RES}/background/tick_ring.png")
    print("  tick_ring.png")
    return img


# ========== 蓝色阿拉伯数字 ==========
def nums():
    img = Image.new("RGBA", (SIZE, SIZE), TRANS)
    d = ImageDraw.Draw(img)
    f = font(SANS_B, 34)
    nr = R - 55

    for h in range(1, 13):
        ang = h * 30
        x, y = polar(CX, CY, nr, ang)
        t = str(h)
        bb = d.textbbox((0, 0), t, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((x - tw / 2, y - th / 2 - 1), t, fill=BLUE, font=f)

    img.save(f"{RES}/background/numerals.png")
    print("  numerals.png")
    return img


# ========== 中心帽 ==========
def cap():
    s = 18
    img = Image.new("RGBA", (s, s), TRANS)
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, s - 1, s - 1], fill=(20, 30, 55, 255))
    d.ellipse([2, 2, s - 3, s - 3], fill=(55, 75, 125, 255))
    d.ellipse([5, 5, s - 6, s - 6], fill=(25, 35, 60, 255))
    img.save(f"{RES}/background/center_cap.png")
    print("  center_cap.png")
    return img


# ========== 指针 - 两截式：后半深色 + 前半红色 ==========
def hand_hour():
    """时针: 总长 120px, pivot在90处 (前部90px, 尾部30px)"""
    w, h = 18, 120
    img = Image.new("RGBA", (w, h), TRANS)
    d = ImageDraw.Draw(img)
    cx = w // 2

    # 后半（下部/尾部）- 深色，较宽
    # 从pivot(y=90)到底部(y=h)
    d.polygon([
        (cx - 4, h),         # 左下
        (cx - 5, 90),        # 左侧pivot处
        (cx + 5, 90),        # 右侧pivot处
        (cx + 4, h),         # 右下
    ], fill=DARK)

    # 前半（上部/尖端）- 红色，锥形
    # 从pivot(y=90)到尖端(y=0)
    d.polygon([
        (cx, 0),             # 尖端
        (cx - 5, 50),        # 左侧中段
        (cx - 6, 90),        # 左侧最宽处
        (cx + 6, 90),        # 右侧最宽处
        (cx + 5, 50),        # 右侧中段
    ], fill=RED)

    # 深色中线（给前部增加细节）
    d.line([(cx, 10), (cx, 85)], fill=(150, 25, 35, 180), width=1)

    img.save(f"{RES}/hands/hour_hand.png")
    print("  hour_hand.png")


def hand_min():
    """分针: 总长 155px, pivot在120处 (前部120px, 尾部35px)"""
    w, h = 14, 155
    img = Image.new("RGBA", (w, h), TRANS)
    d = ImageDraw.Draw(img)
    cx = w // 2

    # 后半 - 深色
    d.polygon([
        (cx - 3, h),
        (cx - 4, 120),
        (cx + 4, 120),
        (cx + 3, h),
    ], fill=DARK)

    # 前半 - 红色锥形
    d.polygon([
        (cx, 0),
        (cx - 3, 40),
        (cx - 4, 120),
        (cx + 4, 120),
        (cx + 3, 40),
    ], fill=RED)

    d.line([(cx, 8), (cx, 115)], fill=(150, 25, 35, 180), width=1)

    img.save(f"{RES}/hands/minute_hand.png")
    print("  minute_hand.png")


def hand_sec():
    """秒针: 极细蓝色"""
    w, h = 6, 190
    img = Image.new("RGBA", (w, h), TRANS)
    d = ImageDraw.Draw(img)
    cx = w // 2
    d.line([(cx, 0), (cx, 160)], fill=BLUE_LIGHT, width=1)
    d.line([(cx, 160), (cx, h - 5)], fill=BLUE_LIGHT, width=2)
    d.ellipse([cx - 3, h - 8, cx + 3, h - 2], fill=BLUE_LIGHT)
    img.save(f"{RES}/hands/second_hand.png")
    print("  second_hand.png")


# ========== 心率图标 ==========
def icon_heart():
    s = 14
    img = Image.new("RGBA", (s, s), TRANS)
    d = ImageDraw.Draw(img)
    d.ellipse([1, 2, 6, 7], fill=RED_HEART)
    d.ellipse([6, 2, 11, 7], fill=RED_HEART)
    d.polygon([(1, 6), (6, 12), (11, 6)], fill=RED_HEART)
    img.save(f"{RES}/icons/ic_heart.png")
    print("  ic_heart.png")


# ========== 天气图标 ==========
def weather():
    sz = 28
    cld = (155, 160, 170, 255)
    sun = (235, 185, 45, 255)
    rain = (75, 125, 195, 255)

    types = ["sunny", "cloudy", "overcast", "rain", "snow", "fog", "wind", "haze"]
    for i, name in enumerate(types):
        img = Image.new("RGBA", (sz, sz), TRANS)
        d = ImageDraw.Draw(img)
        if name == "sunny":
            d.ellipse([7, 7, 21, 21], fill=sun)
            for a in range(0, 360, 45):
                p1 = polar(14, 14, 9, a)
                p2 = polar(14, 14, 12, a)
                d.line([p1, p2], fill=sun, width=2)
        elif name == "cloudy":
            d.ellipse([3, 3, 14, 14], fill=sun)
            d.ellipse([9, 11, 19, 20], fill=cld)
            d.ellipse([14, 8, 25, 19], fill=cld)
            d.rectangle([10, 15, 24, 21], fill=cld)
        elif name == "overcast":
            d.ellipse([3, 7, 15, 18], fill=cld)
            d.ellipse([10, 4, 24, 17], fill=cld)
            d.rectangle([7, 12, 23, 20], fill=cld)
        elif name == "rain":
            d.ellipse([4, 2, 14, 11], fill=cld)
            d.ellipse([10, 1, 22, 11], fill=cld)
            d.rectangle([7, 7, 21, 13], fill=cld)
            for rx in [9, 14, 19]:
                d.line([(rx, 16), (rx - 1, 23)], fill=rain, width=2)
        elif name == "snow":
            d.ellipse([4, 2, 14, 11], fill=cld)
            d.ellipse([10, 1, 22, 11], fill=cld)
            d.rectangle([7, 7, 21, 13], fill=cld)
            for sx in [9, 15, 21]:
                d.ellipse([sx - 2, 17, sx + 2, 21], fill=(210, 220, 235, 255))
        elif name == "fog":
            for fy in [7, 13, 19]:
                d.line([(4, fy), (24, fy)], fill=cld, width=2)
        elif name == "wind":
            for wy, wl in [(8, 18), (14, 14), (20, 16)]:
                d.line([(4, wy), (4 + wl, wy)], fill=cld, width=2)
        elif name == "haze":
            for hy in [6, 12, 18]:
                d.line([(3, hy), (25, hy)], fill=(170, 160, 140, 150), width=3)
        img.save(f"{RES}/weather/{i}.png")
    print("  weather x8")


def week_icons():
    f = font(CN, 13)
    days = ["一", "二", "三", "四", "五", "六", "日"]
    for i, day in enumerate(days):
        img = Image.new("RGBA", (44, 18), TRANS)
        d = ImageDraw.Draw(img)
        t = f"周{day}"
        bb = d.textbbox((0, 0), t, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((44 - tw) / 2, (18 - th) / 2), t, fill=BLUE, font=f)
        img.save(f"{RES}/icons/week/{i + 1}.png")
    print("  week x7")


# ========== 预览图：精确复刻布局 ==========
def preview():
    img = Image.new("RGBA", (SIZE, SIZE), TRANS)

    # 叠加背景层
    for lp in ["background/bg_main.png", "background/tick_ring.png",
               "background/numerals.png"]:
        fp = f"{RES}/{lp}"
        if os.path.exists(fp):
            img = Image.alpha_composite(img, Image.open(fp).convert("RGBA"))

    d = ImageDraw.Draw(img)

    # 字体
    fs = font(SANS, 13)
    fb = font(SANS_B, 14)
    ft = font(SANS_B, 30)   # 数字时间
    fc = font(CN, 14)
    fcs = font(CN, 12)

    # ==== 天气区域（12点下方）====
    # 左侧：晴雾
    _ctxt(d, "晴雾", fcs, GRAY, CX - 25, 130)
    # 竖线
    d.line([(CX - 2, 130), (CX - 2, 158)], fill=LIGHT_GRAY, width=1)
    # 右侧：温度
    d.text((CX + 8, 128), "24°C", fill=DARK_TEXT, font=fb)
    d.text((CX + 8, 144), "-10/36", fill=GRAY, font=fs)

    # ==== 左面板：农历/时辰 ====
    lx, ly, lw, lh = 78, 207, 106, 42
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=3,
                        outline=BLUE_LIGHT, width=1)
    _ctxt(d, "十月十八", fc, BLUE, lx + lw // 2, ly + 4)
    d.line([(lx + 8, ly + lh // 2), (lx + lw - 8, ly + lh // 2)],
           fill=(185, 195, 210, 80), width=1)
    _ctxt(d, "巳时", fcs, GRAY, lx + lw // 2, ly + 23)

    # ==== 右面板：星期/日期 ====
    rx, ry, rw, rh = 270, 207, 106, 42
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=3,
                        outline=BLUE_LIGHT, width=1)
    _ctxt(d, "星期五", fc, BLUE, rx + rw // 2, ry + 4)
    d.line([(rx + 8, ry + rh // 2), (rx + rw - 8, ry + rh // 2)],
           fill=(185, 195, 210, 80), width=1)
    _ctxt(d, "10-18", font(SANS, 14), GRAY, rx + rw // 2, ry + 23)

    # ==== 数字时间 ====
    tt = "10:27"
    bb = d.textbbox((0, 0), tt, font=ft)
    tw = bb[2] - bb[0]
    d.text(((SIZE - tw) / 2, 272), tt, fill=DARK_TEXT, font=ft)

    # ==== 数据行 ====
    data_line = "7651 步数 | 距离 3.66 km"
    fd = font(CN, 12)
    bb = d.textbbox((0, 0), data_line, font=fd)
    tw = bb[2] - bb[0]
    # 手动分段绘制以使 | 为灰色
    left_t = "7651 步数"
    sep_t = " | "
    right_t = "距离 3.66 km"
    bbl = d.textbbox((0, 0), left_t, font=fd)
    bbs = d.textbbox((0, 0), sep_t, font=fs)
    bbr = d.textbbox((0, 0), right_t, font=fd)
    twl, tws, twr = bbl[2] - bbl[0], bbs[2] - bbs[0], bbr[2] - bbr[0]
    total = twl + tws + twr
    sx = (SIZE - total) / 2
    dy = 312
    d.text((sx, dy), left_t, fill=DARK_TEXT, font=fd)
    d.text((sx + twl, dy), sep_t, fill=LIGHT_GRAY, font=fs)
    d.text((sx + twl + tws, dy), right_t, fill=DARK_TEXT, font=fd)

    # ==== 心率 ====
    hy = 335
    # 小红星/心图标
    hicon = f"{RES}/icons/ic_heart.png"
    if os.path.exists(hicon):
        hi = Image.open(hicon).convert("RGBA")
        img.paste(hi, (CX - 18, hy), hi)
    d = ImageDraw.Draw(img)
    d.text((CX - 2, hy), "103", fill=RED_HEART, font=fb)

    # ==== 绘制指针 ====
    # 时针 10:27 → (10+27/60)*30 = 313.5°
    h_ang = (10 + 27 / 60) * 30
    _hand2(img, CX, CY, h_ang, front=90, tail=25, fw_base=6, fw_tip=1,
           tw=4, front_color=RED, tail_color=DARK)

    # 分针 27*6 = 162°
    m_ang = 27 * 6
    _hand2(img, CX, CY, m_ang, front=120, tail=30, fw_base=4, fw_tip=0.5,
           tw=3, front_color=RED, tail_color=DARK)

    # 秒针不显示（参考图未见明显秒针）

    # 中心帽
    cp = f"{RES}/background/center_cap.png"
    if os.path.exists(cp):
        c = Image.open(cp).convert("RGBA")
        img.paste(c, (CX - 9, CY - 9), c)

    # 保存
    rgb = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    rgb.paste(img, mask=img.split()[3])
    rgb.save(f"{PREV}/cover.jpg", "JPEG", quality=95)
    rgb.resize((120, 120), Image.Resampling.LANCZOS).save(
        f"{PREV}/icon_small.jpg", "JPEG", quality=90)
    img.save(f"{DOCS}/preview_full.png")
    print("  preview images")


def _ctxt(d, text, f, color, cx, y):
    bb = d.textbbox((0, 0), text, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2, y), text, fill=color, font=f)


def _hand2(img, cx, cy, angle, front, tail, fw_base, fw_tip, tw,
           front_color, tail_color):
    """绘制两截式指针：前部front_color + 尾部tail_color"""
    d = ImageDraw.Draw(img)
    a = math.radians(angle - 90)
    perp = a + math.pi / 2

    # 尖端
    tip_x = cx + front * math.cos(a)
    tip_y = cy + front * math.sin(a)

    # 前部底端（pivot处）两侧
    fb_lx = cx - fw_base * math.cos(perp)
    fb_ly = cy - fw_base * math.sin(perp)
    fb_rx = cx + fw_base * math.cos(perp)
    fb_ry = cy + fw_base * math.sin(perp)

    # 前部尖端两侧
    ft_lx = tip_x - fw_tip * math.cos(perp)
    ft_ly = tip_y - fw_tip * math.sin(perp)
    ft_rx = tip_x + fw_tip * math.cos(perp)
    ft_ry = tip_y + fw_tip * math.sin(perp)

    # 绘制前部（红色锥形）
    d.polygon([(ft_lx, ft_ly), (fb_lx, fb_ly),
               (fb_rx, fb_ry), (ft_rx, ft_ry)], fill=front_color)

    # 尾端
    tail_x = cx - tail * math.cos(a)
    tail_y = cy - tail * math.sin(a)
    tl_lx = tail_x - tw * math.cos(perp)
    tl_ly = tail_y - tw * math.sin(perp)
    tl_rx = tail_x + tw * math.cos(perp)
    tl_ry = tail_y + tw * math.sin(perp)

    # 绘制尾部（深色矩形）
    d.polygon([(fb_lx, fb_ly), (tl_lx, tl_ly),
               (tl_rx, tl_ry), (fb_rx, fb_ry)], fill=tail_color)

    # 前部中心暗线
    m1x = cx + (front * 0.1) * math.cos(a)
    m1y = cy + (front * 0.1) * math.sin(a)
    m2x = cx + (front * 0.9) * math.cos(a)
    m2y = cy + (front * 0.9) * math.sin(a)
    darker = (max(0, front_color[0] - 50), max(0, front_color[1] - 15),
              max(0, front_color[2] - 15), 120)
    d.line([(m1x, m1y), (m2x, m2y)], fill=darker, width=1)


def main():
    print("=" * 50)
    print("  翰墨精英 - 蓝白商务表盘 (红色指针前部)")
    print("=" * 50)
    dirs()
    print("\n背景...")
    bg(); ticks(); nums(); cap()
    print("\n指针...")
    hand_hour(); hand_min(); hand_sec()
    print("\n图标...")
    icon_heart(); weather(); week_icons()
    print("\n预览...")
    preview()
    print("\n完成!")


if __name__ == "__main__":
    main()
