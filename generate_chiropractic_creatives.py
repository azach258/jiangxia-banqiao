import urllib.request
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/meta_ads_creatives"
os.makedirs(out_dir, exist_ok=True)

# High Quality Authentic Asian Chiropractic & Bodywork Stock Photos
# Explicitly selected for clean treatment tables, comfortable clothes, joint/back/shoulder relaxation (NO SPA/NO OIL/NO CANDLES)
photo_sources = [
    {
        "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=1200&q=80", # Athletic joint & muscle stretch on treatment table
        "filename": "chiropractic_photo_A.jpg",
        "out_png": "meta_ad_A_chiropractic.png",
        "hook": "肩頸沉重像頂著磚頭？",
        "sub": "江夏武術內勁鬆拿 ‧ 板橋館前西路152-1號",
        "cta": "私訊小幫手 預約專屬舒緩"
    },
    {
        "url": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?w=1200&q=80", # Clean wooden wellness treatment bed room
        "filename": "chiropractic_photo_B.jpg",
        "out_png": "meta_ad_B_chiropractic.png",
        "hook": "整復一定要痛到流眼淚？",
        "sub": "溫和放鬆不硬抓 ‧ 賴師傅親自調理",
        "cta": "私訊諮詢 溫和深層放鬆"
    },
    {
        "url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=1200&q=80", # Posture alignment & athletic bodywork
        "filename": "chiropractic_photo_C.jpg",
        "out_png": "meta_ad_C_chiropractic.png",
        "hook": "板橋上班族私藏 筋骨保養",
        "sub": "久坐習慣翹腳 ‧ 體態結構平衡",
        "cta": "點擊發送訊息 了解詳情"
    }
]

headers = {'User-Agent': 'Mozilla/5.0'}

W, H = 1080, 1080
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
font_hook = ImageFont.truetype(FONT_BOLD, 72)
font_sub = ImageFont.truetype(FONT_BOLD, 36)
font_cta = ImageFont.truetype(FONT_BOLD, 38)

for item in photo_sources:
    jpg_path = os.path.join(out_dir, item["filename"])
    
    # Download photo
    try:
        req = urllib.request.Request(item["url"], headers=headers)
        with urllib.request.urlopen(req) as response, open(jpg_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"✅ Downloaded chiropractic photo: {item['filename']}")
    except Exception as e:
        print(f"⚠️ Download failed for {item['filename']}: {e}")
        
    if os.path.exists(jpg_path):
        base_img = Image.open(jpg_path).convert("RGB")
    else:
        base_img = Image.new("RGB", (W, H), color="#1C241E")

    # Crop 1:1
    bw, bh = base_img.size
    min_dim = min(bw, bh)
    left = (bw - min_dim) // 2
    top = (bh - min_dim) // 2
    cropped = base_img.crop((left, top, left + min_dim, top + min_dim))
    resized = cropped.resize((W, H), Image.Resampling.LANCZOS)
    
    # Subtle dark gradient overlay to ensure text contrast while showing the treatment bed & posture work
    overlay = Image.new("RGBA", (W, H), (14, 26, 20, 150))
    resized_rgba = resized.convert("RGBA")
    combined = Image.alpha_composite(resized_rgba, overlay).convert("RGB")
    
    draw = ImageDraw.Draw(combined)
    
    # PURE TEXT OVERLAY — ZERO BOXES, ZERO EMOJIS, ZERO TAGS
    hook_text = item["hook"]
    bbox = font_hook.getbbox(hook_text)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = H // 2 - 100
    
    # Draw Hook Text directly over chiropractic background with soft shadow
    draw.text((tx + 3, ty + 3), hook_text, font=font_hook, fill="#000000")
    draw.text((tx, ty), hook_text, font=font_hook, fill="#FFFFFF")
    
    # Draw Subtitle
    sub_text = item["sub"]
    bbox_sub = font_sub.getbbox(sub_text)
    stw = bbox_sub[2] - bbox_sub[0]
    stx = (W - stw) // 2
    sty = ty + 95
    draw.text((stx, sty), sub_text, font=font_sub, fill="#F3E8C9")
    
    # Draw Clean CTA Button at Bottom (LINE/Meta Emerald Green, NO BOX AROUND TEXT, NO EMOJIS)
    cta_text = item["cta"]
    bbox_cta = font_cta.getbbox(cta_text)
    ctw = bbox_cta[2] - bbox_cta[0]
    
    cta_x1 = (W - (ctw + 100)) // 2
    cta_y1 = H - 180
    cta_x2 = cta_x1 + ctw + 100
    cta_y2 = cta_y1 + 80
    
    draw.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=16, fill="#06C755")
    
    ctx = cta_x1 + 50
    cty = cta_y1 + 20
    draw.text((ctx, cty), cta_text, font=font_cta, fill="#FFFFFF")
    
    # Save
    out_png_path = os.path.join(out_dir, item["out_png"])
    combined.save(out_png_path, quality=95)
    print(f"🎉 Generated Chiropractic Meta Ad Creative: {out_png_path}")

print("✅ All Chiropractic Meta Ad Creatives Ready!")
