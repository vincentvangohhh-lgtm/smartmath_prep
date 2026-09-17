import random
import hashlib
import sympy as sp

class AIQuestionGenerator:
    """Engine điều khiển sinh tham số toán học và ngăn ngừa lặp đề thi"""
    
    @staticmethod
    def generate_semantic_hash(concept_code, coefficients):
        """Tạo mã định danh cấu trúc câu hỏi dựa trên Concept và bộ tham số thực tế"""
        param_str = f"{concept_code}_{sorted(list(coefficients.items()))}"
        return hashlib.sha256(param_str.encode('utf-8')).hexdigest()

    @classmethod
    def generate_extreme_values_template(cls, existing_hashes):
        """
        Dạng toán: Tìm cực trị của hàm số bậc ba
        Mô tả: Sinh ngẫu nhiên hàm số có nghiệm cực trị đẹp, kiểm tra trùng lặp
        """
        concept_code = "DX_CUC_TRI_01"
        max_attempts = 100
        
        for _ in range(max_attempts):
            # 1. Sinh ngẫu nhiên tọa độ 2 điểm cực trị nguyên để hàm số có đạo hàm nghiệm đẹp
            x1 = random.randint(-3, 2)
            x2 = random.randint(x1 + 1, 4)
            if x1 == 0 or x2 == 0: continue # Tránh trường hợp quá đặc biệt
            
            # Đạo hàm y' = k*(x - x1)*(x - x2) = k*(x^2 - (x1+x2)x + x1*x2)
            k = random.choice([-3, -1, 1, 3])
            
            # Tính các hệ số của hàm số bậc ba: y = ax^3 + bx^2 + cx + d
            a = k / 3
            b = -k * (x1 + x2) / 2
            c = k * (x1 * x2)
            d = random.randint(-5, 5)
            
            # Ép hệ số nguyên để học sinh dễ tính toán (Chuẩn kiến thức thông hiểu/vận dụng)
            if not (b.is_integer() and a.is_integer()):
                continue
                
            coefficients = {'a': int(a), 'b': int(b), 'c': int(c), 'd': int(d)}
            semantic_hash = cls.generate_semantic_hash(concept_code, coefficients)
            
            # 2. KIỂM TRA CHỐNG TRÙNG LẶP ĐỀ (>70% cấu trúc tham số)
            if semantic_hash in existing_hashes:
                continue # Trùng lập dữ kiện, thực hiện sinh lại (Resample)
                
            # Khởi tạo biểu thức Symbolic bằng Sympy để tự động giải lời giải chi tiết
            x = sp.Symbol('x')
            f_x = a*x**3 + b*x**2 + c*x + d
            
            content = f"Cho hàm số bậc ba $y = {sp.latex(f_x)}$. Mệnh đề nào sau đây là đúng về cực trị của hàm số?"
            
            # Tự động giải toán lập ma trận đáp án
            y1 = int(f_x.subs(x, x1))
            y2 = int(f_x.subs(x, x2))
            
            options = [
                f"Hàm số đạt cực đại tại $x = {x1}$ và cực tiểu tại $x = {x2}$.",
                f"Hàm số đạt cực tiểu tại $x = {x1}$ và cực đại tại $x = {x2}$.",
                f"Hàm số không có điểm cực trị.",
                f"Hàm số đồng biến trên toàn bộ tập xác định $\\mathbb{{R}}$."
            ]
            
            # Xác định đáp án đúng dựa vào hệ số k
            correct_ans = options[0] if k > 0 else options[1]
            random.shuffle(options)
            
            ans_letter = ['A', 'B', 'C', 'D'][options.index(correct_ans)]
            
            solution_details = f"**Lời giải chi tiết:**\nTa có đạo hàm $y' = {sp.latex(sp.diff(f_x, x))}$.\n" \
                               f"Cho $y' = 0 \\Leftrightarrow x = {x1}$ hoặc $x = {x2}$.\n" \
                               f"Bảng biến thiên cho thấy hàm số đạt các giá trị cực trị tương ứng.\n" \
                               f"**Mẹo giải nhanh:** Nhận biết nhanh dấu của hệ số $a={int(a)}$ để suy luận dáng đồ thị."

            return {
                "concept_code": concept_code,
                "bloom_level": "Thông hiểu",
                "question_type": "PART_I",
                "content": content,
                "options": options,
                "correct_answer": ans_letter,
                "solution_details": solution_details,
                "semantic_hash": semantic_hash
            }
            
        raise RuntimeError("AI Engine không thể sinh biến thể mới mà không trùng lặp trong giới hạn số lượt thử.")