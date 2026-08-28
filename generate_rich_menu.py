import os
from PIL import Image, ImageDraw, ImageFont

# Canvas setup
WIDTH, HEIGHT = 2500, 1686
img = Image.new("RGB", (WIDTH, HEIGHT), color="#F7F5F0")  # Warm elegant cream background
draw = ImageDraw.Draw(img)

# Colors
FONT_PATH_BOLD = "C:/Windows/Fonts/msjhbd.ttc"
FONT_PATH_REG = "C:/Windows/Fonts/msjh.ttc"

COLOR_BG_PRIMARY = "#8C6A43"    # Warm teak/golden wood tone for primary CTA
COLOR_BG_SECONDARY = "#FFFFFF"  # Pure crisp white for standard cards
COLOR_BORDER = "#E0D8CB"        # Delicate border line
COLOR_TEXT_MAIN = "#2C2621"     # Dark charcoal
COLOR_TEXT_MUTED = "#6E655F"    # Muted taupe
COLOR_TEXT_GOLD = "#D4A359"     # Accent gold
COLOR_TEXT_WHITE = "#FFFFFF"    # White for primary card

# Fonts
font_title_lg = ImageFont.truetype(FONT_PATH_BOLD, 76)
font_title_md = ImageFont.truetype(FONT_PATH_BOLD, 68)
font_sub = ImageFont.truetype(FONT_PATH_REG, 42)
font_badge = ImageFont.truetype(FONT_PATH_BOLD, 36)

# Grid Layout: 2 rows x 3 columns
cols, rows = 3, 2
cell_w = WIDTH // cols
cell_h = HEIGHT // rows
gap = 12  # gap between cards

# Define grid items
items = [
    {
        "col": 0, "row": 0,
        "badge": "⚡ 熱門推薦",
        "icon": "📅",
        "title": "線上立即預約",
        "sub": "24h 輕鬆預約專屬時段",
        "is_primary": True
    },
    {
        "col": 1, "row": 0,
        "badge": "明碼標價",
        "icon": "💰",
        "title": "服務項目與價目",
        "sub": "價目透明 / 局部與全身保養",
        "is_primary": False
    },
    {
        "col": 2, "row": 0,
        "badge": "武術內勁",
        "icon": "👨‍⚕️",
        "title": "賴師傅與特色",
        "sub": "專業細心 / 溫和不暴力",
        "is_primary": False
    },
    {
        "col": 0, "row": 1,
        "badge": "國光路",
        "icon": "📍",
        "title": "到館交通與地圖",
        "sub": "捷運公車路線 / 停車資訊",
        "is_primary": False
    },
    {
        "col": 1, "row": 1,
        "badge": "5★口碑",
        "icon": "⭐",
        "title": "顧客真實好評",
        "sub": "Google 商家滿意回饋",
        "is_primary": False
    },
    {
        "col": 2, "row": 1,
        "badge": "專人服務",
        "icon": "💬",
        "title": "專人一對一諮詢",
        "sub": "即時解答您的調理疑問",
        "is_primary": False
    }
]

# Draw cards
for item in items:
    x1 = item["col"] * cell_w + gap
    y1 = item["row"] * cell_h + gap
    x2 = (item["col"] + 1) * cell_w - gap
    y2 = (item["row"] + 1) * cell_h - gap

    # Corner radius simulated by rounded rectangle
    radius = 32
    
    if item["is_primary"]:
        # Primary card styling (Warm teak/gold)
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=COLOR_BG_PRIMARY)
        
        # Draw Badge
        badge_box = [x1 + 60, y1 + 50, x1 + 260, y1 + 105]
        draw.rounded_rectangle(badge_box, radius=18, fill="#A68053")
        draw.text((x1 + 80, y1 + 58), item["badge"], font=font_badge, fill=COLOR_TEXT_WHITE)
        
        # Icon + Title
        draw.text((x1 + 60, y1 + 140), f"{item['icon']} {item['title']}", font=font_title_lg, fill=COLOR_TEXT_WHITE)
        draw.text((x1 + 60, y1 + 250), item["sub"], font=font_sub, fill="#E6DAC8")
        
        # Decorative Arrow
        draw.text((x2 - 120, y2 - 140), "➔", font=font_title_lg, fill=COLOR_TEXT_WHITE)

    else:
        # Standard card styling
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=COLOR_BG_SECONDARY, outline=COLOR_BORDER, width=4)
        
        # Draw Badge
        badge_box = [x1 + 60, y1 + 50, x1 + 260, y1 + 105]
        draw.rounded_rectangle(badge_box, radius=18, fill="#F2ECE4")
        draw.text((x1 + 80, y1 + 58), item["badge"], font=font_badge, fill="#8C6A43")
        
        # Icon + Title
        draw.text((x1 + 60, y1 + 140), f"{item['icon']} {item['title']}", font=font_title_md, fill=COLOR_TEXT_MAIN)
        draw.text((x1 + 60, y1 + 250), item["sub"], font=font_sub, fill=COLOR_TEXT_MUTED)

        # Decorative subtle arrow
        draw.text((x2 - 120, y2 - 140), "›", font=font_title_lg, fill="#C0B4A5")

# Outer border accent
draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline="#D4A359", width=8)

# Save
out_dir = "C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館"
out_path = os.path.join(out_dir, "LINE_Rich_Menu_2500x1686.png")
img.save(out_path, quality=95)
print(f"✅ Successfully generated LINE Rich Menu image at: {out_path}")
