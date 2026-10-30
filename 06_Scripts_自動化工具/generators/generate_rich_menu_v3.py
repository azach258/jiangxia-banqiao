import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Canvas setup - Standard LINE Rich Menu Size
WIDTH, HEIGHT = 2500, 1686

# Fonts
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msjh.ttc"

# Very Large Bold Centered Title (Max 6 Chars)
font_title = ImageFont.truetype(FONT_BOLD, 115)
font_sub = ImageFont.truetype(FONT_REG, 44)

# Create high-end comfortable therapy clinic environment base
# Synthesize a warm, clean, wood-and-warm-light clinic background
bg_img = Image.new("RGB", (WIDTH, HEIGHT), color="#211A15")
bg_draw = ImageDraw.Draw(bg_img)

# Warm lighting atmosphere gradient
for y in range(HEIGHT):
    ratio = y / float(HEIGHT)
    r = int(38 + (18 - 38) * ratio)
    g = int(28 + (14 - 28) * ratio)
    b = int(22 + (10 - 22) * ratio)
    bg_draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add soft ambient light texture simulating warm wooden massage room
for i in range(0, WIDTH, 80):
    bg_draw.line([(i, 0), (i + 300, HEIGHT)], fill=(45, 34, 26), width=40)

bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))

# Create drawing object
draw = ImageDraw.Draw(bg_img)

# 2 rows x 2 cols layout
cols, rows = 2, 2
cell_w = WIDTH // cols
cell_h = HEIGHT // rows
gap = 28

# 4 Core Cards - Max 6 Chars per Title, NO icons/emojis, Centered, Huge Font
cards = [
    {
        "col": 0, "row": 0,
        "title": "線上立即預約",      # 6 chars
        "sub": "24小時輕鬆挑選專屬時段",
        "bg_c1": "#06C755",         # LINE official brand green
        "bg_c2": "#03923E",
        "border": "#34D399",
        "text_color": "#FFFFFF",
        "sub_color": "#E6FFFA",
        "is_primary": True
    },
    {
        "col": 1, "row": 0,
        "title": "武術內勁鬆拿",      # 6 chars
        "sub": "賴師傅親自調理 ‧ 溫和不痛",
        "bg_c1": "#2A211B",         # Deep warm dark teak
        "bg_c2": "#1A1410",
        "border": "#D4AF37",         # Elegant Gold Accent
        "text_color": "#F3E8C9",
        "sub_color": "#D1C2A5",
        "is_primary": False
    },
    {
        "col": 0, "row": 1,
        "title": "到館交通導航",      # 6 chars
        "sub": "館前西路152-1號 ‧ 捷運府中站",
        "bg_c1": "#211A15",
        "bg_c2": "#14100D",
        "border": "#4A3B30",
        "text_color": "#FFFFFF",
        "sub_color": "#B8A89C",
        "is_primary": False
    },
    {
        "col": 1, "row": 1,
        "title": "顧客真實好評",      # 6 chars
        "sub": "Google 5星在地推薦 ‧ 放心體驗",
        "bg_c1": "#211A15",
        "bg_c2": "#14100D",
        "border": "#4A3B30",
        "text_color": "#FFFFFF",
        "sub_color": "#B8A89C",
        "is_primary": False
    }
]

def draw_centered_card(draw_obj, rect, c1_hex, c2_hex, radius, border_hex, card_data):
    x1, y1, x2, y2 = rect
    w, h = x2 - x1, y2 - y1
    
    # Card image with gradient
    card_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_img)
    
    r1, g1, b1 = int(c1_hex[1:3], 16), int(c1_hex[3:5], 16), int(c1_hex[5:7], 16)
    r2, g2, b2 = int(c2_hex[1:3], 16), int(c2_hex[3:5], 16), int(c2_hex[5:7], 16)
    
    for y in range(h):
        ratio = y / float(h)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        cdraw.line([(0, y), (w, y)], fill=(r, g, b, 230 if not card_data["is_primary"] else 245))
        
    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    
    card_img.putalpha(mask)
    bg_img.paste(card_img, (x1, y1), card_img)
    
    # Draw subtle rounded border
    draw_obj.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=border_hex, width=5)
    
    # Calculate Centered Text Positioning
    title_text = card_data["title"]
    sub_text = card_data["sub"]
    
    # Measure Title Width
    bbox_title = font_title.getbbox(title_text)
    tw = bbox_title[2] - bbox_title[0]
    tx = x1 + (w - tw) // 2
    ty = y1 + (h // 2) - 80
    
    # Measure Subtitle Width
    bbox_sub = font_sub.getbbox(sub_text)
    sw = bbox_sub[2] - bbox_sub[0]
    sx = x1 + (w - sw) // 2
    sy = y1 + (h // 2) + 55
    
    # Draw Centered Main Title (MAX 6 CHARS, BOLD, NO ICONS)
    draw_obj.text((tx, ty), title_text, font=font_title, fill=card_data["text_color"])
    
    # Draw Centered Subtitle
    draw_obj.text((sx, sy), sub_text, font=font_sub, fill=card_data["sub_color"])

for c in cards:
    x1 = c["col"] * cell_w + gap
    y1 = c["row"] * cell_h + gap
    x2 = (c["col"] + 1) * cell_w - gap
    y2 = (c["row"] + 1) * cell_h - gap
    
    draw_centered_card(draw, [x1, y1, x2, y2], c["bg_c1"], c["bg_c2"], radius=36, border_hex=c["border"], card_data=c)

# Save
out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館"
out_path = os.path.join(out_dir, "LINE_Rich_Menu_2500x1686_v3.png")
bg_img.save(out_path, quality=98)
print(f"✅ Successfully generated LINE Rich Menu v3 image at: {out_path}")
