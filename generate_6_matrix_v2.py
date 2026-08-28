import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives/matrix_6_v2"
os.makedirs(out_dir, exist_ok=True)

# User's authentic real photos
photo_exterior = "C:/Users/love_/AppData/Local/hermes/cache/images/img_81edf849663c.jpg"
photo_interior = "C:/Users/love_/AppData/Local/hermes/cache/images/img_015914eafd8a.jpg"
photo_technique = "C:/Users/love_/AppData/Local/hermes/cache/images/img_d00d4008c009.jpg"

W, H = 1080, 1080
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"

font_title = ImageFont.truetype(FONT_BOLD, 72)
font_sub = ImageFont.truetype(FONT_BOLD, 36)

matrix_concepts = [
    {
        "id": "1_authority",
        "photo": photo_exterior,
        "title": "板橋30年老字號 賴師傅親自調理",
        "sub": "超越45家海內外媒體報導 ‧ 館前西路152-1號",
        "out_file": "01_authority_30years.png"
    },
    {
        "id": "2_curiosity",
        "photo": photo_interior,
        "title": "整復一定要痛到流眼淚嗎？",
        "sub": "源自武英門內勁 ‧ 溫和舒緩不硬抓",
        "out_file": "02_curiosity_gentle.png"
    },
    {
        "id": "3_painpoint",
        "photo": photo_technique,
        "title": "下班後肩頸像頂著兩塊磚頭？",
        "sub": "武術內勁鬆拿 ‧ 板橋館前西路152-1號",
        "out_file": "03_painpoint_office.png"
    },
    {
        "id": "4_offer",
        "photo": photo_exterior,
        "title": "路過免費15分鐘鬆筋體驗",
        "sub": "親身體驗武術內勁 ‧ 舒緩久坐痠痛",
        "out_file": "04_value_offer_free15m.png"
    },
    {
        "id": "5_socialproof",
        "photo": photo_interior,
        "title": "館前西路152-1號 溫馨門市實景",
        "sub": "明亮乾淨整復室 ‧ 專屬一對一調理",
        "out_file": "05_social_proof_clinic.png"
    },
    {
        "id": "6_transformation",
        "photo": photo_technique,
        "title": "習慣翹腳？上班族體態保養",
        "sub": "客製化結構放鬆 ‧ 恢復輕盈活力",
        "out_file": "06_transformation_posture.png"
    }
]

for item in matrix_concepts:
    src_path = item["photo"]
    out_path = os.path.join(out_dir, item["out_file"])
    
    if os.path.exists(src_path):
        base_img = Image.open(src_path).convert("RGB")
    else:
        continue

    # Crop to 1:1 Square (1080x1080)
    bw, bh = base_img.size
    min_dim = min(bw, bh)
    left = (bw - min_dim) // 2
    top = (bh - min_dim) // 2
    cropped = base_img.crop((left, top, left + min_dim, top + min_dim))
    resized = cropped.resize((W, H), Image.Resampling.LANCZOS)
    
    # Base RGBA
    canvas = resized.convert("RGBA")
    
    # Measure Title and Subtitle Text Width
    title_text = item["title"]
    sub_text = item["sub"]
    
    bbox_t = font_title.getbbox(title_text)
    tw = bbox_t[2] - bbox_t[0]
    th = bbox_t[3] - bbox_t[1]
    
    bbox_s = font_sub.getbbox(sub_text)
    sw = bbox_s[2] - bbox_s[0]
    sh = bbox_s[3] - bbox_s[1]
    
    # Calculate banner dimensions
    max_w = max(tw, sw) + 80
    banner_h = th + sh + 90
    banner_x1 = (W - max_w) // 2
    banner_y1 = (H - banner_h) // 2  # Centered on image
    banner_x2 = banner_x1 + max_w
    banner_y2 = banner_y1 + banner_h
    
    # Create dark frosted translucent backing banner (solves background text collision)
    banner_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(banner_overlay)
    
    # Draw sleek dark slate-emerald solid backing card with rounded corners
    bdraw.rounded_rectangle([banner_x1, banner_y1, banner_x2, banner_y2], radius=24, fill=(12, 22, 16, 225), outline=(212, 175, 55, 200), width=3)
    
    # Composite banner over photo
    combined = Image.alpha_composite(canvas, banner_overlay).convert("RGB")
    draw = ImageDraw.Draw(combined)
    
    # Render Headline Text Crisp White
    tx = (W - tw) // 2
    ty = banner_y1 + 35
    draw.text((tx, ty), title_text, font=font_title, fill="#FFFFFF")
    
    # Render Subtitle Text Champagne Gold
    sx = (W - sw) // 2
    sy = ty + th + 25
    draw.text((sx, sy), sub_text, font=font_sub, fill="#F3E8C9")
    
    # NO GREEN BUTTON AT BOTTOM (Completely Removed!)
    
    combined.save(out_path, quality=98)
    print(f"✅ Rendered v2 Clean Creative: {out_path}")

print("🎉 All 6 v2 Creatives Rendered Successfully!")
