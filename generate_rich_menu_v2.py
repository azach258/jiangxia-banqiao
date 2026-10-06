import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Canvas setup - Standard LINE Rich Menu Size
WIDTH, HEIGHT = 2500, 1686

# Fonts
FONT_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msjh.ttc"

font_main_primary = ImageFont.truetype(FONT_BOLD, 105)
font_sub_primary = ImageFont.truetype(FONT_BOLD, 52)

font_main_card = ImageFont.truetype(FONT_BOLD, 95)
font_sub_card = ImageFont.truetype(FONT_REG, 46)

# Create base canvas with deep luxury dark emerald-slate background
img = Image.new("RGB", (WIDTH, HEIGHT), color="#0E1A14")
draw = ImageDraw.Draw(img)

# Layout: 2 rows x 2 cols (4 large cards)
cols, rows = 2, 2
cell_w = WIDTH // cols
cell_h = HEIGHT // rows
gap = 24  # gap between cards

# Define 4 core intuitive needs (直覺需求)
cards = [
    {
        "col": 0, "row": 0,
        "title": "📅 線上立即預約",
        "sub": "即刻挑選專屬調理時段 ➔",
        "bg_color": "#06C755",         # LINE official brand green
        "bg_gradient_to": "#028A3B",
        "text_color": "#FFFFFF",
        "sub_color": "#E6FFFA",
        "border_color": "#10B981",
        "is_primary": True
    },
    {
        "col": 1, "row": 0,
        "title": "👨‍⚕️ 武術內勁鬆拿",
        "sub": "賴師傅親自調理 ‧ 溫和不痛放鬆 ›",
        "bg_color": "#182E23",         # Deep luxury dark emerald card
        "bg_gradient_to": "#11221A",
        "text_color": "#F3E8C9",        # Elegant champange gold
        "sub_color": "#D1C2A5",
        "border_color": "#D4AF37",      # Gold border
        "is_primary": False
    },
    {
        "col": 0, "row": 1,
        "title": "📍 到館交通導航",
        "sub": "館前西路152-1號 ‧ 地圖導航 ›",
        "bg_color": "#182E23",
        "bg_gradient_to": "#11221A",
        "text_color": "#FFFFFF",
        "sub_color": "#A3B8AC",
        "border_color": "#2A4737",
        "is_primary": False
    },
    {
        "col": 1, "row": 1,
        "title": "⭐ 顧客真實好評",
        "sub": "Google 5星在地推薦 ‧ 放心體驗 ›",
        "bg_color": "#182E23",
        "bg_gradient_to": "#11221A",
        "text_color": "#FFFFFF",
        "sub_color": "#A3B8AC",
        "border_color": "#2A4737",
        "is_primary": False
    }
]

def draw_gradient_card(draw_obj, rect, c1_hex, c2_hex, radius, border_hex):
    x1, y1, x2, y2 = rect
    w, h = x2 - x1, y2 - y1
    
    # Create card layer
    card_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_img)
    
    # Vertical gradient
    r1, g1, b1 = int(c1_hex[1:3], 16), int(c1_hex[3:5], 16), int(c1_hex[5:7], 16)
    r2, g2, b2 = int(c2_hex[1:3], 16), int(c2_hex[3:5], 16), int(c2_hex[5:7], 16)
    
    for y in range(h):
        ratio = y / float(h)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        cdraw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # Mask rounded corner
    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    
    # Apply mask
    card_img.putalpha(mask)
    img.paste(card_img, (x1, y1), card_img)
    
    # Draw stroke
    draw_obj.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=border_hex, width=6)

for c in cards:
    x1 = c["col"] * cell_w + gap
    y1 = c["row"] * cell_h + gap
    x2 = (c["col"] + 1) * cell_w - gap
    y2 = (c["row"] + 1) * cell_h - gap
    
    draw_gradient_card(draw, [x1, y1, x2, y2], c["bg_color"], c["bg_gradient_to"], radius=40, border_hex=c["border_color"])
    
    # Large Full-card Text (滿版大字)
    if c["is_primary"]:
        # Primary CTA - Large Bold Crisp White Text
        title_font = font_main_primary
        sub_font = font_sub_primary
        title_y = y1 + 260
        sub_y = y1 + 440
    else:
        title_font = font_main_card
        sub_font = font_sub_card
        title_y = y1 + 270
        sub_y = y1 + 440
        
    # Draw Title
    draw.text((x1 + 90, title_y), c["title"], font=title_font, fill=c["text_color"])
    # Draw Subtitle
    draw.text((x1 + 95, sub_y), c["sub"], font=sub_font, fill=c["sub_color"])

# Save
out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館"
out_path = os.path.join(out_dir, "LINE_Rich_Menu_2500x1686_v2.png")
img.save(out_path, quality=98)
print(f"✅ Successfully generated LINE Rich Menu v2 image at: {out_path}")
