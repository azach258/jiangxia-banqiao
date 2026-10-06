# -*- coding: utf-8 -*-
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

base_dir = r'C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館'
out_dir = os.path.join(base_dir, 'fb_charity_posters')
artifact_dir = r'C:/Users/love_/.gemini/antigravity/brain/cc0683a0-544d-4081-a6ca-781abf203c0f'
os.makedirs(out_dir, exist_ok=True)
os.makedirs(artifact_dir, exist_ok=True)

photo_technique = r'C:/Users/love_/AppData/Local/hermes/cache/images/img_d00d4008c009.jpg'
photo_exterior = r'C:/Users/love_/AppData/Local/hermes/cache/images/img_81edf849663c.jpg'

FONT_BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
FONT_REG = 'C:/Windows/Fonts/msjh.ttc'

def get_text_size(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_text_centered(draw, y, text, font, fill, W, shadow=True, shadow_color=(0, 0, 0, 200), offset=(2, 2)):
    tw, th = get_text_size(font, text)
    x = (W - tw) // 2
    if shadow:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)
    return tw, th

# ==============================================================================
# POSTER 1: 4:5 旗艦尊爵版 (1080 x 1350) - 手機滿版極致美感
# ==============================================================================
def create_poster_flagship_4_5():
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#0E0A08')
    draw = ImageDraw.Draw(img)
    
    c_top = (35, 22, 16)
    c_mid = (20, 14, 10)
    c_bot = (10, 8, 7)
    for y in range(H):
        ratio = y / H
        if ratio < 0.5:
            r = int(c_top[0] + (c_mid[0] - c_top[0]) * (ratio * 2))
            g = int(c_top[1] + (c_mid[1] - c_top[1]) * (ratio * 2))
            b = int(c_top[2] + (c_mid[2] - c_top[2]) * (ratio * 2))
        else:
            r = int(c_mid[0] + (c_bot[0] - c_mid[0]) * ((ratio - 0.5) * 2))
            g = int(c_mid[1] + (c_bot[1] - c_mid[1]) * ((ratio - 0.5) * 2))
            b = int(c_mid[2] + (c_bot[2] - c_mid[2]) * ((ratio - 0.5) * 2))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    if os.path.exists(photo_technique):
        bg_photo = Image.open(photo_technique).convert('RGBA')
        pw, ph = bg_photo.size
        crop_h = int(pw * 0.7)
        bg_crop = bg_photo.crop((0, 0, pw, min(ph, crop_h)))
        bg_resized = bg_crop.resize((W, int(W * 0.65)), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', bg_resized.size, 45)
        img_rgba = img.convert('RGBA')
        img_rgba.paste(bg_resized, (0, 0), mask)
        img = img_rgba.convert('RGB')
        draw = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(FONT_BOLD, 26)
    f_hook = ImageFont.truetype(FONT_BOLD, 30)
    f_title = ImageFont.truetype(FONT_BOLD, 52)
    f_name = ImageFont.truetype(FONT_BOLD, 68)
    f_price_tag = ImageFont.truetype(FONT_BOLD, 52)
    f_price_sub = ImageFont.truetype(FONT_BOLD, 26)
    f_badge = ImageFont.truetype(FONT_BOLD, 24)
    f_item_title = ImageFont.truetype(FONT_BOLD, 32)
    f_item_desc = ImageFont.truetype(FONT_REG, 26)
    f_slogan = ImageFont.truetype(FONT_BOLD, 30)
    f_info_label = ImageFont.truetype(FONT_BOLD, 26)
    f_info_val = ImageFont.truetype(FONT_BOLD, 28)
    f_info_sub = ImageFont.truetype(FONT_REG, 24)
    f_cta_btn = ImageFont.truetype(FONT_BOLD, 40)
    f_cta_sub = ImageFont.truetype(FONT_BOLD, 26)

    # 1. Top Brand Tag
    tag_text = '江夏傳統整復推拿 ‧ 板橋館【年度公益企劃】'
    tw, th = get_text_size(f_tag, tag_text)
    draw.rounded_rectangle([(W - tw)//2 - 30, 40, (W + tw)//2 + 30, 40 + th + 18], radius=20, fill='#B45309', outline='#F59E0B', width=2)
    draw.text(((W - tw)//2, 48), tag_text, font=f_tag, fill='#FFFFFF')

    # 2. Main Title Section
    draw_text_centered(draw, 115, '平常預約不到的大師級調理 ‧ 限時親臨現場', f_hook, '#FDE68A', W)
    draw_text_centered(draw, 162, '創始人「黃正斌 總館長」', f_name, '#FFD700', W, shadow=True, offset=(3, 3))
    draw_text_centered(draw, 248, '親自出手 ‧ 板橋館公益義整', f_title, '#FFFFFF', W, shadow=True, offset=(2, 2))

    # 3. Main Center Card
    cx1, cy1, cx2, cy2 = 45, 335, W - 45, 875
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=28, fill='#1B130E', outline='#D97706', width=3)
    
    # Red Price Banner Header
    draw.rounded_rectangle([cx1 + 3, cy1 + 3, cx2 - 3, cy1 + 115], radius=25, fill='#991B1B')
    draw_text_centered(draw, cy1 + 16, '超值銅板公益價 NT$ 500 元', f_price_tag, '#FFFBEB', W, shadow=False)
    draw_text_centered(draw, cy1 + 76, '★ 所得全額捐贈【伊甸基金會】★', f_price_sub, '#FEF08A', W, shadow=False)

    # Benefit 1 Card
    b1_y = cy1 + 140
    draw.rounded_rectangle([cx1 + 25, b1_y, cx2 - 25, b1_y + 130], radius=18, fill='#291A12', outline='#B45309', width=2)
    bw, bh = get_text_size(f_badge, '好禮相贈')
    draw.rounded_rectangle([cx1 + 45, b1_y + 20, cx1 + 45 + bw + 24, b1_y + 20 + bh + 14], radius=10, fill='#D97706')
    draw.text((cx1 + 57, b1_y + 26), '好禮相贈', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 45 + bw + 40, b1_y + 22), '總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#FDE68A')
    draw.text((cx1 + 45, b1_y + 76), '創始人 30 年武學與經絡鬆身心法 ‧ 最實用的日常養生寶典', font=f_item_desc, fill='#CBD5E1')

    # Benefit 2 Card
    b2_y = b1_y + 150
    draw.rounded_rectangle([cx1 + 25, b2_y, cx2 - 25, b2_y + 130], radius=18, fill='#291A12', outline='#B45309', width=2)
    bw2, bh2 = get_text_size(f_badge, '大師親調')
    draw.rounded_rectangle([cx1 + 45, b2_y + 20, cx1 + 45 + bw2 + 24, b2_y + 20 + bh2 + 14], radius=10, fill='#0284C7')
    draw.text((cx1 + 57, b2_y + 26), '大師親調', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 45 + bw2 + 40, b2_y + 22), '專業單部位整復調理 乙次', font=f_item_title, fill='#38BDF8')
    draw.text((cx1 + 45, b2_y + 76), '正統武術內勁鬆拿 ‧ 深層釋放長年緊繃與僵硬 ‧ 活絡通暢', font=f_item_desc, fill='#CBD5E1')

    # Slogan inside card
    draw_text_centered(draw, cy1 + 460, '舒緩全身緊繃 ‧ 同時把愛心溫暖傳遞出去', f_slogan, '#34D399', W, shadow=False)

    # 4. Event Time & Location Box
    bx1, by1, bx2, by2 = 45, 900, W - 45, 1100
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=20, fill='#16171B', outline='#4B5563', width=2)
    
    lbl_w, lbl_h = get_text_size(f_info_label, '活動時間')
    draw.rounded_rectangle([bx1 + 30, by1 + 20, bx1 + 30 + lbl_w + 24, by1 + 20 + lbl_h + 12], radius=8, fill='#374151')
    draw.text((bx1 + 42, by1 + 25), '活動時間', font=f_info_label, fill='#F9FAFB')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 22), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 62), '※ 13:30 開始現場報到拿號碼牌 ‧ 名額有限搶完即止', font=f_info_sub, fill='#F87171')

    draw.rounded_rectangle([bx1 + 30, by1 + 112, bx1 + 30 + lbl_w + 24, by1 + 112 + lbl_h + 12], radius=8, fill='#374151')
    draw.text((bx1 + 42, by1 + 117), '活動地點', font=f_info_label, fill='#F9FAFB')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 114), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 154), '新北市板橋區館前西路 152-1 號（近府中捷運站）', font=f_info_sub, fill='#94A3B8')

    # 5. Bottom CTA
    cta_x1, cta_y1, cta_x2, cta_y2 = 45, 1125, W - 45, 1310
    draw.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=24, fill='#06C755', outline='#22C55E', width=2)
    draw_text_centered(draw, cta_y1 + 26, '立即加 LINE 預約：@429rnxzs', f_cta_btn, '#FFFFFF', W, shadow=True, shadow_color=(0, 60, 20, 160))
    draw_text_centered(draw, cta_y1 + 95, '私訊發送「我要預約公益義整」光速保留名額！', f_cta_sub, '#F0FDF4', W, shadow=False)

    filename = '01_FB貼文海報_4比5旗艦手機版.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print('Generated Flagship 4:5 Poster')

