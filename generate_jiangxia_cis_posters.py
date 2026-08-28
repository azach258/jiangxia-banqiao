# -*- coding: utf-8 -*-
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_dir = r'C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館'
out_dir = os.path.join(base_dir, 'fb_charity_posters')
artifact_dir = r'C:/Users/love_/.gemini/antigravity/brain/cc0683a0-544d-4081-a6ca-781abf203c0f'
os.makedirs(out_dir, exist_ok=True)
os.makedirs(artifact_dir, exist_ok=True)

photo_wall = r'C:/Users/love_/AppData/Local/hermes/cache/images/img_015914eafd8a.jpg'
photo_exterior = r'C:/Users/love_/AppData/Local/hermes/cache/images/img_81edf849663c.jpg'
photo_technique = r'C:/Users/love_/AppData/Local/hermes/cache/images/img_d00d4008c009.jpg'

FONT_KAI = 'C:/Windows/Fonts/kaiu.ttf'
FONT_JH_BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
FONT_JH_REG = 'C:/Windows/Fonts/msjh.ttc'

def get_text_size(font, text):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_text_centered(draw, y, text, font, fill, W, shadow=False, shadow_color=(0, 0, 0, 160), offset=(2, 2)):
    tw, th = get_text_size(font, text)
    x = (W - tw) // 2
    if shadow:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)
    return tw, th

# Classical Chinese Seal (朱印篆刻)
def draw_seal_badge(draw, pos, text, font, bg_color='#9E1A1A', border_color='#7A1212', text_color='#FFFFFF', padding=(10, 6)):
    x, y = pos
    tw, th = get_text_size(font, text)
    px, py = padding
    box = [x, y, x + tw + px * 2, y + th + py * 2]
    draw.rounded_rectangle(box, radius=6, fill=bg_color, outline=border_color, width=2)
    draw.rounded_rectangle([box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2], radius=4, outline='#FFE4E6', width=1)
    draw.text((x + px, y + py - 2), text, font=font, fill=text_color)
    return box[2] - box[0]

