import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives/matrix_6"
os.makedirs(out_dir, exist_ok=True)

# User's authentic real photos
photo_exterior = "C:/Users/love_/AppData/Local/hermes/cache/images/img_81edf849663c.jpg"
photo_interior = "C:/Users/love_/AppData/Local/hermes/cache/images/img_015914eafd8a.jpg"
photo_technique = "C:/Users/love_/AppData/Local/hermes/cache/images/img_d00d4008c009.jpg"

W, H = 1080, 1080
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msjh.ttc"

font_title = ImageFont.truetype(FONT_BOLD, 68)
font_sub = ImageFont.truetype(FONT_BOLD, 34)
font_cta = ImageFont.truetype(FONT_BOLD, 38)

# 6 Emotion Matrix Concepts
matrix_concepts = [
    {
        "id": "1_authority",
        "name": "1. 權威信任流 (Authority)",
        "photo": photo_exterior,
        "title": "板橋30年老字號 賴師傅親自調理",
        "sub": "超越45家海內外媒體報導 ‧ 預約制免等待",
        "cta": "私訊小幫手 領取專屬舒緩方案",
        "out_file": "01_authority_30years.png"
    },
    {
        "id": "2_curiosity",
        "name": "2. 迷思破解流 (Curiosity)",
        "photo": photo_interior,
        "title": "整復一定要痛到流眼淚嗎？",
        "sub": "源自武英門內勁 ‧ 溫和舒緩不硬抓",
        "cta": "點擊發送訊息 線上諮詢預約",
        "out_file": "02_curiosity_gentle.png"
    },
    {
        "id": "3_painpoint",
        "name": "3. 痛點共鳴流 (Pain Points)",
        "photo": photo_technique,
        "title": "下班後肩頸像頂著兩塊磚頭？",
        "sub": "武術內勁鬆拿 ‧ 館前西路152-1號",
        "cta": "點擊發送訊息 預約專屬時段",
        "out_file": "03_painpoint_office.png"
    },
    {
        "id": "4_offer",
        "name": "4. 好康誘因流 (Value Offer)",
        "photo": photo_exterior,
        "title": "路過免費15分鐘鬆筋體驗",
        "sub": "親身體驗武術內勁 ‧ 舒緩久坐痠痛",
        "cta": "私訊小幫手 詢問免費體驗",
        "out_file": "04_value_offer_free15m.png"
    },
    {
        "id": "5_socialproof",
        "name": "5. 現場實景流 (Social Proof)",
        "photo": photo_interior,
        "title": "館前西路152-1號 溫馨門市實景",
        "sub": "明亮乾淨整復室 ‧ 專屬一對一調理",
        "cta": "私訊小幫手 查看預約時段",
        "out_file": "05_social_proof_clinic.png"
    },
    {
        "id": "6_transformation",
        "name": "6. 體態改變流 (Transformation)",
        "photo": photo_technique,
        "title": "習慣翹腳？上班族體態保養",
        "sub": "客製化結構放鬆 ‧ 恢復輕盈活力",
        "cta": "點擊發送訊息 了解體態調理",
        "out_file": "06_transformation_posture.png"
    }
]

for item in matrix_concepts:
    src_path = item["photo"]
    out_path = os.path.join(out_dir, item["out_file"])
    
    if os.path.exists(src_path):
        base_img = Image.open(src_path).convert("RGB")
    else:
        print(f"⚠️ Photo not found: {src_path}")
        continue

    # Crop to 1:1 Square (1080x1080)
    bw, bh = base_img.size
    min_dim = min(bw, bh)
    left = (bw - min_dim) // 2
    top = (bh - min_dim) // 2
    cropped = base_img.crop((left, top, left + min_dim, top + min_dim))
    resized = cropped.resize((W, H), Image.Resampling.LANCZOS)
    
    # Soft translucent dark overlay for high contrast and legibility over real photo
    overlay = Image.new("RGBA", (W, H), (10, 14, 12, 130))
    resized_rgba = resized.convert("RGBA")
    combined = Image.alpha_composite(resized_rgba, overlay).convert("RGB")
    
    draw = ImageDraw.Draw(combined)
    
    # Render Title - NO BOXES, NO TAGS, NO EMOJIS!
    title_text = item["title"]
    bbox_t = font_title.getbbox(title_text)
    tw = bbox_t[2] - bbox_t[0]
    tx = (W - tw) // 2
    ty = 110  # Top area for maximum photo visibility
    
    # Soft text shadow
    draw.text((tx + 3, ty + 3), title_text, font=font_title, fill="#000000")
    draw.text((tx, ty), title_text, font=font_title, fill="#FFFFFF")
    
    # Render Subtitle
    sub_text = item["sub"]
    bbox_s = font_sub.getbbox(sub_text)
    sw = bbox_s[2] - bbox_s[0]
    sx = (W - sw) // 2
    sy = ty + 95
    
    draw.text((sx + 2, sy + 2), sub_text, font=font_sub, fill="#000000")
    draw.text((sx, sy), sub_text, font=font_sub, fill="#F3E8C9") # Warm Gold Subtitle
    
    # Render Bottom CTA Button
    cta_text = item["cta"]
    bbox_c = font_cta.getbbox(cta_text)
    cw = bbox_c[2] - bbox_c[0]
    
    btn_w = cw + 90
    btn_h = 80
    btn_x = (W - btn_w) // 2
    btn_y = H - 170
    
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=18, fill="#06C755")
    
    ctx = btn_x + (btn_w - cw) // 2
    cty = btn_y + 20
    draw.text((ctx, cty), cta_text, font=font_cta, fill="#FFFFFF")
    
    combined.save(out_path, quality=98)
    print(f"✅ Rendered Matrix Ad Creative [{item['id']}]: {out_path}")

print("🎉 All 6 Emotion Matrix Creatives Rendered Successfully!")