# ==============================================================================
# POSTER 2: 1:1 正方形經典社群圖卡 (1080 x 1080)
# ==============================================================================
def create_poster_square_1_1():
    W, H = 1080, 1080
    img = Image.new('RGB', (W, H), color='#100C0A')
    draw = ImageDraw.Draw(img)

    c_top = (35, 20, 15)
    c_bot = (12, 10, 8)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    f_tag = ImageFont.truetype(FONT_BOLD, 24)
    f_main = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_BOLD, 28)
    f_price_sub = ImageFont.truetype(FONT_BOLD, 25)
    f_badge = ImageFont.truetype(FONT_BOLD, 22)
    f_item_title = ImageFont.truetype(FONT_BOLD, 30)
    f_item_desc = ImageFont.truetype(FONT_REG, 24)
    f_info_label = ImageFont.truetype(FONT_BOLD, 24)
    f_info_val = ImageFont.truetype(FONT_BOLD, 26)
    f_info_sub = ImageFont.truetype(FONT_REG, 22)
    f_cta = ImageFont.truetype(FONT_BOLD, 36)
    f_cta_sub = ImageFont.truetype(FONT_BOLD, 24)

    # 1. Header Tag
    tag = '江夏傳統整復推拿 ‧ 板橋館【限時震撼 ‧ 公益義整】'
    tw, th = get_text_size(f_tag, tag)
    draw.rounded_rectangle([(W - tw)//2 - 25, 24, (W + tw)//2 + 25, 24 + th + 14], radius=16, fill='#B45309')
    draw.text(((W - tw)//2, 31), tag, font=f_tag, fill='#FFFFFF')

    # 2. Main Title
    draw_text_centered(draw, 75, '江夏創始人「黃正斌 總館長」親自出手！', f_main, '#FFD700', W)
    draw_text_centered(draw, 134, '30年正統武術內勁鬆拿 ‧ 平常排不到的大師親調', f_sub, '#FDE68A', W)

    # 3. Main Center Box
    cx1, cy1, cx2, cy2 = 40, 180, W - 40, 620
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=22, fill='#1E1510', outline='#D97706', width=2)
    
    # Red Price Banner
    draw.rounded_rectangle([cx1 + 2, cy1 + 2, cx2 - 2, cy1 + 80], radius=20, fill='#991B1B')
    draw_text_centered(draw, cy1 + 12, '銅板公益價 NT$ 500 元（所得全額捐贈 伊甸基金會）', f_price_sub, '#FEF08A', W, shadow=False)
    draw_text_centered(draw, cy1 + 44, '舒緩全身緊繃 ‧ 同時把愛心傳遞出去', f_price_sub, '#FFFBEB', W, shadow=False)

    # Item 1
    b1_y = cy1 + 96
    draw.rounded_rectangle([cx1 + 20, b1_y, cx2 - 20, b1_y + 105], radius=14, fill='#2B1B13', outline='#B45309', width=1)
    bw1, bh1 = get_text_size(f_badge, '好禮相贈')
    draw.rounded_rectangle([cx1 + 35, b1_y + 14, cx1 + 35 + bw1 + 20, b1_y + 14 + bh1 + 10], radius=8, fill='#D97706')
    draw.text((cx1 + 45, b1_y + 18), '好禮相贈', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 35 + bw1 + 32, b1_y + 16), '總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#FDE68A')
    draw.text((cx1 + 35, b1_y + 60), '30 年武術精粹 ‧ 居家自我經絡鬆身養生心法', font=f_item_desc, fill='#CBD5E1')

    # Item 2
    b2_y = b1_y + 120
    draw.rounded_rectangle([cx1 + 20, b2_y, cx2 - 20, b2_y + 105], radius=14, fill='#2B1B13', outline='#B45309', width=1)
    bw2, bh2 = get_text_size(f_badge, '大師親調')
    draw.rounded_rectangle([cx1 + 35, b2_y + 14, cx1 + 35 + bw2 + 20, b2_y + 14 + bh2 + 10], radius=8, fill='#0284C7')
    draw.text((cx1 + 45, b2_y + 18), '大師親調', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 35 + bw2 + 32, b2_y + 16), '專業單部位整復調理 乙次', font=f_item_title, fill='#38BDF8')
    draw.text((cx1 + 35, b2_y + 60), '大師親自調理 ‧ 深度釋放緊繃 ‧ 鬆通筋膜', font=f_item_desc, fill='#CBD5E1')

    # Slogan
    draw_text_centered(draw, cy1 + 385, '★ 名額極度有限 ‧ 現場依順序叫號 ‧ 額滿即止 ★', ImageFont.truetype(FONT_BOLD, 22), '#34D399', W, shadow=False)

    # 4. Info Card
    bx1, by1, bx2, by2 = 40, 635, W - 40, 865
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=18, fill='#17181D', outline='#4B5563', width=2)
    
    lw, lh = get_text_size(f_info_label, '活動時間')
    draw.rounded_rectangle([bx1 + 25, by1 + 16, bx1 + 25 + lw + 20, by1 + 16 + lh + 10], radius=8, fill='#374151')
    draw.text((bx1 + 35, by1 + 20), '活動時間', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 18), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 54), '※ 13:30 開始發放號碼牌 ‧ 名額有限搶完即止', font=f_info_sub, fill='#F87171')

    draw.rounded_rectangle([bx1 + 25, by1 + 95, bx1 + 25 + lw + 20, by1 + 95 + lh + 10], radius=8, fill='#374151')
    draw.text((bx1 + 35, by1 + 99), '活動地點', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 97), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 133), '新北市板橋區館前西路 152-1 號（近府中商圈）', font=f_info_sub, fill='#94A3B8')

    draw.rounded_rectangle([bx1 + 25, by1 + 172, bx1 + 25 + lw + 20, by1 + 172 + lh + 10], radius=8, fill='#0284C7')
    draw.text((bx1 + 35, by1 + 176), '預約連結', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 174), 'LINE ID：@429rnxzs ｜ 網址：lin.ee/tQpJVq0', font=f_info_val, fill='#38BDF8')

    # 5. Bottom CTA
    draw.rounded_rectangle([40, 885, W - 40, 1045], radius=20, fill='#06C755', outline='#22C55E', width=2)
    draw_text_centered(draw, 908, '立即加 LINE 預約：@429rnxzs', f_cta, '#FFFFFF', W, shadow=True, shadow_color=(0, 60, 20, 160))
    draw_text_centered(draw, 975, '私訊發送「我要預約公益義整」光速保留名額！', f_cta_sub, '#F0FDF4', W, shadow=False)

    filename = '02_FB貼文海報_1比1正方形社群版.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print('Generated Square 1:1 Poster')