# Classical Chinese Square Seal (2-char vertical/square stamp)
def draw_square_seal(draw, pos, text, font, size=52, fill_color='#9E1A1A', border_color='#7A1212', text_color='#FFFFFF'):
    x, y = pos
    draw.rounded_rectangle([x, y, x + size, y + size], radius=8, fill=fill_color, outline=border_color, width=2)
    draw.rounded_rectangle([x + 3, y + 3, x + size - 3, y + size - 3], radius=6, outline='#FFE4E6', width=1)
    tw, th = get_text_size(font, text)
    draw.text((x + (size - tw)//2, y + (size - th)//2 - 2), text, font=font, fill=text_color)

# Classical Chinese Double-Line Border with Corner Accents
def draw_classical_border(draw, rect, border_color='#B8860B', line_width=2, gap=6):
    x1, y1, x2, y2 = rect
    draw.rectangle([x1, y1, x2, y2], outline=border_color, width=line_width)
    draw.rectangle([x1 + gap, y1 + gap, x2 - gap, y2 - gap], outline=border_color, width=1)
    cs = gap + 6
    draw.rectangle([x1, y1, x1 + cs, y1 + cs], fill=border_color)
    draw.rectangle([x2 - cs, y1, x2, y1 + cs], fill=border_color)
    draw.rectangle([x1, y2 - cs, x1 + cs, y2], fill=border_color)
    draw.rectangle([x2 - cs, y2 - cs, x2, y2], fill=border_color)

# ==============================================================================
# POSTER 1: 【江夏典雅宣紙書法旗艦版】 (4:5 / 1080 x 1350)
# ==============================================================================
def create_jiangxia_cis_ricepaper_4_5():
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#FAF6EF')
    draw = ImageDraw.Draw(img)

    # Gradient: Ivory Cream to Warm Paper
    c_top = (252, 250, 246)
    c_bot = (240, 232, 218)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Classical Gold Border
    draw_classical_border(draw, (28, 28, W - 28, H - 28), border_color='#C5A059', line_width=2, gap=6)

    # Fonts
    f_seal = ImageFont.truetype(FONT_KAI, 22)
    f_badge = ImageFont.truetype(FONT_KAI, 22)
    f_brand_top = ImageFont.truetype(FONT_KAI, 32)
    f_hero_sub = ImageFont.truetype(FONT_KAI, 32)
    f_hero_main = ImageFont.truetype(FONT_KAI, 68)
    f_hero_action = ImageFont.truetype(FONT_KAI, 46)
    
    f_card_head = ImageFont.truetype(FONT_KAI, 42)
    f_price_note = ImageFont.truetype(FONT_KAI, 28)
    
    f_item_title = ImageFont.truetype(FONT_KAI, 32)
    f_item_desc = ImageFont.truetype(FONT_JH_REG, 25)
    f_slogan = ImageFont.truetype(FONT_KAI, 30)
    
    f_info_label = ImageFont.truetype(FONT_KAI, 24)
    f_info_val = ImageFont.truetype(FONT_JH_BOLD, 28)
    f_info_sub = ImageFont.truetype(FONT_JH_REG, 24)
    
    f_cta_main = ImageFont.truetype(FONT_KAI, 38)
    f_cta_sub = ImageFont.truetype(FONT_JH_BOLD, 24)

    # 1. Top Header
    y_pos = 52
    draw_square_seal(draw, (65, y_pos - 6), '武英', f_seal, size=50, fill_color='#9E1A1A')
    draw_square_seal(draw, (W - 65 - 50, y_pos - 6), '江夏', f_seal, size=50, fill_color='#9E1A1A')
    
    draw_text_centered(draw, y_pos, '江夏傳統整復推拿 ‧ 板橋館', f_brand_top, '#8B1E1F', W)
    draw_text_centered(draw, y_pos + 44, '【 源自武英門 ‧ 超過 30 年老字號正統內勁鬆拿 】', ImageFont.truetype(FONT_KAI, 24), '#5C4033', W)

    draw.line([(120, y_pos + 82), (W - 120, y_pos + 82)], fill='#C5A059', width=2)
    draw.ellipse([(W//2 - 6, y_pos + 77), (W//2 + 6, y_pos + 89)], fill='#9E1A1A')

    # 2. Main Announcement (大師親自出手)
    y_pos = 155
    draw_text_centered(draw, y_pos, '平常預約不到的大師級調理 ‧ 限時親臨板橋', f_hero_sub, '#78350F', W)
    
    y_pos += 48
    draw_text_centered(draw, y_pos, '創始人「黃正斌 總館長」', f_hero_main, '#1C1917', W, shadow=True, shadow_color=(210, 190, 160, 130), offset=(2, 2))
    
    y_pos += 86
    draw_text_centered(draw, y_pos, '親自出手 ‧ 愛心公益義整', f_hero_action, '#9E1A1A', W)

    # 3. Main Center Charity Plaque Card
    cx1, cy1, cx2, cy2 = 55, 365, W - 55, 885
    draw.rectangle([cx1, cy1, cx2, cy2], fill='#FFFDF8', outline='#C5A059', width=2)
    draw.rectangle([cx1 + 4, cy1 + 4, cx2 - 4, cy2 - 4], outline='#E5D5BA', width=1)

    # Red Plaque Banner
    draw.rectangle([cx1 + 4, cy1 + 4, cx2 - 4, cy1 + 115], fill='#9E1A1A')
    draw.rectangle([cx1 + 8, cy1 + 8, cx2 - 8, cy1 + 111], outline='#DFB75A', width=1)
    
    draw_text_centered(draw, cy1 + 18, '✦ 銅板公益價 只要 NT$ 500 元 ✦', f_card_head, '#FFFBEB', W)
    draw_text_centered(draw, cy1 + 72, '（ 本次活動所得全數捐贈【伊甸基金會】幫助弱勢家庭 ）', f_price_note, '#FDE68A', W)

    # Offer Item 1
    b1_y = cy1 + 138
    draw.rectangle([cx1 + 25, b1_y, cx2 - 25, b1_y + 125], fill='#F8F3EA', outline='#D6C2A1', width=1)
    w1 = draw_seal_badge(draw, (cx1 + 40, b1_y + 18), '好禮相贈', f_badge, bg_color='#8B1E1F', border_color='#5C1010')
    draw.text((cx1 + 40 + w1 + 18, b1_y + 20), '贈｜總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#1C1917')
    draw.text((cx1 + 45, b1_y + 75), '創始人 30 年武學與經絡鬆身心法 ‧ 最實用的日常自我養生寶典', font=f_item_desc, fill='#4B5563')

    # Offer Item 2
    b2_y = b1_y + 145
    draw.rectangle([cx1 + 25, b2_y, cx2 - 25, b2_y + 125], fill='#F8F3EA', outline='#D6C2A1', width=1)
    w2 = draw_seal_badge(draw, (cx1 + 40, b2_y + 18), '大師親調', f_badge, bg_color='#9E1A1A', border_color='#7A1212')
    draw.text((cx1 + 40 + w2 + 18, b2_y + 20), '調｜專業單部位整復調理 乙次（大師親自調理）', font=f_item_title, fill='#1C1917')
    draw.text((cx1 + 45, b2_y + 75), '正統武術內勁鬆拿 ‧ 溫和深層釋放長年緊繃與僵硬 ‧ 活絡通暢', font=f_item_desc, fill='#4B5563')

    # Zen Slogan
    draw_text_centered(draw, cy1 + 448, '「 心靜身靈 ‧ 氣斂勁整 ‧ 舒緩緊繃 ‧ 把愛傳遞 」', f_slogan, '#8B1E1F', W)

    # 4. Event Information Card
    bx1, by1, bx2, by2 = 55, 910, W - 55, 1120
    draw.rectangle([bx1, by1, bx2, by2], fill='#F3EBE0', outline='#C5A059', width=2)
    draw.rectangle([bx1 + 4, by1 + 4, bx2 - 4, by2 - 4], outline='#E5D5BA', width=1)

    # Row 1: Time
    tw1 = draw_seal_badge(draw, (bx1 + 25, by1 + 18), '活動時間', f_info_label, bg_color='#5C4033', border_color='#3E2718')
    draw.text((bx1 + 25 + tw1 + 20, by1 + 18), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#1C1917')
    draw.text((bx1 + 25 + tw1 + 20, by1 + 56), '※ 13:30 開始現場報到領取號碼牌 ‧ 名額極度有限 ‧ 搶完即止', font=f_info_sub, fill='#9E1A1A')

    # Row 2: Location
    tw2 = draw_seal_badge(draw, (bx1 + 25, by1 + 115), '活動地點', f_info_label, bg_color='#5C4033', border_color='#3E2718')
    draw.text((bx1 + 25 + tw2 + 20, by1 + 114), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#1C1917')
    draw.text((bx1 + 25 + tw2 + 20, by1 + 152), '新北市板橋區館前西路 152-1 號（近捷運府中站 / 府中商圈）', font=f_info_sub, fill='#4B5563')

    # 5. Bottom CTA
    cta_x1, cta_y1, cta_x2, cta_y2 = 55, 1145, W - 55, 1295
    draw.rectangle([cta_x1, cta_y1, cta_x2, cta_y2], fill='#9E1A1A', outline='#DFB75A', width=3)
    draw.rectangle([cta_x1 + 4, cta_y1 + 4, cta_x2 - 4, cta_y2 - 4], outline='#FCA5A5', width=1)
    
    draw_text_centered(draw, cta_y1 + 22, '立即預約 ‧ 加入官方 LINE：@429rnxzs', f_cta_main, '#FFFBEB', W, shadow=True, shadow_color=(80, 10, 10, 200))
    draw_text_centered(draw, cta_y1 + 82, '私訊發送「我要預約公益義整」光速保留大師調理時段！', f_cta_sub, '#FDE68A', W)

    filename = '01_江夏CIS_宣紙書法旗艦版_4比5.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print(f'Generated: {filename}')

# ==============================================================================
# POSTER 2: 【江夏典雅黑檀紅木匾額版】 (4:5 / 1080 x 1350)
# ==============================================================================
def create_jiangxia_cis_wood_gold_4_5():
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#1C100B')
    draw = ImageDraw.Draw(img)

    c_top = (45, 25, 18)
    c_bot = (18, 10, 7)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    if os.path.exists(photo_exterior):
        store_img = Image.open(photo_exterior).convert('RGBA')
        sw, sh = store_img.size
        store_crop = store_img.crop((0, 0, sw, int(sw * 0.7)))
        store_resized = store_crop.resize((W, int(W * 0.7)), Image.Resampling.LANCZOS)
        mask = Image.new('L', store_resized.size, 38)
        img_rgba = img.convert('RGBA')
        img_rgba.paste(store_resized, (0, 0), mask)
        img = img_rgba.convert('RGB')
        draw = ImageDraw.Draw(img)

    draw_classical_border(draw, (28, 28, W - 28, H - 28), border_color='#D4AF37', line_width=3, gap=8)

    # Fonts
    f_seal = ImageFont.truetype(FONT_KAI, 22)
    f_badge = ImageFont.truetype(FONT_KAI, 22)
    f_brand = ImageFont.truetype(FONT_KAI, 34)
    f_sub = ImageFont.truetype(FONT_KAI, 30)
    f_name = ImageFont.truetype(FONT_KAI, 70)
    f_action = ImageFont.truetype(FONT_KAI, 46)
    
    f_card_head = ImageFont.truetype(FONT_KAI, 42)
    f_price_sub = ImageFont.truetype(FONT_KAI, 28)
    
    f_item_title = ImageFont.truetype(FONT_KAI, 32)
    f_item_desc = ImageFont.truetype(FONT_JH_REG, 25)
    f_slogan = ImageFont.truetype(FONT_KAI, 30)
    
    f_info_label = ImageFont.truetype(FONT_KAI, 24)
    f_info_val = ImageFont.truetype(FONT_JH_BOLD, 28)
    f_info_sub = ImageFont.truetype(FONT_JH_REG, 24)
    
    f_cta_main = ImageFont.truetype(FONT_KAI, 38)
    f_cta_sub = ImageFont.truetype(FONT_JH_BOLD, 24)

    # 1. Header
    y_pos = 52
    draw_square_seal(draw, (65, y_pos - 6), '武英', f_seal, size=50, fill_color='#A82222', border_color='#DFB75A')
    draw_square_seal(draw, (W - 65 - 50, y_pos - 6), '江夏', f_seal, size=50, fill_color='#A82222', border_color='#DFB75A')
    
    draw_text_centered(draw, y_pos, '江夏傳統整復推拿 ‧ 板橋門市', f_brand, '#DFB75A', W, shadow=True, offset=(2, 2))
    draw_text_centered(draw, y_pos + 44, '【 榮獲海內外 45 家媒體專訪 ‧ 正統武術內勁鬆拿 】', ImageFont.truetype(FONT_KAI, 24), '#E5D5BA', W)

    draw.line([(120, y_pos + 82), (W - 120, y_pos + 82)], fill='#D4AF37', width=2)
    draw.ellipse([(W//2 - 6, y_pos + 77), (W//2 + 6, y_pos + 89)], fill='#9E1A1A')

    # 2. Main Announcement
    y_pos = 155
    draw_text_centered(draw, y_pos, '平常預約不到的大師級調理 ‧ 隆重親臨義整', f_sub, '#FDE68A', W)
    y_pos += 48
    draw_text_centered(draw, y_pos, '創始人「黃正斌 總館長」', f_name, '#FFD700', W, shadow=True, shadow_color=(0, 0, 0, 220), offset=(3, 3))
    y_pos += 86
    draw_text_centered(draw, y_pos, '親臨板橋館 ‧ 公益義整！', f_action, '#FFFFFF', W, shadow=True, offset=(2, 2))

    # 3. Main Center Plaque
    cx1, cy1, cx2, cy2 = 55, 365, W - 55, 885
    draw.rectangle([cx1, cy1, cx2, cy2], fill='#281710', outline='#D4AF37', width=2)
    draw.rectangle([cx1 + 5, cy1 + 5, cx2 - 5, cy2 - 5], outline='#78350F', width=1)

    # Red Plaque inside
    draw.rectangle([cx1 + 4, cy1 + 4, cx2 - 4, cy1 + 115], fill='#881313')
    draw.rectangle([cx1 + 8, cy1 + 8, cx2 - 8, cy1 + 111], outline='#DFB75A', width=1)
    draw_text_centered(draw, cy1 + 18, '✦ 銅板公益價 只要 NT$ 500 元 ✦', f_card_head, '#FFFBEB', W)
    draw_text_centered(draw, cy1 + 72, '（ 本次所得全數捐贈【伊甸基金會】傳遞愛心 ）', f_price_sub, '#FDE68A', W)

    # Item 1
    b1_y = cy1 + 138
    draw.rectangle([cx1 + 25, b1_y, cx2 - 25, b1_y + 125], fill='#382017', outline='#B8860B', width=1)
    w1 = draw_seal_badge(draw, (cx1 + 40, b1_y + 18), '好禮相贈', f_badge, bg_color='#A82222', border_color='#DFB75A')
    draw.text((cx1 + 40 + w1 + 18, b1_y + 20), '贈｜總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#FFD700')
    draw.text((cx1 + 45, b1_y + 75), '創始人 30 年武學與經絡鬆身心法 ‧ 最實用的日常自我養生寶典', font=f_item_desc, fill='#E2E8F0')

    # Item 2
    b2_y = b1_y + 145
    draw.rectangle([cx1 + 25, b2_y, cx2 - 25, b2_y + 125], fill='#382017', outline='#B8860B', width=1)
    w2 = draw_seal_badge(draw, (cx1 + 40, b2_y + 18), '大師親調', f_badge, bg_color='#A82222', border_color='#DFB75A')
    draw.text((cx1 + 40 + w2 + 18, b2_y + 20), '調｜專業單部位整復調理 乙次（大師親自調理）', font=f_item_title, fill='#38BDF8')
    draw.text((cx1 + 45, b2_y + 75), '正統武術內勁鬆拿 ‧ 溫和深層釋放長年緊繃與僵硬 ‧ 活絡通暢', font=f_item_desc, fill='#E2E8F0')

    draw_text_centered(draw, cy1 + 448, '「 心靜身靈 ‧ 氣斂勁整 ‧ 舒緩緊繃 ‧ 把愛傳遞 」', f_slogan, '#34D399', W)

    # 4. Info Card
    bx1, by1, bx2, by2 = 55, 910, W - 55, 1120
    draw.rectangle([bx1, by1, bx2, by2], fill='#20130E', outline='#A16207', width=2)

    tw1 = draw_seal_badge(draw, (bx1 + 25, by1 + 18), '活動時間', f_info_label, bg_color='#78350F', border_color='#D4AF37')
    draw.text((bx1 + 25 + tw1 + 20, by1 + 18), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + tw1 + 20, by1 + 56), '※ 13:30 開始現場報到拿號碼牌 ‧ 名額極度有限 ‧ 額滿即止', font=f_info_sub, fill='#F87171')

    tw2 = draw_seal_badge(draw, (bx1 + 25, by1 + 115), '活動地點', f_info_label, bg_color='#78350F', border_color='#D4AF37')
    draw.text((bx1 + 25 + tw2 + 20, by1 + 114), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#FFFFFF')
    draw.text((bx1 + 25 + tw2 + 20, by1 + 152), '新北市板橋區館前西路 152-1 號（近捷運府中站）', font=f_info_sub, fill='#CBD5E1')

    # 5. Bottom CTA
    cta_x1, cta_y1, cta_x2, cta_y2 = 55, 1145, W - 55, 1295
    draw.rectangle([cta_x1, cta_y1, cta_x2, cta_y2], fill='#881313', outline='#DFB75A', width=3)
    draw.rectangle([cta_x1 + 4, cta_y1 + 4, cta_x2 - 4, cta_y2 - 4], outline='#FCA5A5', width=1)
    
    draw_text_centered(draw, cta_y1 + 22, '立即預約 ‧ 加入官方 LINE：@429rnxzs', f_cta_main, '#FFFBEB', W, shadow=True, offset=(2, 2))
    draw_text_centered(draw, cta_y1 + 82, '私訊發送「我要預約公益義整」光速保留名額！', f_cta_sub, '#FDE68A', W)

    filename = '02_江夏CIS_黑檀紅木宗師版_4比5.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print(f'Generated: {filename}')

# ==============================================================================
# POSTER 3: 【江夏 1:1 正方形經典社群版】 (1080 x 1080)
# ==============================================================================
def create_jiangxia_cis_square_1_1():
    W, H = 1080, 1080
    img = Image.new('RGB', (W, H), color='#FAF6EF')
    draw = ImageDraw.Draw(img)

    c_top = (252, 250, 246)
    c_bot = (240, 232, 218)
    for y in range(H):
        ratio = y / H
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_classical_border(draw, (24, 24, W - 24, H - 24), border_color='#C5A059', line_width=2, gap=6)

    # Fonts
    f_seal = ImageFont.truetype(FONT_KAI, 20)
    f_badge = ImageFont.truetype(FONT_KAI, 20)
    f_brand = ImageFont.truetype(FONT_KAI, 28)
    f_name = ImageFont.truetype(FONT_KAI, 54)
    f_sub = ImageFont.truetype(FONT_KAI, 28)
    f_price_head = ImageFont.truetype(FONT_KAI, 36)
    f_price_sub = ImageFont.truetype(FONT_KAI, 24)
    f_item_title = ImageFont.truetype(FONT_KAI, 30)
    f_item_desc = ImageFont.truetype(FONT_JH_REG, 24)
    f_info_label = ImageFont.truetype(FONT_KAI, 22)
    f_info_val = ImageFont.truetype(FONT_JH_BOLD, 26)
    f_info_sub = ImageFont.truetype(FONT_JH_REG, 22)
    f_cta_main = ImageFont.truetype(FONT_KAI, 34)
    f_cta_sub = ImageFont.truetype(FONT_JH_BOLD, 22)

    # 1. Header
    draw_square_seal(draw, (45, 34), '武英', f_seal, size=44, fill_color='#9E1A1A')
    draw_square_seal(draw, (W - 45 - 44, 34), '江夏', f_seal, size=44, fill_color='#9E1A1A')
    
    draw_text_centered(draw, 38, '江夏傳統整復推拿 ‧ 板橋館【限時公益義整】', f_brand, '#8B1E1F', W)

    # 2. Main Title
    draw_text_centered(draw, 82, '創始人「黃正斌 總館長」親自出手！', f_name, '#1C1917', W)
    draw_text_centered(draw, 145, '30年正統武術內勁鬆拿 ‧ 平常預約不到的大師親調', f_sub, '#78350F', W)

    # 3. Main Center Card
    cx1, cy1, cx2, cy2 = 45, 192, W - 45, 625
    draw.rectangle([cx1, cy1, cx2, cy2], fill='#FFFDF8', outline='#C5A059', width=2)
    
    # Plaque Header
    draw.rectangle([cx1 + 2, cy1 + 2, cx2 - 2, cy1 + 82], fill='#9E1A1A')
    draw.rectangle([cx1 + 6, cy1 + 6, cx2 - 6, cy1 + 78], outline='#DFB75A', width=1)
    draw_text_centered(draw, cy1 + 12, '✦ 銅板公益價 只要 NT$ 500 元 ✦', f_price_head, '#FFFBEB', W)
    draw_text_centered(draw, cy1 + 50, '所得全額捐贈【伊甸基金會】‧ 舒緩緊繃 ‧ 溫暖傳遞', f_price_sub, '#FDE68A', W)

    # Item 1
    b1_y = cy1 + 96
    draw.rectangle([cx1 + 20, b1_y, cx2 - 20, b1_y + 100], fill='#F8F3EA', outline='#D6C2A1', width=1)
    w1 = draw_seal_badge(draw, (cx1 + 32, b1_y + 14), '好禮相贈', f_badge, bg_color='#8B1E1F', border_color='#5C1010')
    draw.text((cx1 + 32 + w1 + 16, b1_y + 16), '贈｜總館長親著《天能勁源·天能十字功》乙本', font=f_item_title, fill='#1C1917')
    draw.text((cx1 + 35, b1_y + 60), '30 年武術精粹 ‧ 居家自我經絡鬆身養生心法', font=f_item_desc, fill='#4B5563')

    # Item 2
    b2_y = b1_y + 115
    draw.rectangle([cx1 + 20, b2_y, cx2 - 20, b2_y + 100], fill='#F8F3EA', outline='#D6C2A1', width=1)
    w2 = draw_seal_badge(draw, (cx1 + 32, b2_y + 14), '大師親調', f_badge, bg_color='#9E1A1A', border_color='#7A1212')
    draw.text((cx1 + 32 + w2 + 16, b2_y + 16), '調｜專業單部位整復調理 乙次（大師親自調理）', font=f_item_title, fill='#1C1917')
    draw.text((cx1 + 35, b2_y + 60), '正統武術內勁鬆拿 ‧ 溫和深層釋放緊繃 ‧ 鬆通筋膜', font=f_item_desc, fill='#4B5563')

    draw_text_centered(draw, cy1 + 392, '★ 名額極度有限 ‧ 現場依順序叫號 ‧ 額滿即止 ★', ImageFont.truetype(FONT_KAI, 22), '#8B1E1F', W)

    # 4. Info Card
    bx1, by1, bx2, by2 = 45, 640, W - 45, 875
    draw.rectangle([bx1, by1, bx2, by2], fill='#F3EBE0', outline='#C5A059', width=2)

    tw1 = draw_seal_badge(draw, (bx1 + 20, by1 + 16), '活動時間', f_info_label, bg_color='#5C4033', border_color='#3E2718')
    draw.text((bx1 + 20 + tw1 + 16, by1 + 16), '2026 / 09 / 20（日） 14:00 - 21:00', font=f_info_val, fill='#1C1917')
    draw.text((bx1 + 20 + tw1 + 16, by1 + 52), '※ 13:30 開始發放號碼牌 ‧ 名額有限搶完即止', font=f_info_sub, fill='#9E1A1A')

    tw2 = draw_seal_badge(draw, (bx1 + 20, by1 + 92), '活動地點', f_info_label, bg_color='#5C4033', border_color='#3E2718')
    draw.text((bx1 + 20 + tw2 + 16, by1 + 92), '江夏傳統整復推拿 - 板橋館', font=f_info_val, fill='#1C1917')
    draw.text((bx1 + 20 + tw2 + 16, by1 + 126), '新北市板橋區館前西路 152-1 號（近府中商圈）', font=f_info_sub, fill='#4B5563')

    tw3 = draw_seal_badge(draw, (bx1 + 20, by1 + 165), '線上預約', f_info_label, bg_color='#8B1E1F', border_color='#5C1010')
    draw.text((bx1 + 20 + tw3 + 16, by1 + 165), '官方 LINE ID：@429rnxzs ｜ 網址：lin.ee/tQpJVq0', font=f_info_val, fill='#1C1917')

    # 5. Bottom CTA
    cta_x1, cta_y1, cta_x2, cta_y2 = 45, 895, W - 45, 1045
    draw.rectangle([cta_x1, cta_y1, cta_x2, cta_y2], fill='#9E1A1A', outline='#DFB75A', width=3)
    draw.rectangle([cta_x1 + 4, cta_y1 + 4, cta_x2 - 4, cta_y2 - 4], outline='#FCA5A5', width=1)
    
    draw_text_centered(draw, cta_y1 + 18, '點此加 LINE 預約：@429rnxzs', f_cta_main, '#FFFBEB', W, shadow=True, offset=(2, 2))
    draw_text_centered(draw, cta_y1 + 76, '私訊發送「我要預約公益義整」光速保留名額！', f_cta_sub, '#FDE68A', W)

    filename = '03_江夏CIS_宣紙朱印經典版_1比1.png'
    p_path = os.path.join(out_dir, filename)
    img.save(p_path, quality=95)
    shutil.copy(p_path, os.path.join(artifact_dir, filename))
    print(f'Generated: {filename}')

if __name__ == '__main__':
    create_jiangxia_cis_ricepaper_4_5()
    create_jiangxia_cis_wood_gold_4_5()
    create_jiangxia_cis_square_1_1()
    print('All 3 Jiangxia CIS Posters Updated Successfully!')
