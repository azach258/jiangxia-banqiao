import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Output directory
out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives"
os.makedirs(out_dir, exist_ok=True)

# 1080 x 1080 Meta Ad Standard Square
W, H = 1080, 1080

FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msjh.ttc"

font_hook = ImageFont.truetype(FONT_BOLD, 68)
font_sub = ImageFont.truetype(FONT_BOLD, 38)
font_cta = ImageFont.truetype(FONT_BOLD, 42)
font_tag = ImageFont.truetype(FONT_REG, 28)

ad_concepts = [
    {
        "filename": "meta_ad_A_office.png",
        "tag": "板橋館前西路 152-1 號 ‧ 賴師傅",
        "hook_line1": "下班後，肩頸像",
        "hook_line2": "頂著兩塊磚頭？",
        "sub": "源自武術內勁鬆拿 ‧ 溫和放鬆不硬抓",
        "cta": "💬 點擊發送訊息 ‧ 領取私訊專屬體驗",
        "bg_c1": "#1C1510",
        "bg_c2": "#2C2018",
        "accent": "#D4AF37",  # Gold
        "cta_bg": "#06C755"  # Meta/LINE Messenger Green
    },
    {
        "filename": "meta_ad_B_gentle.png",
        "tag": "板橋在地首選 ‧ 預約制免等待",
        "hook_line1": "整復推拿一定要",
        "hook_line2": "痛到流眼淚嗎？",
        "sub": "江夏內勁溫和舒緩 ‧ 乾淨明亮環境",
        "cta": "💬 點擊發送訊息 ‧ 線上諮詢預約",
        "bg_c1": "#13231B",
        "bg_c2": "#1A3326",
        "accent": "#10B981",  # Emerald
        "cta_bg": "#06C755"
    },
    {
        "filename": "meta_ad_C_posture.png",
        "tag": "板橋國前西路 152-1 號 ‧ 賴師傅親自調理",
        "hook_line1": "板橋上班族私藏",
        "hook_line2": "筋骨日常體態保養",
        "sub": "習慣翹腳/久坐疲勞 ‧ 客製化結構放鬆",
        "cta": "💬 點擊發送訊息 ‧ 私訊了解詳情",
        "bg_c1": "#1A1A24",
        "bg_c2": "#282838",
        "accent": "#818CF8",  # Soft Indigo Accent
        "cta_bg": "#06C755"
    }
]

for ad in ad_concepts:
    # Build warm, comfortable background with subtle texture
    img = Image.new("RGB", (W, H), color=ad["bg_c1"])
    draw = ImageDraw.Draw(img)
    
    # Vertical gradient
    r1, g1, b1 = int(ad["bg_c1"][1:3], 16), int(ad["bg_c1"][3:5], 16), int(ad["bg_c1"][5:7], 16)
    r2, g2, b2 = int(ad["bg_c2"][1:3], 16), int(ad["bg_c2"][3:5], 16), int(ad["bg_c2"][5:7], 16)
    for y in range(H):
        ratio = y / float(H)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Draw top tag pill
    draw.rounded_rectangle([70, 70, 620, 125], radius=15, fill="#382C22" if "office" in ad["filename"] else "#20382B")
    draw.text((95, 82), ad["tag"], font=font_tag, fill="#E6DAC8")
    
    # Inner main card container (Semi-transparent overlay card)
    card_box = [60, 160, W - 60, H - 70]
    draw.rounded_rectangle(card_box, radius=32, outline=ad["accent"], width=4)
    
    # Draw Big Hook Text
    draw.text((110, 260), ad["hook_line1"], font=font_hook, fill="#FFFFFF")
    draw.text((110, 360), ad["hook_line2"], font=font_hook, fill=ad["accent"])
    
    # Draw Subtitle
    draw.text((110, 520), ad["sub"], font=font_sub, fill="#E2D9D2")
    
    # Divider line
    draw.line([(110, 620), (W - 110, 620)], fill="#524438", width=2)
    
    # Brand Footer Info
    draw.text((110, 660), "《江夏傳統整復推拿 板橋館》", font=font_sub, fill="#FFFFFF")
    draw.text((110, 720), "源自武術內勁鬆拿 ‧ 一對一客製調理 ‧ 預約制", font=font_tag, fill="#B8A89C")
    
    # Big CTA Button at Bottom
    cta_box = [110, 830, W - 110, 940]
    draw.rounded_rectangle(cta_box, radius=24, fill=ad["cta_bg"])
    
    # Center CTA text
    bbox = font_cta.getbbox(ad["cta"])
    tw = bbox[2] - bbox[0]
    tx = 110 + ((W - 220) - tw) // 2
    draw.text((tx, 860), ad["cta"], font=font_cta, fill="#FFFFFF")
    
    # Save Image
    path = os.path.join(out_dir, ad["filename"])
    img.save(path, quality=95)
    print(f"✅ Generated Meta Ad Creative: {path}")

print("🎉 All 3 Meta Ad Creatives Generated Successfully!")
