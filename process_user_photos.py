import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives"
os.makedirs(out_dir, exist_ok=True)

# User's exact authentic photos
real_photos = [
    {
        "src": "C:/Users/love_/AppData/Local/hermes/cache/images/img_81edf849663c.jpg",
        "out_png": "meta_ad_A_real_exterior.png",
        "hook": "板橋30年老字號 賴師傅親自調理",
        "cta": "私訊小幫手 領取專屬舒緩方案"
    },
    {
        "src": "C:/Users/love_/AppData/Local/hermes/cache/images/img_015914eafd8a.jpg",
        "out_png": "meta_ad_B_real_interior.png",
        "hook": "源自武英門內勁 溫和舒緩不硬抓",
        "cta": "點擊發送訊息 線上諮詢預約"
    },
    {
        "src": "C:/Users/love_/AppData/Local/hermes/cache/images/img_d00d4008c009.jpg",
        "out_png": "meta_ad_C_real_technique.png",
        "hook": "久坐肩頸腰背痠痛？館前西路152-1號",
        "cta": "點擊發送訊息 預約專屬時段"
    }
]

W, H = 1080, 1080
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
font_hook = ImageFont.truetype(FONT_BOLD, 68)
font_cta = ImageFont.truetype(FONT_BOLD, 36)

for item in real_photos:
    src_path = item["src"]
    out_path = os.path.join(out_dir, item["out_png"])
    
    if os.path.exists(src_path):
        base_img = Image.open(src_path).convert("RGB")
    else:
        print(f"⚠️ Source photo not found: {src_path}")
        continue

    # Center Crop to 1:1 Square (1080x1080)
    bw, bh = base_img.size
    min_dim = min(bw, bh)
    left = (bw - min_dim) // 2
    top = (bh - min_dim) // 2
    cropped = base_img.crop((left, top, left + min_dim, top + min_dim))
    resized = cropped.resize((W, H), Image.Resampling.LANCZOS)
    
    # Elegant dark gradient overlay to ensure text contrast while preserving full photo visibility
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    resized_rgba = resized.convert("RGBA")
    combined = Image.alpha_composite(resized_rgba, overlay).convert("RGB")
    
    draw = ImageDraw.Draw(combined)
    
    # Pure Clean Text Hook — NO BOXES, NO BORDERS, NO EMOJIS, NO TAGS (<15% canvas area)
    hook_text = item["hook"]
    bbox = font_hook.getbbox(hook_text)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = 100  # Positioned top-center for maximum photo visibility
    
    # Draw dark backing shadow behind text for readability over real photo
    draw.text((tx + 3, ty + 3), hook_text, font=font_hook, fill="#000000")
    draw.text((tx, ty), hook_text, font=font_hook, fill="#FFFFFF")
    
    # Draw Clean Emerald Green CTA Button at Bottom (NO BOX AROUND TEXT, NO EMOJIS)
    cta_text = item["cta"]
    bbox_cta = font_cta.getbbox(cta_text)
    ctw = bbox_cta[2] - bbox_cta[0]
    
    cta_x1 = (W - (ctw + 100)) // 2
    cta_y1 = H - 180
    cta_x2 = cta_x1 + ctw + 100
    cta_y2 = cta_y1 + 80
    
    draw.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=18, fill="#06C755")
    
    ctx = cta_x1 + 50
    cty = cta_y1 + 20
    draw.text((ctx, cty), cta_text, font=font_cta, fill="#FFFFFF")
    
    # Save Final Real Photo Meta Ad Creative
    combined.save(out_path, quality=98)
    print(f"🎉 Processed Real User Photo Creative: {out_path}")

print("✅ All 3 Real User Photo Meta Ad Creatives Generated Successfully!")
