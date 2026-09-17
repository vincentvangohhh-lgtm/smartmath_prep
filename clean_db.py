import os
from app import create_app, db
from app.models import Question

# Khởi tạo Flask Context để kết nối với Database
app = create_app()

with app.app_context():
    # Lấy tất cả các câu hỏi thuộc Part I (Trắc nghiệm đơn)
    questions = Question.query.filter_by(question_type="PART_I").all()

    count = 0
    for q in questions:
        modified = False
        
        # Hàm loại bỏ tiền tố thừa như "A. ", "A. A. ", "A.  "
        def clean_option(text, prefix):
            if not text:
                return text
            new_text = text.strip()
            # Vòng lặp xóa nếu dính nhiều tầng tiền tố lặp
            while new_text.upper().startswith(f"{prefix}.") or new_text.upper().startswith(f"{prefix} ."):
                new_text = new_text[2:].strip()
                if new_text.startswith('.') or new_text.startswith(')'):
                    new_text = new_text[1:].strip()
            return new_text

        # Tiến hành làm sạch từng option
        new_a = clean_option(q.option_a, "A")
        new_b = clean_option(q.option_b, "B")
        new_c = clean_option(q.option_c, "C")
        new_d = clean_option(q.option_d, "D")
        
        # Nếu có sự thay đổi thì cập nhật và đánh dấu
        if new_a != q.option_a: q.option_a = new_a; modified = True
        if new_b != q.option_b: q.option_b = new_b; modified = True
        if new_c != q.option_c: q.option_c = new_c; modified = True
        if new_d != q.option_d: q.option_d = new_d; modified = True
        
        # Sửa tay dữ liệu câu OXYZ (Câu 4) bị trùng đáp án H(1;0;0) sang H(1;0;-2) để tạo độ nhiễu
        if q.content and "hình chiếu vuông góc" in q.content and q.option_c and "1;0;0" in q.option_c:
            q.option_c = "H(1; 0; -2)"
            modified = True

        if modified:
            count += 1

    # Commit thay đổi vào cơ sở dữ liệu
    db.session.commit()
    print(f"\n[SUCCESS] Da don dep va lam sach du lieu thanh cong cho {count} cau hoi!\n")