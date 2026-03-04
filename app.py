from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# ==============================
# RULE CỨNG
# ==============================

RULES = [

# socola
(r"thanh.*socola|socola.*thanh|chocolate bar",
 ("Thực phẩm khô","Đồ ăn vặt","Thanh socola")),

(r"socola",
 ("Thực phẩm khô","Đồ ăn vặt","Kẹo socola các loại")),

# bột
(r"bột chiên giòn",
 ("Thực phẩm khô","Lương thực khô","Bột mì & bột gạo các loại")),

# bánh
(r"bánh que",
 ("Thực phẩm khô","Đồ ăn vặt","Bánh quy")),

(r"wafer|bánh quế",
 ("Thực phẩm khô","Đồ ăn vặt","Bánh xốp")),

# khô gà
(r"khô gà",
 ("Thực phẩm khô","Đồ ăn vặt","Thịt bò khô")),

# nước mắm
(r"nước mắm",
 ("Thực phẩm khô","Phụ liệu cho món mặn","Nước xốt Châu Á")),

# kem đánh răng
(r"kem đánh răng|kđr",
 ("Đồ dùng cá nhân & gia đình","Chăm sóc răng miệng","Kem đánh răng")),

# bàn chải
(r"bàn chải đánh răng|bcđr",
 ("Đồ dùng cá nhân & gia đình","Chăm sóc răng miệng","Bàn chải đánh răng")),

# xà phòng
(r"xà phòng|soap",
 ("Đồ dùng cá nhân & gia đình","Chăm sóc cơ thể & da","Xà phòng & sữa tắm")),

# nước rửa tay
(r"nước rửa tay",
 ("Đồ dùng cá nhân & gia đình","Chăm sóc cơ thể & da","Nước rửa tay")),

# bát đĩa
(r"đĩa|bát|cốc",
 ("Đồ dùng cá nhân & gia đình","Dụng cụ nấu ăn","Bộ đồ ăn & đồ dùng 1 lần")),

# khay nhôm
(r"khay nhôm",
 ("Đồ dùng cá nhân & gia đình","Dụng cụ nấu ăn","Dụng cụ làm bếp")),

# rổ chậu
(r"rổ|chậu|vo gạo",
 ("Đồ dùng cá nhân & gia đình","Dụng cụ nấu ăn","Dụng cụ làm bếp")),
]


# ==============================
# MODEL INPUT
# ==============================

class Product(BaseModel):
    name: str


# ==============================
# RULE ENGINE
# ==============================

def apply_rules(name):

    name = name.lower()

    for pattern,cat in RULES:

        if re.search(pattern,name):
            return cat

    return None


# ==============================
# AI fallback đơn giản
# ==============================

def ai_guess(name):

    name = name.lower()

    if "kẹo" in name:
        return ("Thực phẩm khô","Đồ ăn vặt","Kẹo")

    if "bánh" in name:
        return ("Thực phẩm khô","Đồ ăn vặt","Bánh quy")

    if "sữa" in name:
        return ("Đồ uống","Sữa thực vật","Không")

    if "trà" in name:
        return ("Đồ uống","Trà","Trà đóng chai & đóng lon")

    if "cà phê" in name:
        return ("Đồ uống","Cà phê","Cà phê hòa tan")

    return ("Thực phẩm khô","Lương thực khô","Không")


# ==============================
# API
# ==============================

@app.post("/classify")
def classify(product:Product):

    rule = apply_rules(product.name)

    if rule:
        c1,c2,c3 = rule
    else:
        c1,c2,c3 = ai_guess(product.name)

    return {
        "result": f"{product.name} - {c1} - {c2} - {c3}"
    }