# ==============================================================================
# POSTER 3: 溫暖紅金大師義診版 (1080 x 1080)
# ==============================================================================
def create_poster_charity_warm():
    W, H = 1080, 1080
    img = Image.new('RGB', (W, H), color='#180B0E')
    draw = ImageDraw.Draw(img)

    c_top = (85, 18, 25)
    c_bot = (20, 10, 12)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    f_tag = ImageFont.truetype(FONT_BOLD, 26)
    f_main = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_BOLD, 28)
    f_price = ImageFont.truetype(FONT_BOLD, 44)
    f_price_sub = ImageFont.truetype(FONT_BOLD, 24)
    f_badge = ImageFont.truetype(FONT_BOLD, 22)
    f_item_title = ImageFont.truetype(FONT_BOLD, 30)
    f_item_desc = ImageFont.truetype(FONT_REG, 24)
    f_info_label = ImageFont.truetype(FONT_BOLD, 24)
    f_info_val = ImageFont.truetype(FONT_BOLD, 26)
    f_info_sub = ImageFont.truetype(FONT_REG, 22)
    f_cta = ImageFont.truetype(FONT_BOLD, 36)
    f_cta_sub = ImageFont.truetype(FONT_BOLD, 24)

    # 1. Top Banner
    tag = '【愛心公益義整 ‧ 所得全額捐贈伊甸基金會】'
    tw, th = get_text_size(f_tag, tag)
    draw.rounded_rectangle([(W - tw)//2 - 25, 24, (W + tw)//2 + 25, 24 + th + 16], radius=18, fill='#B91C1C', outline='#FECDD3', width=1)
    draw.text(((W - tw)//2, 32), tag, font=f_tag, fill='#FFFBEB')

    # 2. Master Title
    draw_text_centered(draw, 78, '江夏創始人「黃正斌 總館長」親臨板橋', f_main, '#FFD700', W)
    draw_text_centered(draw, 138, '大師親調 ‧ 舒緩筋骨 ‧ 一起把愛傳遞出去', f_sub, '#FDE68A', W)

    # 3. Price Card
    cx1, cy1, cx2, cy2 = 45, 185, W - 45, 620
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=22, fill='#261118', outline='#E11D48', width=2)
    
    # Top header of card (Roomy 115px height)
    draw.rounded_rectangle([cx1 + 2, cy1 + 2, cx2 - 2, cy1 + 115], radius=20, fill='#831843')
    draw_text_centered(draw, cy1 + 16, '超值公益價 NT$ 500 元', f_price, '#FFFBEB', W, shadow=False)
    draw_text_centered(draw, cy1 + 75, '所得全數捐贈伊甸基金會 ‧ 幫助弱勢家庭', f_price_sub, '#FCE7F3', W, shadow=False)

    # Item 1
    b1_y = cy1 + 130
    draw.rounded_rectangle([cx1 + 20, b1_y, cx2 - 20, b1_y + 95], radius=12, fill='#381420', outline='#F43F5E', width=1)
    bw1, bh1 = get_text_size(f_badge, '贈實體書')
    draw.rounded_rectangle([cx1 + 35, b1_y + 14, cx1 + 35 + bw1 + 20, b1_y + 14 + bh1 + 10], radius=6, fill='#F59E0B')
    draw.text((cx1 + 45, b1_y + 18), '贈實體書', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 35 + bw1 + 32, b1_y + 16), '總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#FDE047')
    draw.text((cx1 + 35, b1_y + 58), '30年武術精華 ‧ 居家自我經絡鬆身養生心法', font=f_item_desc, fill='#E2E8F0')

    # Item 2
    b2_y = b1_y + 110
    draw.rounded_rectangle([cx1 + 20, b2_y, cx2 - 20, b2_y + 95], radius=12, fill='#381420', outline='#F43F5E', width=1)
    bw2, bh2 = get_text_size(f_badge, '大師調理')
    draw.rounded_rectangle([cx1 + 35, b2_y + 14, cx1 + 35 + bw2 + 20, b2_y + 14 + bh2 + 10], radius=6, fill='#0284C7')
    draw.text((cx1 + 45, b2_y + 18), '大師調理', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 35 + bw2 + 32, b2_y + 16), '專業單部位整復調理 乙次', font=f_item_title, fill='#38BDF8')
    draw.text((cx1 + 35, b2_y + 58), '針對長期肩頸/腰背僵硬深層放鬆，調理通暢', font=f_item_desc, fill='#E2E8F0')

    # Slogan
    draw_text_centered(draw, cy1 + 388, '★ 限量名額 ‧ 現場依順序叫號 ‧ 額滿即止 ★', ImageFont.truetype(FONT_BOLD, 22), '#F472B6', W, shadow=False)

    # 4. Info Card
    bx1, by1, bx2, by2 = 45, 635, W - 45, 865
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=18, fill='#1A1720', outline='#4B5563', width=2)
    
    lw, lh = get_text_size(f_info_label, '活動時間')
    draw.rounded_rectangle([bx1 + 25, by1 + 16, bx1 + 25 + lw + 20, by1 + 16 + lh + 10], radius=8, fill='#374151')
    draw.text((bx1 + 35, by1 + 20), '活動時間', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 18), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 54), '※ 13:30 開始發放號碼牌 ‧ 依順序叫號體驗', font=f_info_sub, fill='#FBBF24')

    draw.rounded_rectangle([bx1 + 25, by1 + 95, bx1 + 25 + lw + 20, by1 + 95 + lh + 10], radius=8, fill='#374151')
    draw.text((bx1 + 35, by1 + 99), '活動地點', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 97), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 133), '新北市板橋區館前西路 152-1 號（近府中商圈）', font=f_info_sub, fill='#94A3B8')

    draw.rounded_rectangle([bx1 + 25, by1 + 172, bx1 + 25 + lw + 20, by1 + 172 + lh + 10], radius=8, fill='#0284C7')
    draw.text((bx1 + 35, by1 + 176), '線上搶位', font=f_info_label, fill='#FFFFFF')
    draw.text((bx1 + 25 + lw + 35, by1 + 174), '加 LINE：@429rnxzs ｜ 私訊「我要預約公益義整」', font=f_info_val, fill='#38BDF8')

    # 5. Bottom CTA
    draw.rounded_rectangle([45, 885, W - 45, 1045], radius=20, fill='#06C755', outline='#22C55E', width=2)
    draw_text_centered(draw, 908, '點此加 LINE 預約：@429rnxzs', f_cta, '#FFFFFF', W, shadow=True, shadow_color=(0, 60, 20, 160))
    draw_text_centered(draw, 975, '名額極度有限 ‧ 搶完即止 ‧ 立即卡位', f_cta_sub, '#F0FDF4', W, shadow=False)

    filename = '03_FB貼文海報_暖心紅金公益版.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print('Generated Warm Heart Charity Poster')

