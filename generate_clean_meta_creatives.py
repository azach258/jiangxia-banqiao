import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives"
os.makedirs(out_dir, exist_ok=True)

W, H = 1080, 1080

FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
font_hook = ImageFont.truetype(FONT_BOLD, 72)
font_cta = ImageFont.truetype(FONT_BOLD, 36)

# Ultra-clean 20% text compliant creatives (< 15% text area)
ad_concepts_clean = [
    {
        "filename": "meta_ad_A_clean.png",
        "hook": "肩頸沉重像頂著磚頭？",
        "cta": "💬 私訊小幫手 ‧ 預約專屬舒緩",
        "bg_c1": "#1E1712",
        "bg_c2": "#2C2018",
        "accent": "#D4AF37",
        "cta_bg": "#06C755"
    },
    {
        "filename": "meta_ad_B_clean.png",
        "hook": "整復一定要痛到流眼淚？",
        "cta": "💬 私訊諮詢 ‧ 溫和不硬抓",
        "bg_c1": "#12211A",
        "bg_c2": "#1C3328",
        "accent": "#10B981",
        "cta_bg": "#06C755"
    },
    {
        "filename": "meta_ad_C_clean.png",
        "hook": "板橋人私藏 筋骨保養",
        "cta": "💬 點擊發送訊息 ‧ 了解詳情",
        "bg_c1": "#181822",
        "bg_c2": "#242436",
        "accent": "#818CF8",
        "cta_bg": "#06C755"
    }
]

for ad in ad_concepts_clean:
    # 80%+ Clean Ambient Wood/Clinic Atmosphere
    img = Image.new("RGB", (W, H), color=ad["bg_c1"])
    draw = ImageDraw.Draw(img)
    
    r1, g1, b1 = int(ad["bg_c1"][1:3], 16), int(ad["bg_c1"][3:5], 16), int(ad["bg_c1"][5:7], 16)
    r2, g2, b2 = int(ad["bg_c2"][1:3], 16), int(ad["bg_c2"][3:5], 16), int(ad["bg_c2"][5:7], 16)
    for y in range(H):
        ratio = y / float(H)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Ambient texture
    for i in range(0, W, 100):
        draw.line([(i, 0), (i + 200, H)], fill=(255, 255, 255, 5), width=20)
        
    # Single Punchy Center Hook (< 15% Canvas Area)
    hook_text = ad["hook"]
    bbox = font_hook.getbbox(hook_text)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = H // 2 - 80
    
    # Draw dark backing card behind hook for contrast
    draw.rounded_rectangle([tx - 40, ty - 30, tx + tw + 40, ty + 100], radius=24, fill="#0D0A08", outline=ad["accent"], width=3)
    draw.text((tx, ty), hook_text, font=font_hook, fill="#FFFFFF")
    
    # Clean CTA Button at bottom
    cta_box = [150, H - 200, W - 150, H - 110]
    draw.rounded_rectangle(cta_box, radius=20, fill=ad["cta_bg"])
    
    bbox_cta = font_cta.getbbox(ad["cta"])
    ctw = bbox_cta[2] - bbox_cta[0]
    ctx = (W - ctw) // 2
    draw.text((ctx, H - 178), ad["cta"], font=font_cta, fill="#FFFFFF")
    
    # Save Image
    path = os.path.join(out_dir, ad["filename"])
    img.save(path, quality=95)
    print(f"✅ Generated Ultra-Clean Meta Ad Creative: {path}")

print("🎉 Ultra-Clean Meta Ad Creatives Generated!")