# ==============================================================================
# POSTER 4: 4:5 門市實景加持版 (1080 x 1350)
# ==============================================================================
def create_poster_real_exterior_4_5():
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#0E0A08')
    draw = ImageDraw.Draw(img)
    
    c_top = (35, 22, 16)
    c_bot = (10, 8, 7)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    if os.path.exists(photo_exterior):
        bg_photo = Image.open(photo_exterior).convert('RGBA')
        pw, ph = bg_photo.size
        crop_h = int(pw * 0.75)
        bg_crop = bg_photo.crop((0, 0, pw, min(ph, crop_h)))
        bg_resized = bg_crop.resize((W, int(W * 0.7)), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', bg_resized.size, 55)
        img_rgba = img.convert('RGBA')
        img_rgba.paste(bg_resized, (0, 0), mask)
        img = img_rgba.convert('RGB')
        draw = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(FONT_BOLD, 26)
    f_hook = ImageFont.truetype(FONT_BOLD, 30)
    f_title = ImageFont.truetype(FONT_BOLD, 52)
    f_name = ImageFont.truetype(FONT_BOLD, 68)
    f_price_tag = ImageFont.truetype(FONT_BOLD, 52)
    f_price_sub = ImageFont.truetype(FONT_BOLD, 26)
    f_badge = ImageFont.truetype(FONT_BOLD, 24)
    f_item_title = ImageFont.truetype(FONT_BOLD, 32)
    f_item_desc = ImageFont.truetype(FONT_REG, 26)
    f_slogan = ImageFont.truetype(FONT_BOLD, 30)
    f_info_label = ImageFont.truetype(FONT_BOLD, 26)
    f_info_val = ImageFont.truetype(FONT_BOLD, 28)
    f_info_sub = ImageFont.truetype(FONT_REG, 24)
    f_cta_btn = ImageFont.truetype(FONT_BOLD, 40)
    f_cta_sub = ImageFont.truetype(FONT_BOLD, 26)

    # 1. Top Brand Tag
    tag_text = '江夏傳統整復推拿 ‧ 板橋館前西路門市【大師站台】'
    tw, th = get_text_size(f_tag, tag_text)
    draw.rounded_rectangle([(W - tw)//2 - 30, 40, (W + tw)//2 + 30, 40 + th + 18], radius=20, fill='#B45309', outline='#F59E0B', width=2)
    draw.text(((W - tw)//2, 48), tag_text, font=f_tag, fill='#FFFFFF')

    # 2. Main Title Section
    draw_text_centered(draw, 115, '超過45家媒體報導 ‧ 武英門創始人親臨站台', f_hook, '#FDE68A', W)
    draw_text_centered(draw, 162, '創始人「黃正斌 總館長」', f_name, '#FFD700', W, shadow=True, offset=(3, 3))
    draw_text_centered(draw, 248, '親臨板橋館 ‧ 公益義整！', f_title, '#FFFFFF', W, shadow=True, offset=(2, 2))

    # 3. Main Center Card
    cx1, cy1, cx2, cy2 = 45, 335, W - 45, 875
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=28, fill='#1B130E', outline='#D97706', width=3)
    
    # Red Price Banner Header
    draw.rounded_rectangle([cx1 + 3, cy1 + 3, cx2 - 3, cy1 + 115], radius=25, fill='#991B1B')
    draw_text_centered(draw, cy1 + 16, '超值銅板公益價 NT$ 500 元', f_price_tag, '#FFFBEB', W, shadow=False)
    draw_text_centered(draw, cy1 + 76, '★ 所得全額捐贈【伊甸基金會】★', f_price_sub, '#FEF08A', W, shadow=False)

    # Benefit 1 Card
    b1_y = cy1 + 140
    draw.rounded_rectangle([cx1 + 25, b1_y, cx2 - 25, b1_y + 130], radius=18, fill='#291A12', outline='#B45309', width=2)
    bw, bh = get_text_size(f_badge, '好禮相贈')
    draw.rounded_rectangle([cx1 + 45, b1_y + 20, cx1 + 45 + bw + 24, b1_y + 20 + bh + 14], radius=10, fill='#D97706')
    draw.text((cx1 + 57, b1_y + 26), '好禮相贈', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 45 + bw + 40, b1_y + 22), '總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#FDE68A')
    draw.text((cx1 + 45, b1_y + 76), '創始人 30 年武學與經絡鬆身心法 ‧ 最實用的日常養生寶典', font=f_item_desc, fill='#CBD5E1')

    # Benefit 2 Card
    b2_y = b1_y + 150
    draw.rounded_rectangle([cx1 + 25, b2_y, cx2 - 25, b2_y + 130], radius=18, fill='#291A12', outline='#B45309', width=2)
    bw2, bh2 = get_text_size(f_badge, '大師親調')
    draw.rounded_rectangle([cx1 + 45, b2_y + 20, cx1 + 45 + bw2 + 24, b2_y + 20 + bh2 + 14], radius=10, fill='#0284C7')
    draw.text((cx1 + 57, b2_y + 26), '大師親調', font=f_badge, fill='#FFFFFF')
    draw.text((cx1 + 45 + bw2 + 40, b2_y + 22), '專業單部位整復調理 乙次', font=f_item_title, fill='#38BDF8')
    draw.text((cx1 + 45, b2_y + 76), '正統武術內勁鬆拿 ‧ 深層釋放長年緊繃與僵硬 ‧ 活絡通暢', font=f_item_desc, fill='#CBD5E1')

    # Slogan inside card
    draw_text_centered(draw, cy1 + 460, '舒緩全身緊繃 ‧ 同時把愛心溫暖傳遞出去', f_slogan, '#34D399', W, shadow=False)

    # 4. Event Time & Location Box
    bx1, by1, bx2, by2 = 45, 900, W - 45, 1100
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=20, fill='#16171B', outline='#4B5563', width=2)
    
    lbl_w, lbl_h = get_text_size(f_info_label, '活動時間')
    draw.rounded_rectangle([bx1 + 30, by1 + 20, bx1 + 30 + lbl_w + 24, by1 + 20 + lbl_h + 12], radius=8, fill='#374151')
    draw.text((bx1 + 42, by1 + 25), '活動時間', font=f_info_label, fill='#F9FAFB')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 22), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 62), '※ 13:30 開始現場報到拿號碼牌 ‧ 名額有限搶完即止', font=f_info_sub, fill='#F87171')

    draw.rounded_rectangle([bx1 + 30, by1 + 112, bx1 + 30 + lbl_w + 24, by1 + 112 + lbl_h + 12], radius=8, fill='#374151')
    draw.text((bx1 + 42, by1 + 117), '活動地點', font=f_info_label, fill='#F9FAFB')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 114), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 30 + lbl_w + 45, by1 + 154), '新北市板橋區館前西路 152-1 號（近府中捷運站）', font=f_info_sub, fill='#94A3B8')

    # 5. Bottom CTA
    cta_x1, cta_y1, cta_x2, cta_y2 = 45, 1125, W - 45, 1310
    draw.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=24, fill='#06C755', outline='#22C55E', width=2)
    draw_text_centered(draw, cta_y1 + 26, '立即加 LINE 預約：@429rnxzs', f_cta_btn, '#FFFFFF', W, shadow=True, shadow_color=(0, 60, 20, 160))
    draw_text_centered(draw, cta_y1 + 95, '私訊發送「我要預約公益義整」光速保留名額！', f_cta_sub, '#F0FDF4', W, shadow=False)

    filename = '04_FB貼文海報_實體門面加持版.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print('Generated Real Exterior 4:5 Poster')

if __name__ == '__main__':
    create_poster_flagship_4_5()
    create_poster_square_1_1()
    create_poster_charity_warm()
    create_poster_real_exterior_4_5()
