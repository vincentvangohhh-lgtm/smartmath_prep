import random
import math
from math import gcd

# Import db và Model Question từ ứng dụng của bạn để trả về đối tượng câu hỏi
from app import db
from app.models import Question

# ==============================================================================
# KHU VỰC 22 DẠNG TOÁN TRẮC NGHIỆM (PART_I) - CODE CŨ NGUYÊN BẢN
# ==============================================================================

def generate_dang_1():
    a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    x1 = random.randint(1, 2)
    x2 = random.randint(3, 5)
    prefix_a = "" if a == 1 else ("-" if a == -1 else str(a))
    content = f"Cho hàm số $y=f(x)$ xác định trên $\\mathbb{{R}}$ và có đạo hàm $f'(x) = {prefix_a}x(x - {x1})^2(x - {x2})^3$. Số điểm cực trị của hàm số đã cho là:"
    return Question(    
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer="B. 2", option_a="A. 1", option_b="B. 2", option_c="C. 3", option_d="D. 4", 
        semantic_hash="PARAM_PART1_CUCTRI"
    )

def generate_dang_2():
    m = random.randint(1, 10)
    ab_length = round((4 * m**2 + 16 * m**6)**0.5, 2)
    content = f"Biết rằng đồ thị của hàm số $y = x^3 - {3*m}x^2 + 2$ có hai điểm cực trị $A$ và $B$. Tính độ dài đoạn thẳng $AB$."
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"B. {ab_length}", option_a=f"A. {round(ab_length + 2, 2)}", option_b=f"B. {ab_length}", 
        option_c=f"C. {round(ab_length - 1, 2)}", option_d=f"D. {round(ab_length*1.2, 2)}", 
        semantic_hash="PARAM_PART1_DODAIAB"
    )

def generate_dang_3():
    base = random.choice([2, 3, 5])
    diff = random.randint(1, 4)
    power = random.randint(1, 3)
    right_bound = (base ** power) + diff
    content = f"Bất phương trình $\\log_{{{base}}}(x - {diff}) < {power}$ có tập nghiệm là:"
    return Question(
        concept_code="MU_LOGARIT", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"C. $({diff}; {right_bound})$", option_a=f"A. $(-\\infty; {right_bound})$", option_b=f"B. $({diff}; {base**power})$", 
        option_c=f"C. $({diff}; {right_bound})$", option_d=f"D. $({diff}; +\\infty)$", 
        semantic_hash="PARAM_PART1_LOGBPT"
    )

def generate_dang_4():
    a_val = random.choice([-2, -1, 1, 2])
    b_val = random.choice([-4, -2, 2, 4])
    c_val = random.randint(-3, 3)
    sign_a = "a < 0" if a_val < 0 else "a > 0"
    sign_b = "b > 0" if b_val > 0 else "b < 0"
    content = f"Cho hàm số trùng phương $y = {a_val}x^4 + {b_val}x^2 + {c_val}$. Mệnh đề nào sau đây đúng về dấu của các hệ số $a$ và $b$?"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"B. ${sign_a}$ và ${sign_b}$", option_a=f"A. ${sign_a}$ và $b$ ngược dấu với $a$", option_b=f"B. ${sign_a}$ và ${sign_b}$", 
        option_c="C. $a > 0$ và $b > 0$", option_d="D. $a < 0$ và $b < 0$", 
        semantic_hash="PARAM_PART1_DOTHITHPT"
    )

def generate_dang_5():
    m_val = random.randint(2, 5)
    n_val = random.randint(2, 4)
    numerator = m_val * n_val + 1
    content = f"Rút gọn biểu thức $P = x^{{{m_val}}} \\cdot \\sqrt[{n_val}]{{x}}$ (với $x > 0$)."
    return Question(
        concept_code="MU_LOGARIT", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"C. $P = x^{{\\frac{{{numerator}}}{{{n_val}}}}}$", option_a=f"A. $P = x^{{{numerator}}}$", option_b=f"B. $P = x^{{\\frac{{{m_val}}}{{{n_val}}}}}$", 
        option_c=f"C. $P = x^{{\\frac{{{numerator}}}{{{n_val}}}}}$", option_d=f"D. $P = x^{{\\frac{{{n_val}}}{{{numerator}}}}}$", 
        semantic_hash="PARAM_PART1_LUYTHUA"
    )

def generate_dang_6():
    a_val = random.randint(2, 6)
    content = f"Tìm tập xác định $D$ của hàm số $y = \\ln({a_val} - x)$."
    return Question(
        concept_code="MU_LOGARIT", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"B. $D = (-\\infty; {a_val})$", option_a=f"A. $D = ({a_val}; +\\infty)$", option_b=f"B. $D = (-\\infty; {a_val})$", 
        option_c=f"C. $D = \\mathbb{{R}} \\setminus \\{{{a_val}\\}}$", option_d=f"D. $D = [-\\infty; {a_val})$", 
        semantic_hash="PARAM_PART1_TXD"
    )

def generate_dang_7():
    h = random.choice([3, 6, 9, 12])
    edge = random.randint(2, 5)
    v_correct = (h // 3) * (edge ** 2)
    content = f"Cho khối chóp $S.ABCD$ có đáy $ABCD$ là hình vuông cạnh ${edge}$, cạnh bên $SA$ vuông góc với mặt phẳng đáy và $SA = {h}$. Tính thể tích $V$ của khối chóp đã cho."
    return Question(
        concept_code="KHOI_DA_DIEN", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"C. $V = {v_correct}$", option_a=f"A. $V = {h * edge * 4}$", option_b=f"B. $V = {h * (edge ** 2)}$", 
        option_c=f"C. $V = {v_correct}$", option_d=f"D. $V = {v_correct // 2}$", 
        semantic_hash="PARAM_PART1_VTICH_CHOP"
    )

def generate_dang_8():
    a, b, c = random.randint(-4, 4), random.randint(-4, 4), random.randint(-4, 4)
    r = random.choice([2, 3, 4, 5])
    r_sq = r ** 2
    sign_x = f"+ {-a}" if a < 0 else f"- {a}" if a > 0 else ""
    sign_y = f"+ {-b}" if b < 0 else f"- {b}" if b > 0 else ""
    sign_z = f"+ {-c}" if c < 0 else f"- {c}" if c > 0 else ""
    content = f"Trong không gian $Oxyz$, viết phương trình mặt cầu $(S)$ có tâm $I({a}; {b}; {c})$ và bán kính $R = {r}$."
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"B. $(x {sign_x})^2 + (y {sign_y})^2 + (z {sign_z})^2 = {r_sq}$", option_a=f"A. $(x {sign_x})^2 + (y {sign_y})^2 + (z {sign_z})^2 = {r}$", option_b=f"B. $(x {sign_x})^2 + (y {sign_y})^2 + (z {sign_z})^2 = {r_sq}$", 
        option_c=f"C. $(x + {a})^2 + (y + {b})^2 + (z + {c})^2 = {r_sq}$", option_d=f"D. $(x - {a})^2 + (y - {b})^2 + (z - {c})^2 = {r}$", 
        semantic_hash="PARAM_PART1_MATCAU"
    )

def generate_dang_9():
    val_f = random.randint(2, 6)
    val_g = random.randint(-5, 5)
    while val_g == 0: val_g = random.randint(-5, 5)
    ans = 2 * val_f - 3 * val_g
    content = f"Biết $\\int_{{0}}^{{2}} f(x)dx = {val_f}$ và $\\int_{{0}}^{{2}} g(x)dx = {val_g}$. Tính tích phân $I = \\int_{{0}}^{{2}} [2f(x) - 3g(x)]dx$."
    return Question(
        concept_code="NGUYEN_HAM_TICH_PHAN", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"B. $I = {ans}$", option_a=f"A. $I = {val_f + val_g}$", option_b=f"B. $I = {ans}$", 
        option_c=f"C. $I = {2 * val_f + 3 * val_g}$", option_d=f"D. $I = {val_f - val_g}$", 
        semantic_hash="PARAM_PART1_TPHAN_TCHAT"
    )

def generate_dang_10():
    x_a, y_a, z_a = random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)
    while x_a == 0 and y_a == 0: x_a = random.randint(-3, 3)
    content = f"Trong không gian $Oxyz$, cho điểm $A({x_a}; {y_a}; {z_a})$. Tìm tọa độ điểm $H$ là hình chiếu vuông góc của điểm $A$ trên mặt phẳng $(Oxy)$."
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"A. $H({x_a}; {y_a}; 0)$", option_a=f"A. $H({x_a}; {y_a}; 0)$", option_b=f"B. $H(0; 0; {z_a})$", 
        option_c=f"C. $H({x_a}; 0; 0)$", option_d=f"D. $H({-x_a}; {-y_a}; {z_a})$", 
        semantic_hash="PARAM_PART1_OXYZ_HINHCHIEU"
    )

def generate_dang_11():
    edge_a = random.choice([2, 3, 4, 5])
    content = f"Cho hình chóp $S.ABC$ có đáy $ABC$ là tam giác vuông tại $B$, cạnh $AB = {edge_a}$. Cạnh bên $SA$ vuông góc với mặt phẳng đáy và $SA = {edge_a}$. Tính góc giữa đường thẳng $SB$ và mặt phẳng $(ABC)$."
    return Question(
        concept_code="HINH_HOC_CO_DIEN", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer="C. $45^\\circ$", option_a="A. $30^\\circ$", option_b="B. $60^\\circ$", 
        option_c="C. $45^\\circ$", option_d="D. $90^\\circ$", 
        semantic_hash="PARAM_PART1_GOC_DUONG_MAT"
    )

def generate_dang_12():
    num_blue = random.randint(4, 6)
    num_red = random.randint(5, 7)
    total = num_blue + num_red
    n_omega = total * (total - 1) // 2
    n_a = num_blue * (num_blue - 1) // 2
    common = gcd(n_a, n_omega)
    t_num = n_a // common
    t_den = n_omega // common
    content = f"Một hộp chứa {num_blue} viên bi xanh và {num_red} viên bi đỏ. Chọn ngẫu nhiên đồng thời 2 viên bi từ hộp. Tính xác suất $P$ để chọn được 2 viên bi đều có màu xanh."
    return Question(
        concept_code="XAC_SUAT", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"A. $P = \\frac{{{t_num}}}{{{t_den}}}$", option_a=f"A. $P = \\frac{{{t_num}}}{{{t_den}}}$", option_b=f"B. $P = \\frac{{{num_blue}}}{{{total}}}$", 
        option_c=f"C. $P = \\frac{{{num_blue * (num_blue - 1)}}}{{{total * total}}}$", option_d=f"D. $P = \\frac{{{num_red * (num_red - 1)}}}{{{total * (total - 1)}}}$", 
        semantic_hash="PARAM_PART1_XACSUAT_TOHOP"
    )

def generate_dang_13():
    n1, n2, n3, n4 = random.randint(5, 10), random.randint(12, 18), random.randint(6, 11), random.randint(3, 7)
    total = n1 + n2 + n3 + n4
    content = f"Khảo sát thời gian tự học trong ngày của {total} học sinh, ta thu được bảng số liệu ghép nhóm sau:\n* $[0; 2)$ giờ: {n1} HS\n* $[2; 4)$ giờ: {n2} HS\n* $[4; 6)$ giờ: {n3} HS\n* $[6; 8)$ giờ: {n4} HS\nNhóm chứa trung vị $M_e$ là:"
    return Question(
        concept_code="THONG_KE", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer="B. $[2; 4)$", option_a="A. $[0; 2)$", option_b="B. $[2; 4)$", 
        option_c="C. $[4; 6)$", option_d="D. $[6; 8)$", 
        semantic_hash="PARAM_PART1_TK_TRUNGVI"
    )

def generate_dang_14():
    d1 = random.randint(-5, 5)
    while d1 == 0: d1 = random.randint(-5, 5)
    d2 = d1 + random.choice([-3, -2, 2, 3])
    content = f"Trong không gian $Oxyz$, cho hai mặt phẳng $(\\alpha): 2x - y + 3z + {d1} = 0$ và $(\\beta): 2x - y + 3z + {d2} = 0$. Vị trí tương đối của hai mặt phẳng là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer="C. Song song với nhau", option_a="A. Cắt nhau nhưng không vuông góc", option_b="B. Trùng nhau", 
        option_c="C. Song song với nhau", option_d="D. Vuông góc với nhau", 
        semantic_hash="PARAM_PART1_OXYZ_VTTD"
    )

def generate_dang_15():
    a = random.choice([2, 4, 6])
    ans = round(a / (2**0.5), 2)
    content = f"Cho hình chóp $S.ABC$ có đáy $ABC$ là tam giác vuông tại $B$, cạnh $AB = {a}$. Cạnh bên $SA$ vuông góc với đáy và $SA = {a}$. Tính khoảng cách $d$ từ $A$ đến mặt phẳng $(SBC)$."
    return Question(
        concept_code="HINH_HOC_CO_DIEN", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"A. {ans}", option_a=f"A. {ans}", option_b=f"B. {a}", 
        option_c=f"C. {round(a * (2**0.5), 2)}", option_d=f"D. {round(a / 2, 2)}", 
        semantic_hash="PARAM_PART1_KHOANGCACH"
    )

def generate_dang_16():
    p = random.choice([50, 100, 200])
    r = random.choice([5.2, 6.5, 7.2])
    ans = round(p * ((1 + r/100) ** 3), 2)
    content = f"Một người gửi {p} triệu đồng vào ngân hàng theo hình thức lãi kép với lãi suất ${r}\\%$ một năm. Hỏi sau 3 năm người đó rút được cả gốc lẫn lãi là bao nhiêu triệu đồng?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"C. {ans}", option_a=f"A. {round(p * (1 + 3 * r / 100), 2)}", option_b=f"B. {round(ans * 0.9, 2)}", 
        option_c=f"C. {ans}", option_d=f"D. {round(ans * 1.1, 2)}", 
        semantic_hash="PARAM_PART1_LAIKEP"
    )

def generate_dang_17():
    n0 = random.randint(80, 95)
    r_pop = random.choice([0.9, 1.1, 1.2])
    ans_pop = round(n0 * math.exp((r_pop / 100) * 5), 2)
    content = f"Dân số của một quốc gia năm 2026 là {n0} triệu người. Biết tỉ lệ tăng dân số hàng năm là ${r_pop}\\%$. Dự đoán dân số của quốc gia đó vào năm 2031 là bao nhiêu triệu người?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"B. {ans_pop}", option_a=f"A. {round(n0 + (n0 * r_pop / 100) * 5, 2)}", option_b=f"B. {ans_pop}", 
        option_c=f"C. {round(ans_pop * 1.05, 2)}", option_d=f"D. {round(ans_pop * 0.95, 2)}", 
        semantic_hash="PARAM_PART1_DANSO"
    )

def generate_dang_18():
    amount = random.choice([500, 600, 800])
    r_val = 0.8 / 100
    pay_monthly = round((amount * r_val * ((1 + r_val)**24)) / (((1 + r_val)**24) - 1), 2)
    content = f"Một khách hàng vay ngân hàng {amount} triệu đồng trả góp với lãi suất $0.8\\%$ một tháng. Hỏi số tiền người đó phải trả đều đặn hàng tháng là bao nhiêu triệu đồng để hết nợ sau 24 tháng?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content, 
        correct_answer=f"A. {pay_monthly}", option_a=f"A. {pay_monthly}", option_b=f"B. {round(amount / 24, 2)}", 
        option_c=f"C. {round(pay_monthly * 1.2, 2)}", option_d=f"D. {round(pay_monthly * 0.8, 2)}", 
        semantic_hash="PARAM_PART1_TRAGOP"
    )

def generate_dang_19():
    m0 = random.choice([100, 200, 500])
    m_remain = round(m0 * (0.5 ** 3), 2)
    content = f"Một chất phóng xạ có khối lượng ban đầu là {m0} g và chu kỳ bán rã là 8 ngày. Tính khối lượng chất phóng xạ còn lại sau 24 ngày."
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content, 
        correct_answer=f"D. {m_remain}", option_a=f"A. {round(m0 / 2, 2)}", option_b="B. 0 g", 
        option_c=f"C. {round(m0 * 0.75, 2)}", option_d=f"D. {m_remain}", 
        semantic_hash="PARAM_PART1_PHONGRU"
    )

def generate_dang_20():
    power = random.randint(2, 4)
    ans_num = power + 0.5
    content = f"Cho $a > 0$ và $a \\neq 1$. Tính giá trị của biểu thức $P = \\log_{{a}}(a^{{{power}}} \\cdot \\sqrt{{a}})$."
    return Question(
        concept_code="MU_LOGARIT", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"B. {ans_num}", option_a=f"A. {power}", option_b=f"B. {ans_num}", 
        option_c=f"C. {power * 2}", option_d=f"D. $\\frac{{1}}{{{power}}}$", 
        semantic_hash="PARAM_PART1_RUTGONLOG"
    )

def generate_dang_21():
    edge_base = random.randint(2, 5)
    h_chop = random.choice([3, 6, 9])
    v_correct = round((1/3) * (edge_base ** 2) * h_chop, 2)
    content = f"Tính thể tích $V$ của khối chóp tứ giác đều có tất cả các cạnh đáy bằng {edge_base} và chiều cao bằng {h_chop}."
    return Question(
        concept_code="KHOI_DA_DIEN", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"A. {v_correct}", option_a=f"A. {v_correct}", option_b=f"B. {v_correct * 3}", 
        option_c=f"C. {round(v_correct / 2, 2)}", option_d=f"D. {edge_base * h_chop}", 
        semantic_hash="PARAM_PART1_V_CHOPDEU"
    )

def generate_dang_22():
    s_base = random.randint(10, 25)
    h_prism = random.randint(4, 8)
    v_prism = s_base * h_prism
    content = f"Cho khối lăng trụ có diện tích đáy $B = {s_base}$ và chiều cao $h = {h_prism}$. Tính thể tích $V$ của khối lăng trụ đã cho."
    return Question(
        concept_code="KHOI_DA_DIEN", bloom_level="Nhận biết", question_type="PART_I", content=content, 
        correct_answer=f"C. {v_prism}", option_a=f"A. {round(v_prism / 3, 2)}", option_b=f"B. {v_prism + 10}", 
        option_c=f"C. {v_prism}", option_d=f"D. {round(v_prism / 2, 2)}", 
        semantic_hash="PARAM_PART1_V_LANGTRU"
    )

# ==============================================================================
# KHU VỰC 6 DẠNG TOÁN PHẦN II (ĐÚNG / SAI) - CODE CŨ NGUYÊN BẢN
# ==============================================================================

def generate_part2_dang_1():
    x1, y1, z1 = random.randint(-2, 2), random.randint(-2, 2), random.randint(1, 3)
    x2, y2, z2 = random.randint(1, 3), random.randint(-3, -1), random.randint(-2, 2)
    dot_prod = x1*x2 + y1*y2 + z1*z2
    x_2u, y_2u, z_2u = 2*x1, 2*y1, 2*z1
    content = f"Trong không gian $Oxyz$, cho hai vectơ $\\vec{{u}} = ({x1}; {y1}; {z1})$ và $\\vec{{v}} = ({x2}; {y2}; {z2})$. Xét các khẳng định sau:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_II", content=content,
        correct_answer="Đúng|Sai|Đúng|Sai",
        option_a=f"Tọa độ của vectơ $2\\vec{{u}}$ là $({x_2u}; {y_2u}; {z_2u})$.",
        option_b=f"Tích vô hướng của hai vectơ là $\\vec{{u}} \\cdot \\vec{{v}} = {dot_prod + 2}$.",
        option_c=f"Độ dài của vectơ $\\vec{{u}}$ là $|\\vec{{u}}| = \\sqrt{{{x1**2 + y1**2 + z1**2}}}$.",
        option_d="Tích có hướng $[\\vec{{u}}, \\vec{{v}}]$ là một số thực thay vì một vectơ.",
        semantic_hash="PARAM_PART2_D1_OXYZ"
    )

def generate_part2_dang_2():
    a = random.choice([2, 4, 6])
    content = f"Cho hàm số $f(x) = {a}x + \\cos(x)$. Xét các khẳng định về nguyên hàm và tích phân của hàm số trên $\\mathbb{{R}}$:"
    return Question(
        concept_code="NGUYEN_HAM_TICH_PHAN", bloom_level="Thông hiểu", question_type="PART_II", content=content,
        correct_answer="Đúng|Sai|Đúng|Sai",
        option_a=f"Một nguyên hàm của hàm số $f(x)$ là $F(x) = {a//2}x^2 + \\sin(x) + C$.",
        option_b=f"Hàm số $F(x) = {a} - \\sin(x)$ là một nguyên hàm của $f(x)$.",
        option_c=f"Tích phân $\\int_{{0}}^{{\\pi}} f(x)dx = \\frac{{{a}\\pi^2}}{{2}}$.",
        option_d="Mọi nguyên hàm $F(x)$ của $f(x)$ đều thỏa mãn $F(0) = 0$.",
        semantic_hash="PARAM_PART2_D2_TCHAT"
    )

def generate_part2_dang_3():
    t0 = random.randint(2, 4)
    s_t0 = -(t0**3) + 6*(t0**2)
    content = f"Một vật chuyển động biến đổi với vận tốc tính theo thời gian $t$ (giây) là $v(t) = -3t^2 + 12t$ (m/s). Khảo sát các phát biểu sau:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_II", content=content,
        correct_answer="Đúng|Đúng|Sai|Đúng",
        option_a="Vận tốc của vật đạt giá trị lớn nhất tại thời điểm $t = 2$ giây.",
        option_b=f"Quãng đường vật đi được từ thời điểm $t = 0$ đến $t = {t0}$ là {s_t0} mét.",
        option_c="Gia tốc của vật tại thời điểm $t = 1$ giây là $a(1) = 12$ $m/s^2$.",
        option_d="Vật sẽ dừng hẳn (vận tốc bằng 0) tại thời điểm $t = 4$ giây.",
        semantic_hash="PARAM_PART2_D3_UDUNG"
    )

def generate_part2_dang_4():
    m = random.randint(2, 4)
    y_cd = 2 * (m**3)
    content = f"Cho hàm số $y = x^3 - {3 * (m**2)}x$. Xét các khẳng định sau:"
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_II", content=content,
        correct_answer="Sai|Đúng|Đúng|Sai",
        option_a=f"Hàm số đạt cực đại tại điểm $x = {m}$.",
        option_b=f"Giá trị cực đại của hàm số đã cho bằng {y_cd}.",
        option_c=f"Hàm số nghịch biến trên khoảng $({-m}; {m})$.",
        option_d=f"Trên đoạn $[0; {m+2}]$, giá trị nhỏ nhất của hàm số là 0.",
        semantic_hash="PARAM_PART2_D4_MINMAX"
    )

def generate_part2_dang_5():
    a = random.randint(1, 2)
    b = a + random.randint(2, 3)
    content = f"Gọi $(H)$ là hình phẳng giới hạn bởi đồ thị hàm số $y = x^2$, trục hoành và hai đường thẳng $x = {a}, x = {b}$. Khảo sát các phát biểu sau:"
    return Question(
        concept_code="NGUYEN_HAM_TICH_PHAN", bloom_level="Thông hiểu", question_type="PART_II", content=content,
        correct_answer="Đúng|Sai|Đúng|Sai",
        option_a=f"Diện tích $S$ của hình phẳng $(H)$ được tính bằng công thức $S = \\int_{{{a}}}^{{{b}}} x^2 dx$.",
        option_b=f"Diện tích của hình phẳng $(H)$ có giá trị bằng $\\frac{{{b**2 - a**2}}}{{2}}$.",
        option_c=f"Thể tích $V$ của khối tròn xoay thu được khi quay $(H)$ quanh trục $Ox$ là $V = \\pi \\int_{{{a}}}^{{{b}}} x^4 dx$.",
        option_d="Nếu thay bằng đồ thị $y = -x^2$ thì diện tích $S$ sẽ đổi dấu thành giá trị âm.",
        semantic_hash="PARAM_PART2_D5_DIENTICH"
    )

def generate_part2_dang_6():
    A = random.randint(1, 3)
    D = random.randint(-5, 5)
    val_M = A*1 + 2*2 - 3*3 + D
    ans_a = "Đúng" if val_M == 0 else "Sai"
    content = f"Trong không gian $Oxyz$, cho mặt phẳng $(P): {A}x + 2y - 3z + {D} = 0$ và điểm $M(1; 2; 3)$. Xét các phát biểu sau:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_II", content=content,
        correct_answer=f"{ans_a}|Đúng|Sai|Sai",
        option_a=f"Điểm $M(1; 2; 3)$ thuộc mặt phẳng $(P)$.",
        option_b=f"Một vectơ pháp tuyến của mặt phẳng $(P)$ là $\\vec{{n}} = ({A}; 2; -3)$.",
        option_c="Mặt phẳng $(P)$ song song với trục hoành $Ox$.",
        option_d=f"Mặt phẳng $(Q): {A}x + 2y - 3z + {D+5} = 0$ vuông góc với mặt phẳng $(P)$.",
        semantic_hash="PARAM_PART2_D6_MATPHANG"
    )

# ==============================================================================
# KHU VỰC 8 DẠNG TOÁN PHẦN III (ĐIỀN SỐ) - CODE CŨ NGUYÊN BẢN
# ==============================================================================

def generate_part3_dang_1():
    a_val = 1
    b_val = -1
    c_val = 2
    P = a_val + b_val + c_val
    content = "Cho tích phân $I = \\int_{0}^{1} \\frac{x}{x + 1} dx = a + b\\ln(c)$ với $a, b \\in \\mathbb{Z}$ và $c$ là số nguyên tố. Tính giá trị của biểu thức $P = a + b + c$."
    return Question(
        concept_code="TICH_PHAN_AN", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(P), semantic_hash="PARAM_P3_D1_INTEGRAL_AN"
    )

def generate_part3_dang_2():
    k = 3
    V_div_pi = (k**2) * 8 // 3
    content = f"Tính thể tích $V$ của khối tròn xoay thu được khi quay hình phẳng giới hạn bởi đồ thị hàm số $y = {k}x$, trục hoành và hai đường thẳng $x = 0, x = 2$ xung quanh trục $Ox$. Điền giá trị của $\\frac{{V}}{{\\pi}}$."
    return Question(
        concept_code="THE_TICH_TRON_XOAY", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(V_div_pi), semantic_hash="PARAM_P3_D2_VOLUME"
    )

def generate_part3_dang_3():
    a = random.choice([2, 4, 6])
    b = random.randint(5, 15)
    t0 = random.randint(3, 5)
    S = (a // 2) * (t0 ** 2) + b * t0
    content = f"Một vật chuyển động với vận tốc $v(t) = {a}t + {b}$ (m/s). Tính quãng đường $S$ (mét) mà vật di chuyển được từ thời điểm $t = 0$ (s) đến thời điểm $t = {t0}$ (s)."
    return Question(
        concept_code="UD_TICH_PHAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(S), semantic_hash="PARAM_P3_D3_MOTION"
    )

def generate_part3_dang_4():
    ans_pct = 40
    content = "Cho hai biến cố $A$ và $B$ thỏa mãn $P(A) = 0{,}4$; $P(B) = 0{,}5$ và $P(A \\cap B) = 0{,}2$. Tính xác suất có điều kiện $P(A|B)$ (nhập kết quả dưới dạng tỷ lệ phần trăm, ví dụ nếu kết quả là $0{,}45$ thì điền 45)."
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(ans_pct), semantic_hash="PARAM_P3_D4_CONDITIONAL"
    )

def generate_part3_dang_5():
    ans = 59
    content = "Tỷ lệ mắc bệnh hiểm nghèo $X$ trong cộng đồng là $1\\%$. Một loại xét nghiệm có độ chính xác như sau: Nếu có bệnh, xác suất kết quả dương tính là $95\\%$; nếu không có bệnh, xác suất bị kết quả dương tính giả là $5\\%$. Chọn ngẫu nhiên một người trong cộng đồng, tính xác suất để người đó có kết quả xét nghiệm dương tính (Nhập kết quả theo đơn vị phần nghìn, ví dụ xác suất là $0{,}059$ thì điền 59)."
    return Question(
        concept_code="XAC_SUAT_TOAN_PHAN", bloom_level="Vận dụng cao", question_type="PART_III",
        content=content, correct_answer=str(ans), semantic_hash="PARAM_P3_D5_BAYES"
    )

def generate_part3_dang_6():
    start = random.randint(10, 20)
    step = random.randint(5, 10)
    num_groups = 4
    R = num_groups * step
    content = f"Một mẫu số liệu ghép nhóm về chiều cao của học sinh gồm {num_groups} nhóm liên tiếp: [{start}; {start+step}), [{start+step}; {start+2*step}), [{start+2*step}; {start+3*step}), và [{start+3*step}; {start+4*step}]. Tìm khoảng biến thiên $R$ của mẫu số liệu ghép nhóm này."
    return Question(
        concept_code="THONG_KE_GHEP_NHOM", bloom_level="Thông hiểu", question_type="PART_III",
        content=content, correct_answer=str(R), semantic_hash="PARAM_P3_D6_STATISTICS"
    )

def generate_part3_dang_7():
    L = random.choice([40, 80, 120])
    x_opt = L // 4
    S_max = x_opt * (L - 2 * x_opt)
    content = f"Một người nông dân muốn rào một khu đất hình chữ nhật dọc theo một bức tường thẳng có sẵn (không cần rào phía bức tường) bằng {L} mét lưới sắt. Tính diện tích lớn nhất $S_{{max}}$ (mét vuông) của khu đất mà người đó có thể rào được."
    return Question(
        concept_code="TOI_UU_HOA_MAXMIN", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(S_max), semantic_hash="PARAM_P3_D7_OPTIMIZATION"
    )

def generate_part3_dang_8():
    k = random.choice([4, 9])
    ans_count = 5 if k == 4 else 7
    content = f"Có bao nhiêu giá trị nguyên của tham số $m$ để hàm số $y = \\frac{{1}}{{3}}x^3 - mx^2 + {k}x + 2026$ đồng biến trên khoảng $(-\\infty; +\\infty)$?"
    return Question(
        concept_code="TIM_THAM_SO_M", bloom_level="Vận dụng", question_type="PART_III",
        content=content, correct_answer=str(ans_count), semantic_hash="PARAM_P3_D8_MONOTONIC"
    )

# ==============================================================================
# HÀM ĐIỀU PHỐI ĐỘNG SINH ĐỀ KHẢO SÁT BAN ĐẦU - CODE CŨ NGUYÊN BẢN
# ==============================================================================

def generate_parametric_questions():
    """Hàm tham số hóa dữ liệu để sinh đề khảo sát ngẫu nhiên thay số hoàn toàn mới mỗi lần gọi"""
    questions_pool = []

    # PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN (BỐC THĂM 12 CÂU TỪ 22 DẠNG)
    all_part1_formats = [
        generate_dang_1, generate_dang_2, generate_dang_3, generate_dang_4,
        generate_dang_5, generate_dang_6, generate_dang_7, generate_dang_8,
        generate_dang_9, generate_dang_10, generate_dang_11, generate_dang_12,
        generate_dang_13, generate_dang_14, generate_dang_15, generate_dang_16,
        generate_dang_17, generate_dang_18, generate_dang_19, generate_dang_20,
        generate_dang_21, generate_dang_22
    ]
    selected_formats = random.sample(all_part1_formats, 12)
    for i, format_func in enumerate(selected_formats):
        question_obj = format_func()
        question_obj.semantic_hash = f"{question_obj.semantic_hash}_{i}_{random.randint(1000, 9999)}"
        questions_pool.append(question_obj)

    # PHẦN II: ĐÚNG / SAI (BỐC THĂM 2 CÂU TỪ 6 DẠNG)
    all_part2_formats = [
        generate_part2_dang_1, generate_part2_dang_2, generate_part2_dang_3,
        generate_part2_dang_4, generate_part2_dang_5, generate_part2_dang_6
    ]
    selected_p2 = random.sample(all_part2_formats, 2)
    for index_p2, format_func_p2 in enumerate(selected_p2):
        q_obj_p2 = format_func_p2()
        q_obj_p2.semantic_hash = f"{q_obj_p2.semantic_hash}_p2_{index_p2}_{random.randint(1000, 9999)}"
        
        text_a = getattr(q_obj_p2, 'option_a', None) or getattr(q_obj_p2, 'choice_a', None) or getattr(q_obj_p2, 'sub_q_a', None) or ""
        text_b = getattr(q_obj_p2, 'option_b', None) or getattr(q_obj_p2, 'choice_b', None) or getattr(q_obj_p2, 'sub_q_a', None) or ""
        text_c = getattr(q_obj_p2, 'option_c', None) or getattr(q_obj_p2, 'choice_c', None) or getattr(q_obj_p2, 'sub_q_a', None) or ""
        text_d = getattr(q_obj_p2, 'option_d', None) or getattr(q_obj_p2, 'choice_d', None) or getattr(q_obj_p2, 'sub_q_a', None) or ""
        
        q_obj_p2.option_a = q_obj_p2.choice_a = q_obj_p2.sub_q_a = text_a
        q_obj_p2.option_b = q_obj_p2.choice_b = q_obj_p2.sub_q_b = text_b
        q_obj_p2.option_c = q_obj_p2.choice_c = q_obj_p2.sub_q_c = text_c
        q_obj_p2.option_d = q_obj_p2.choice_d = q_obj_p2.sub_q_d = text_d
        
        questions_pool.append(q_obj_p2)

    # PHẦN III: ĐIỀN SỐ TRẢ LỜI NGẮN (BỐC THĂM 4 CÂU TỪ 8 DẠNG)
    all_part3_formats = [
        generate_part3_dang_1, generate_part3_dang_2, generate_part3_dang_3,
        generate_part3_dang_4, generate_part3_dang_5, generate_part3_dang_6,
        generate_part3_dang_7, generate_part3_dang_8
    ]
    selected_p3 = random.sample(all_part3_formats, 4)
    for i, format_func_p3 in enumerate(selected_p3):
        q_obj_p3 = format_func_p3()
        q_obj_p3.semantic_hash = f"{q_obj_p3.semantic_hash}_p3_{i}_{random.randint(1000, 9999)}"
        questions_pool.append(q_obj_p3)

    return questions_pool

# ==============================================================================
# HÀM SINH ĐỀ CHUYÊN ĐỀ THEO LỘ TRÌNH 15 CÂU - CODE CŨ NGUYÊN BẢN
# ==============================================================================

def generate_roadmap_questions(day_id):
    """
    Hàm sinh chính xác 15 câu hỏi trắc nghiệm đơn (PART_I) thay số ngẫu nhiên theo chủ đề của Ngày học
    """
    questions_pool = []
    
    if day_id == 1:
        pool_formats = [generate_dang_1, generate_dang_2, generate_dang_4]
        for i in range(15):
            format_func = random.choice(pool_formats)
            q_obj = format_func()
            q_obj.semantic_hash = f"roadmap_d1_{i}_{random.randint(1000, 9999)}"
            questions_pool.append(q_obj)
            
    elif day_id == 2:
        pool_formats = [generate_dang_3, generate_dang_5, generate_dang_6, generate_dang_20]
        for i in range(15):
            format_func = random.choice(pool_formats)
            q_obj = format_func()
            q_obj.semantic_hash = f"roadmap_d2_{i}_{random.randint(1000, 9999)}"
            questions_pool.append(q_obj)
            
    elif day_id == 3:
        pool_formats = [generate_dang_8, generate_dang_10, generate_dang_14]
        for i in range(15):
            format_func = random.choice(pool_formats)
            q_obj = format_func()
            q_obj.semantic_hash = f"roadmap_d3_{i}_{random.randint(1000, 9999)}"
            questions_pool.append(q_obj)
            
    return questions_pool


# ==============================================================================
# BỔ SUNG TRỌN BỘ 19 DẠNG BÀI: ỨNG DỤNG ĐẠO HÀM KHẢO SÁT HÀM SỐ
# ==============================================================================

# Dạng 1: Sử dụng dấu của đạo hàm để tìm khoảng đồng biến, nghịch biến
def gen_ud_1_dau_dao_ham_don_dieu():
    a = random.choice([2, 3, 4])
    content = f"Cho hàm số $y = f(x)$ có đạo hàm $f'(x) = x^2 - {a*a}$. Mệnh đề nào sau đây đúng?"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. Hàm số nghịch biến trên khoảng ({-a}; {a})",
        option_a=f"A. Hàm số nghịch biến trên khoảng ({-a}; {a})",
        option_b=f"B. Hàm số đồng biến trên khoảng ({-a}; {a})",
        option_c=f"C. Hàm số nghịch biến trên khoảng ({a}; +\\infty)",
        option_d=f"D. Hàm số đồng biến trên khoảng (-\\infty; {a})",
        semantic_hash="UD_DONGDIEU_DAU_DAOHAM"
    )

# Dạng 2: Sử dụng BBT, đồ thị để tìm khoảng đồng biến, nghịch biến
def gen_ud_2_bbt_don_dieu():
    x1, x2 = random.randint(-3, -1), random.randint(1, 3)
    content = f"Cho hàm số $y=f(x)$ có bảng biến thiên với $f'(x) > 0$ trên $(-\\infty; {x1})$ và $({x2}; +\\infty)$, $f'(x) < 0$ trên $({x1}; {x2})$. Khẳng định nào sau đây đúng?"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"C. Hàm số đồng biến trên khoảng ({x2}; +\\infty)",
        option_a=f"A. Hàm số nghịch biến trên khoảng (-\\infty; {x1})",
        option_b=f"B. Hàm số đồng biến trên khoảng ({x1}; {x2})",
        option_c=f"C. Hàm số đồng biến trên khoảng ({x2}; +\\infty)",
        option_d=f"D. Hàm số nghịch biến trên khoảng ({x2}; +\\infty)",
        semantic_hash="UD_DONGDIEU_BBT"
    )

# Dạng 3: Sử dụng đồ thị f'(x) để tìm khoảng đồng biến, nghịch biến của f(x)
def gen_ud_3_dothi_fphay_don_dieu():
    x1, x2 = random.randint(-2, 0), random.randint(1, 4)
    content = f"Cho đồ thị hàm số $y = f'(x)$ cắt trục hoành tại hai điểm $x = {x1}$ và $x = {x2}$. Biết $f'(x) > 0$ khi $x \\in ({x1}; {x2})$. Hàm số $y = f(x)$ đồng biến trên khoảng nào?"
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"B. ({x1}; {x2})",
        option_a=f"A. (-\\infty; {x1})", option_b=f"B. ({x1}; {x2})",
        option_c=f"C. ({x2}; +\\infty)", option_d=f"D. (-\\infty; {x2})",
        semantic_hash="UD_DONGDIEU_DOTHI_FPHAY"
    )

# Dạng 4: Sử dụng dấu đạo hàm để tìm điểm cực trị
def gen_ud_4_dau_dao_ham_cuc_tri():
    a = random.randint(1, 5)
    content = f"Cho hàm số $y = f(x)$ có $f'(x) = (x - {a})^3(x + 2)^2$. Số điểm cực trị của hàm số là:"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. 1",
        option_a="A. 1", option_b="B. 2", option_c="C. 3", option_d="D. 0",
        semantic_hash="UD_CUCTRI_DAU_DAOHAM"
    )

# Dạng 5: Sử dụng BBT, đồ thị để tìm điểm cực trị
def gen_ud_5_bbt_cuc_tri():
    x_cd = random.randint(-2, 0)
    x_ct = random.randint(1, 3)
    content = f"Cho hàm số $y=f(x)$ liên tục trên $\\mathbb{{R}}$, có $f'(x)$ đổi dấu từ dương sang âm khi qua $x = {x_cd}$ và đổi dấu từ âm sang dương khi qua $x = {x_ct}$. Khẳng định nào đúng?"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"D. Hàm số đạt cực đại tại $x = {x_cd}$",
        option_a=f"A. Hàm số đạt cực đại tại $x = {x_ct}$",
        option_b=f"B. Hàm số đạt cực tiểu tại $x = {x_cd}$",
        option_c=f"C. Hàm số không có cực trị",
        option_d=f"D. Hàm số đạt cực đại tại $x = {x_cd}$",
        semantic_hash="UD_CUCTRI_BBT"
    )

# Dạng 6: Sử dụng đồ thị f'(x) để tìm cực trị của f(x)
def gen_ud_6_dothi_fphay_cuc_tri():
    x1, x2, x3 = -2, 1, 3
    content = f"Đồ thị $y=f'(x)$ cắt trục hoành tại 3 điểm phân biệt $x = {x1}, x = {x2}, x = {x3}$ và đổi dấu qua cả 3 điểm này. Hàm số $y=f(x)$ có bao nhiêu điểm cực trị?"
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="C. 3",
        option_a="A. 1", option_b="B. 2", option_c="C. 3", option_d="D. 4",
        semantic_hash="UD_CUCTRI_DOTHI_FPHAY"
    )

# Dạng 7: Bài toán thực tế ứng dụng tính đơn điệu và cực trị
def gen_ud_7_thuc_te_don_dieu_cuc_tri():
    v0 = random.randint(20, 40)
    content = f"Đạn pháo bắn lên theo phương trình độ cao $h(t) = {v0}t - 5t^2$ (mét). Độ cao cực đại mà đạn pháo đạt được là:"
    h_max = int(v0**2 / 20)
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"B. {h_max} m",
        option_a=f"A. {h_max - 10} m", option_b=f"B. {h_max} m",
        option_c=f"C. {h_max + 15} m", option_d=f"D. {h_max * 2} m",
        semantic_hash="UD_THUCTE_DON_DIEU_CUCTRI"
    )

# Dạng 8: Bài toán liên quan đến tính đơn điệu, cực trị có chứa tham số
def gen_ud_8_tham_so_cuc_tri():
    m = random.randint(1, 4)
    content = f"Tìm điều kiện của tham số $m$ để hàm số $y = x^3 - 3mx^2 + 3$ có 2 điểm cực trị."
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="A. $m \\neq 0$",
        option_a="A. $m \\neq 0$", option_b="B. $m = 0$",
        option_c="C. $m > 0$", option_d="D. $m < 0$",
        semantic_hash="UD_THAMSO_CUCTRI"
    )

# Dạng 9: Bài toán hàm hợp liên quan đến đơn điệu và cực trị
def gen_ud_9_ham_hop_cuc_tri():
    content = "Cho hàm số $f(x)$ có $f'(x) = x(x-1)$. Hỏi hàm số $g(x) = f(x^2)$ có bao nhiêu điểm cực trị?"
    return Question(
        concept_code="HAM_SO", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="C. 3",
        option_a="A. 1", option_b="B. 2", option_c="C. 3", option_d="D. 4",
        semantic_hash="UD_HAMHOP_CUCTRI"
    )

# Dạng 10: Tìm Min/Max khi biết đồ thị hoặc BBT
def gen_ud_10_minmax_bbt():
    min_v, max_v = random.randint(-5, -1), random.randint(2, 6)
    content = f"Cho hàm số $y=f(x)$ liên tục trên đoạn $[-1; 4]$ có $\\min_{{[-1;4]}}f(x) = {min_v}$ và $\\max_{{[-1;4]}}f(x) = {max_v}$. Giá trị $\\max_{{[-1;4]}}f(x) - \\min_{{[-1;4]}}f(x)$ là:"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"D. {max_v - min_v}",
        option_a=f"A. {max_v + min_v}", option_b=f"B. {min_v}",
        option_c=f"C. {max_v}", option_d=f"D. {max_v - min_v}",
        semantic_hash="UD_MINMAX_BBT"
    )

# Dạng 11: Tìm Min/Max của hàm số trên một khoảng, đoạn
def gen_ud_11_minmax_doan():
    a = random.randint(1, 3)
    content = f"Giá trị nhỏ nhất của hàm số $y = x^3 - 3x + {a}$ trên đoạn $[0; 2]$ bằng:"
    ans = a - 2
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"A. {ans}",
        option_a=f"A. {ans}", option_b=f"B. {a}",
        option_c=f"C. {a + 2}", option_d=f"D. {a - 1}",
        semantic_hash="UD_MINMAX_DOAN"
    )

# Dạng 12: Bài toán thực tế ứng dụng Min/Max
def gen_ud_12_thuc_te_minmax():
    L = random.choice([20, 40, 60])
    s_max = (L // 4) ** 2
    content = f" Dùng một sợi dây thép dài {L}m uốn thành hình chữ nhật. Diện tích lớn nhất của hình chữ nhật tạo thành là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"C. {s_max} $m^2$",
        option_a=f"A. {s_max // 2} $m^2$", option_b=f"B. {L} $m^2$",
        option_c=f"C. {s_max} $m^2$", option_d=f"D. {s_max * 2} $m^2$",
        semantic_hash="UD_THUCTE_MINMAX"
    )

# Dạng 13: Bài toán hàm hợp liên quan đến Min/Max
def gen_ud_13_ham_hop_minmax():
    content = "Cho hàm số $y = f(x)$ có $\\max_{[-2; 2]} f(x) = 5$. Giá trị lớn nhất của hàm số $g(x) = f(x - 1) + 2$ trên đoạn $[-1; 3]$ là:"
    return Question(
        concept_code="HAM_SO", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="B. 7",
        option_a="A. 5", option_b="B. 7", option_c="C. 8", option_d="D. 3",
        semantic_hash="UD_HAMHOP_MINMAX"
    )

# Dạng 14: Sử dụng đồ thị hoặc BBT xác định đường tiệm cận
def gen_ud_14_tiemcan_bbt():
    x0, y0 = random.randint(1, 3), random.randint(-2, 2)
    content = f"Cho hàm số $y=f(x)$ có $\\lim_{{x \\to {x0}^+}} f(x) = +\\infty$ và $\\lim_{{x \\to +\\infty}} f(x) = {y0}$. Đồ thị hàm số có các đường tiệm cận là:"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. TCĐ: $x = {x0}$, TCN: $y = {y0}$",
        option_a=f"A. TCĐ: $x = {x0}$, TCN: $y = {y0}$",
        option_b=f"B. TCĐ: $y = {x0}$, TCN: $x = {y0}$",
        option_c=f"C. TCĐ: $x = {y0}$, TCN: $y = {x0}$",
        option_d="D. Không có tiệm cận",
        semantic_hash="UD_TIEMCAN_BBT"
    )

# Dạng 15: Tìm đường tiệm cận của đồ thị hàm số
def gen_ud_15_tim_tiem_can():
    a, b = random.randint(1, 4), random.choice([-3, -1, 1, 3])
    content = f"Tiệm cận đứng của đồ thị hàm số $y = \\frac{{{a}x + 1}}{{x - {b}}}$ là đường thẳng:"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"B. $x = {b}$",
        option_a=f"A. $y = {a}$", option_b=f"B. $x = {b}$",
        option_c=f"C. $y = {b}$", option_d=f"D. $x = {a}$",
        semantic_hash="UD_TIM_TIEMCAN"
    )

# Dạng 16: Tiệm cận có chứa tham số
def gen_ud_16_tiemcan_thamso():
    m = random.randint(1, 5)
    content = f"Tìm $m$ để đồ thị hàm số $y = \\frac{{2x + 1}}{{x - m}}$ có tiệm cận đứng đi qua điểm $A({m}; 0)$."
    return Question(
        concept_code="HAM_SO", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="A. Đúng với mọi $m \\neq -\\frac{1}{2}$",
        option_a="A. Đúng với mọi $m \\neq -\\frac{1}{2}$",
        option_b="B. $m = 0$",
        option_c="C. $m = 1$",
        option_d="D. Không có giá trị $m$",
        semantic_hash="UD_TIEMCAN_THAMSO"
    )

# Dạng 17: Bài toán thực tế ứng dụng đường tiệm cận
def gen_ud_17_thuc_te_tiem_can():
    content = "Chi phí trung bình (triệu đồng) để sản xuất $x$ sản phẩm được cho bởi $C(x) = \\frac{10x + 50}{x}$. Khi số lượng sản phẩm $x$ rất lớn, chi phí trung bình tiến dần về bao nhiêu?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. 10 triệu đồng",
        option_a="A. 50 triệu đồng", option_b="B. 10 triệu đồng",
        option_c="C. 0 triệu đồng", option_d="D. 5 triệu đồng",
        semantic_hash="UD_THUCTE_TIEMCAN"
    )

# Dạng 18: Nhận dạng đồ thị hàm số
def gen_ud_18_nhan_dang_do_thi():
    a = random.choice([-1, 1])
    hinh_dang = "úp xuống (a < 0)" if a == -1 else "ngửa lên (a > 0)"
    content = f"Cho đồ thị hàm số bậc ba $y = ax^3 + bx^2 + cx + d$ có nét cuối đi xuống phía dưới. Khẳng định nào đúng về hệ số $a$?"
    return Question(
        concept_code="HAM_SO", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. $a < 0$",
        option_a="A. $a < 0$", option_b="B. $a > 0$",
        option_c="C. $a = 0$", option_d="D. Không xác định được",
        semantic_hash="UD_NHANDANG_DOTHI"
    )

# Dạng 19: Khảo sát sự biến thiên và vẽ đồ thị / Vận dụng giải quyết vấn đề thực tiễn
def gen_ud_19_vdc_thuc_tien_dothi():
    content = "Một mô hình dự báo dân số $P(t) = \\frac{50t + 100}{t + 2}$ (triệu người) với $t \\ge 0$ là số năm. Khẳng định nào sau đây SAI về sự phát triển dân số?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. Dân số giảm dần về 0 khi t tăng lên rất lớn",
        option_a="A. Dân số ban đầu (t=0) là 50 triệu người",
        option_b="B. Dân số luôn tăng theo thời gian",
        option_c="C. Dân số không vượt quá 50 triệu người về lâu dài",
        option_d="D. Dân số giảm dần về 0 khi t tăng lên rất lớn",
        semantic_hash="UD_VDC_THUCTIEN_DOTHI"
    )

# ==============================================================================
# BỔ SUNG CHƯƠNG: VECTƠ VÀ HỆ TRỤC TỌA ĐỘ TRONG KHÔNG GIAN
# ==============================================================================

# Dạng 1: Vectơ trong không gian là gì? Các yếu tố của vectơ
def gen_vec_1_khai_niem():
    content = "Trong không gian, cho hình hộp $ABCD.A'B'C'D'$. Vectơ nào sau đây bằng vectơ $\\vec{{AB}}$?"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. $\\vec{D'C'}$",
        option_a="A. $\\vec{D'C'}$", option_b="B. $\\vec{C'D'}$",
        option_c="C. $\\vec{BA}$", option_d="D. $\\vec{A'D'}$",
        semantic_hash="VEC_KHAI_NIEM_YEU_TO"
    )

# Dạng 2: Cách chứng minh, phân tích các vectơ
def gen_vec_2_phan_tich():
    content = "Cho tứ diện $ABCD$. Gọi $M$ là trung điểm của $BC$. Phân tích vectơ $\\vec{AM}$ theo hai vectơ $\\vec{AB}$ và $\\vec{AC}$."
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. $\\vec{AM} = \\frac{1}{2}\\vec{AB} + \\frac{1}{2}\\vec{AC}$",
        option_a="A. $\\vec{AM} = \\vec{AB} + \\vec{AC}$",
        option_b="B. $\\vec{AM} = \\frac{1}{2}\\vec{AB} + \\frac{1}{2}\\vec{AC}$",
        option_c="C. $\\vec{AM} = \\vec{AB} - \\vec{AC}$",
        option_d="D. $\\vec{AM} = \\frac{1}{2}\\vec{AB} - \\frac{1}{2}\\vec{AC}$",
        semantic_hash="VEC_PHAN_TICH_CHUNG_MINH"
    )

# Dạng 3: Xác định góc giữa hai vectơ và tính tích vô hướng của hai vectơ
def gen_vec_3_goc_tich_vo_huong():
    a = random.choice([2, 4, 6])
    content = f"Cho hình lập phương $ABCD.A'B'C'D'$ có cạnh bằng {a}. Tính tích vô hướng $\\vec{{AB}} \\cdot \\vec{{AD}}$."
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="C. 0",
        option_a=f"A. {a*a}", option_b=f"B. {-a*a}",
        option_c="C. 0", option_d=f"D. {a}",
        semantic_hash="VEC_GOC_TICH_VO_HUONG"
    )

# Dạng 4: Các bài toán ứng dụng vectơ trong thực tế (Hình học không gian thuần túy)
def gen_vec_4_thuc_te_co_dien():
    f1 = random.randint(100, 300)
    f2 = f1
    content = f"Hai lực $\\vec{{F_1}}$ và $\\vec{{F_2}}$ cùng tác dụng vào một vật tại điểm $O$ và tạo với nhau một góc $60^\\circ$. Biết $|\\vec{{F_1}}| = |\\vec{{F_2}}| = {f1}\\text{{ N}}$. Độ lớn của hợp lực $\\vec{{F}} = \\vec{{F_1}} + \\vec{{F_2}}$ là:"
    f_res = round(f1 * math.sqrt(3), 1)
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"A. {f_res} N",
        option_a=f"A. {f_res} N", option_b=f"B. {f1 * 2} N",
        option_c=f"C. {f1} N", option_d=f"D. {round(f1 * math.sqrt(2), 1)} N",
        semantic_hash="VEC_THUC_TE_CO_DIEN"
    )

# Dạng 5: Xác định tọa độ điểm, tọa độ vectơ
def gen_vec_5_xac_dinh_toa_do():
    x, y, z = random.randint(-4, 4), random.randint(-4, 4), random.randint(-4, 4)
    content = f"Trong không gian $Oxyz$, cho điểm $M({x}; {y}; {z})$. Tọa độ của vectơ $\\vec{{OM}}$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"D. $({x}; {y}; {z})$",
        option_a=f"A. $({-x}; {-y}; {-z})$", option_b=f"B. $({y}; {x}; {z})$",
        option_c=f"C. $({z}; {y}; {x})$", option_d=f"D. $({x}; {y}; {z})$",
        semantic_hash="VEC_XAC_DINH_TOA_DO"
    )

# Dạng 6: Xác định tọa độ các phép toán vectơ, tọa độ điểm, độ dài đoạn thẳng
def gen_vec_6_phep_toan_do_dai():
    x1, y1, z1 = random.randint(-2, 2), random.randint(-2, 2), random.randint(-2, 2)
    x2, y2, z2 = x1 + 3, y1 + 0, z1 + 4
    content = f"Trong không gian $Oxyz$, cho $A({x1}; {y1}; {z1})$ và $B({x2}; {y2}; {z2})$. Độ dài đoạn thẳng $AB$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. 5",
        option_a="A. 25", option_b="B. 5",
        option_c="C. 7", option_d="D. $\\sqrt{7}$",
        semantic_hash="VEC_PHEP_TOAN_DO_DAI"
    )

# Dạng 7: Tích vô hướng và ứng dụng tọa độ Oxyz
def gen_vec_7_tich_vo_huong_oxyz():
    x1, y1, z1 = random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)
    x2, y2, z2 = random.randint(-3, -1), random.randint(1, 3), 0
    dot = x1*x2 + y1*y2 + z1*z2
    content = f"Trong không gian $Oxyz$, cho $\\vec{{a}} = ({x1}; {y1}; {z1})$ và $\\vec{{b}} = ({x2}; {y2}; {z2})$. Tích vô hướng $\\vec{{a}} \\cdot \\vec{{b}}$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. {dot}",
        option_a=f"A. {dot}", option_b=f"B. {dot + 2}",
        option_c=f"C. {dot - 3}", option_d=f"D. {-dot}",
        semantic_hash="VEC_TICH_VO_HUONG_OXYZ"
    )

# Dạng 8: Vận dụng tọa độ của vectơ để giải các bài toán thực tế Oxyz
def gen_vec_8_thuc_te_oxyz_vdc():
    vx, vy, vz = 150, 200, 100
    t = 2
    d = round(t * math.sqrt(vx**2 + vy**2 + vz**2), 1)
    content = f"Một ra-da phát hiện một thiết bị bay di chuyển với vận tốc không đổi $\\vec{{v}} = ({vx}; {vy}; {vz})$ (km/h) trong hệ tọa độ $Oxyz$. Sau {t} giờ kể từ mốc xuất phát tại $O(0;0;0)$, khoảng cách từ thiết bị bay đến trạm ra-da $O$ là bao nhiêu km?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer=f"C. {d} km",
        option_a=f"A. {round(d*1.2, 1)} km", option_b=f"B. {round(d*0.8, 1)} km",
        option_c=f"C. {d} km", option_d=f"D. {round(d + 50, 1)} km",
        semantic_hash="VEC_THUC_TE_OXYZ_VDC"
    )

# ==============================================================================
# BỔ SUNG CHƯƠNG: CÁC SỐ ĐẶC TRƯNG ĐO MỨC ĐỘ PHÂN TÁN (MẪU SỐ LIỆU GHÉP NHÓM)
# ==============================================================================

# Dạng 1: Khoảng biến thiên và ý nghĩa
def gen_stat_1_khoang_bien_thien():
    start = random.randint(10, 20)
    step = random.choice([5, 10])
    k = 4
    end = start + k * step
    R = end - start
    content = f"Một mẫu số liệu ghép nhóm có nhóm đầu tiên là $[{start}; {start+step})$ và nhóm cuối cùng là $[{end-step}; {end})$. Khoảng biến thiên $R$ của mẫu số liệu ghép nhóm này là:"
    return Question(
        concept_code="THONG_KE", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"B. {R}",
        option_a=f"A. {R - step}", option_b=f"B. {R}",
        option_c=f"C. {end}", option_d=f"D. {start}",
        semantic_hash="STAT_KHOANG_BIEN_THIEN"
    )

# Dạng 2: Khoảng tứ phân vị và ý nghĩa
def gen_stat_2_khoang_tu_phan_vi():
    q1, q3 = random.randint(15, 25), random.randint(35, 45)
    delta_q = q3 - q1
    content = f"Một mẫu số liệu ghép nhóm sau khi tính toán có tứ phân vị thứ nhất $Q_1 = {q1}$ và tứ phân vị thứ ba $Q_3 = {q3}$. Khoảng tứ phân vị $\\Delta_Q$ của mẫu số liệu là:"
    return Question(
        concept_code="THONG_KE", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. {delta_q}",
        option_a=f"A. {delta_q}", option_b=f"B. {q1 + q3}",
        option_c=f"C. {q3}", option_d=f"D. {delta_q / 2}",
        semantic_hash="STAT_KHOANG_TU_PHAN_VI"
    )

# Dạng 3: Tính phương sai, độ lệch chuẩn ghép nhóm và vận dụng đo mức độ rủi ro
def gen_stat_3_phuong_sai_rui_ro_vdc():
    content = "Hai quỹ đầu tư cổ phiếu A và B có lợi nhuận trung bình năm như nhau. Độ lệch chuẩn lợi nhuận của quỹ A là $s_A = 2.8\\%$ và của quỹ B là $s_B = 5.4\\%$. Khẳng định nào sau đây đúng về mức độ rủi ro đầu tư?"
    return Question(
        concept_code="THONG_KE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. Quỹ B có mức độ rủi ro cao hơn do có độ lệch chuẩn lớn hơn.",
        option_a="A. Quỹ A có mức độ rủi ro cao hơn do độ lệch chuẩn nhỏ hơn.",
        option_b="B. Hai quỹ có mức độ rủi ro bằng nhau vì lợi nhuận trung bình như nhau.",
        option_c="C. Không thể so sánh rủi ro dựa trên độ lệch chuẩn.",
        option_d="D. Quỹ B có mức độ rủi ro cao hơn do có độ lệch chuẩn lớn hơn.",
        semantic_hash="STAT_PHUONG_SAI_RUI_RO_VDC"
    )

# ==============================================================================
# BỔ SUNG CHƯƠNG: PHƯƠNG PHÁP TỌA ĐỘ TRONG KHÔNG GIAN (27 DẠNG CHUẨN)
# ==============================================================================

# --- A. MẶT PHẲNG (9 DẠNG) ---

# Dạng 1: Xác định yếu tố cơ bản liên quan đến mặt phẳng
def gen_geo_1_yeu_to_mat_phang():
    A, B, C, D = random.randint(1, 3), random.randint(-3, -1), random.randint(1, 4), random.randint(-5, 5)
    content = f"Trong không gian $Oxyz$, cho mặt phẳng $(P): {A}x {B:+d}y {C:+d}z {D:+d} = 0$. Một vectơ pháp tuyến của $(P)$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. $\\vec{{n}} = ({A}; {B}; {C})$",
        option_a=f"A. $\\vec{{n}} = ({A}; {B}; {C})$", option_b=f"B. $\\vec{{n}} = ({-A}; {B}; {C})$",
        option_c=f"C. $\\vec{{n}} = ({A}; {C}; {D})$", option_d=f"D. $\\vec{{n}} = ({B}; {A}; {C})$",
        semantic_hash="GEO_YEU_TO_MAT_PHANG"
    )

# Dạng 2: Viết ptmpp đi qua 1 điểm và có 1 VPT
def gen_geo_2_mp_1diem_1vpt():
    x0, y0, z0 = random.randint(-2, 2), random.randint(-2, 2), random.randint(-2, 2)
    A, B, C = random.randint(1, 3), random.randint(1, 3), random.randint(-3, -1)
    D = -(A*x0 + B*y0 + C*z0)
    content = f"Viết phương trình mặt phẳng $(P)$ đi qua $M({x0}; {y0}; {z0})$ và có VCPT $\\vec{{n}} = ({A}; {B}; {C})$."
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"B. ${A}x {B:+d}y {C:+d}z {D:+d} = 0$",
        option_a=f"A. ${A}x {B:+d}y {C:+d}z {-D:+d} = 0$", option_b=f"B. ${A}x {B:+d}y {C:+d}z {D:+d} = 0$",
        option_c=f"C. ${x0}x {y0:+d}y {z0:+d}z = 0$", option_d=f"D. ${A}x {-B:+d}y {C:+d}z {D:+d} = 0$",
        semantic_hash="GEO_MP_1DIEM_1VPT"
    )

# Dạng 3: Viết ptmpp đi qua 1 điểm và có cặp VCP
def gen_geo_3_mp_1diem_cap_vcp():
    content = "Viết phương trình mặt phẳng $(P)$ đi qua $O(0;0;0)$ và song song với cả hai vectơ $\\vec{u} = (1; 0; 0)$ và $\\vec{v} = (0; 1; 0)$."
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="C. $z = 0$",
        option_a="A. $x = 0$", option_b="B. $y = 0$", option_c="C. $z = 0$", option_d="D. $x + y = 0$",
        semantic_hash="GEO_MP_1DIEM_CAP_VCP"
    )

# Dạng 4: Viết ptmpp đi qua 3 điểm không thẳng hàng
def gen_geo_4_mp_qua_3_diem():
    a, b, c = random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)
    content = f"Trong không gian $Oxyz$, mặt phẳng đi qua ba điểm $A({a}; 0; 0)$, $B(0; {b}; 0)$, $C(0; 0; {c})$ có phương trình là:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"A. $\\frac{{x}}{{{a}}} + \\frac{{y}}{{{b}}} + \\frac{{z}}{{{c}}} = 1$",
        option_a=f"A. $\\frac{{x}}{{{a}}} + \\frac{{y}}{{{b}}} + \\frac{{z}}{{{c}}} = 1$",
        option_b=f"B. $\\frac{{x}}{{{a}}} + \\frac{{y}}{{{b}}} + \\frac{{z}}{{{c}}} = 0$",
        option_c=f"C. ${a}x + {b}y + {c}z = 1$",
        option_d=f"D. $\\frac{{x}}{{{a}}} - \\frac{{y}}{{{b}}} + \\frac{{z}}{{{c}}} = 1$",
        semantic_hash="GEO_MP_QUA_3_DIEM"
    )

# Dạng 5: Viết ptmpp trung trực của đoạn thẳng
def gen_geo_5_mp_trung_truc():
    x1, y1, z1 = 0, 0, 0
    x2, y2, z2 = 2, 4, 6
    # Trung điểm I(1,2,3), AB = (2,4,6) => ptm: 2(x-1)+4(y-2)+6(z-3)=0 <=> x + 2y + 3z - 14 = 0
    content = f"Phương trình mặt phẳng trung trực của đoạn thẳng $AB$ với $A(0;0;0)$ và $B(2;4;6)$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="D. $x + 2y + 3z - 14 = 0$",
        option_a="A. $x + 2y + 3z = 0$", option_b="B. $2x + 4y + 6z + 14 = 0$",
        option_c="C. $x + 2y + 3z + 14 = 0$", option_d="D. $x + 2y + 3z - 14 = 0$",
        semantic_hash="GEO_MP_TRUNG_TRUC"
    )

# Dạng 6: Viết ptmpp qua 1 điểm song song mặt phẳng khác
def gen_geo_6_mp_song_song_mp():
    D2 = random.randint(6, 10)
    content = f"Phương trình mặt phẳng $(P)$ đi qua $O(0;0;0)$ và song song với mặt phẳng $(Q): 2x - 3y + z + {D2} = 0$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. $2x - 3y + z = 0$",
        option_a="A. $2x - 3y + z = 0$", option_b="B. $2x - 3y + z + 5 = 0$",
        option_c="C. $x + y + z = 0$", option_d="D. $2x + 3y + z = 0$",
        semantic_hash="GEO_MP_SONG_SONG_MP"
    )

# Dạng 7: Khoảng cách từ một điểm đến một mặt phẳng
def gen_geo_7_khoang_cach_diem_mp():
    # P: x + 2y - 2z - 9 = 0, M(1,2,3) => d = |1 + 4 - 6 - 9| / 3 = |-10|/3 = 10/3
    content = "Tính khoảng cách $d$ từ điểm $M(1; 2; 3)$ đến mặt phẳng $(P): x + 2y - 2z - 9 = 0$."
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. $d = \\frac{10}{3}$",
        option_a="A. $d = 10$", option_b="B. $d = \\frac{10}{3}$",
        option_c="C. $d = 3$", option_d="D. $d = \\frac{4}{3}$",
        semantic_hash="GEO_KHOANG_CACH_DIEM_MP"
    )

# Dạng 8: Vị trí tương đối giữa hai mặt phẳng
def gen_geo_8_vttd_hai_mp():
    D = random.randint(1, 5)
    content = f"Trong không gian $Oxyz$, vị trí tương đối giữa $(P): x + y + z + 1 = 0$ và $(Q): 2x + 2y + 2z + {D*2 + 2} = 0$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="C. Song song với nhau",
        option_a="A. Cắt nhau", option_b="B. Trùng nhau",
        option_c="C. Song song với nhau", option_d="D. Vuông góc với nhau",
        semantic_hash="GEO_VTTD_HAI_MP"
    )

# Dạng 9: Vận dụng kiến thức mặt phẳng vào giải quyết bài toán thực tế
def gen_geo_9_thuc_te_mat_phang_vdc():
    content = "Một mái nhà nghiêng được thiết kế nằm trên mặt phẳng $(P): 3x + 4y + 12z - 24 = 0$ trong hệ trục tọa độ $Oxyz$ (đơn vị: mét). Khoảng cách từ vị trí cảm biến mưa $O(0;0;0)$ đến mái nhà là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="A. $\\frac{24}{13}$ m",
        option_a="A. $\\frac{24}{13}$ m", option_b="B. $2$ m",
        option_c="C. $\\frac{24}{5}$ m", option_d="D. $12$ m",
        semantic_hash="GEO_THUC_TE_MAT_PHANG_VDC"
    )


# --- B. ĐƯỜNG THẲNG (8 DẠNG) ---

# Dạng 10: Xác định các yếu tố cơ bản của đường thẳng
def gen_geo_10_yeu_to_duong_thang():
    x0, y0, z0 = random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)
    u1, u2, u3 = random.randint(1, 3), random.randint(-3, -1), random.randint(1, 4)
    content = f"Đường thẳng $d: \\frac{{x - {x0}}}{{{u1}}} = \\frac{{y - {y0}}}{{{u2}}} = \\frac{{z - {z0}}}{{{u3}}}$ có một vectơ chỉ phương là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"C. $\\vec{{u}} = ({u1}; {u2}; {u3})$",
        option_a=f"A. $\\vec{{u}} = ({x0}; {y0}; {z0})$", option_b=f"B. $\\vec{{u}} = ({-x0}; {-y0}; {-z0})$",
        option_c=f"C. $\\vec{{u}} = ({u1}; {u2}; {u3})$", option_d=f"D. $\\vec{{u}} = ({-u1}; {u2}; {u3})$",
        semantic_hash="GEO_YEU_TO_DUONG_THANG"
    )

# Dạng 11: Viết ptdt đi qua 1 điểm và có 1 VCP
def gen_geo_11_dt_1diem_1vcp():
    x0, y0, z0 = random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)
    content = f"Phương trình tham số của đường thẳng $d$ đi qua $A({x0}; {y0}; {z0})$ và có VCP $\\vec{{u}} = (1; 2; 3)$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. $\\begin{{cases}} x = {x0} + t \\\\ y = {y0} + 2t \\\\ z = {z0} + 3t \\end{{cases}}$",
        option_a=f"A. $\\begin{{cases}} x = {x0} + t \\\\ y = {y0} + 2t \\\\ z = {z0} + 3t \\end{{cases}}$",
        option_b=f"B. $\\begin{{cases}} x = 1 + {x0}t \\\\ y = 2 + {y0}t \\\\ z = 3 + {z0}t \\end{{cases}}$",
        option_c=f"C. $\\begin{{cases}} x = {x0} - t \\\\ y = {y0} + 2t \\\\ z = {z0} - 3t \\end{{cases}}$",
        option_d=f"D. $\\begin{{cases}} x = t \\\\ y = 2t \\\\ z = 3t \\end{{cases}}$",
        semantic_hash="GEO_DT_1DIEM_1VCP"
    )

# Dạng 12: Viết ptdt đi qua 2 điểm
def gen_geo_12_dt_qua_2_diem():
    content = "Viết phương trình chính danh của đường thẳng đi qua $A(1; 2; 3)$ và $B(2; 4; 6)$."
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. $\\frac{x - 1}{1} = \\frac{y - 2}{2} = \\frac{z - 3}{3}$",
        option_a="A. $\\frac{x - 2}{1} = \\frac{y - 4}{2} = \\frac{z - 6}{3}$",
        option_b="B. $\\frac{x - 1}{1} = \\frac{y - 2}{2} = \\frac{z - 3}{3}$",
        option_c="C. $\\frac{x + 1}{1} = \\frac{y + 2}{2} = \\frac{z + 3}{3}$",
        option_d="D. $\\frac{x - 1}{2} = \\frac{y - 2}{4} = \\frac{z - 3}{6}$",
        semantic_hash="GEO_DT_QUA_2_DIEM"
    )

# Dạng 13: Viết ptdt đi qua 1 điểm và vuông góc với mặt phẳng
def gen_geo_13_dt_vuong_goc_mp():
    content = "Đường thẳng $d$ đi qua $M(1; 0; -1)$ và vuông góc với mặt phẳng $(P): 2x - y + 3z + 1 = 0$ có VCP là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="D. $\\vec{u} = (2; -1; 3)$",
        option_a="A. $\\vec{u} = (1; 0; -1)$", option_b="B. $\\vec{u} = (-2; -1; 3)$",
        option_c="C. $\\vec{u} = (2; 1; 3)$", option_d="D. $\\vec{u} = (2; -1; 3)$",
        semantic_hash="GEO_DT_VUONG_GOC_MP"
    )

# Dạng 14: Xác định ptdt khi biết yếu tố song song
def gen_geo_14_dt_song_song_dt():
    content = "Viết phương trình đường thẳng $d$ đi qua $O(0;0;0)$ và song song với đường thẳng $\\Delta: \\frac{x - 1}{2} = \\frac{y + 2}{-3} = \\frac{z}{1}$."
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="A. $\\frac{x}{2} = \\frac{y}{-3} = \\frac{z}{1}$",
        option_a="A. $\\frac{x}{2} = \\frac{y}{-3} = \\frac{z}{1}$",
        option_b="B. $\\frac{x}{1} = \\frac{y}{-2} = \\frac{z}{1}$",
        option_c="C. $\\frac{x-1}{2} = \\frac{y+2}{-3} = \\frac{z}{1}$",
        option_d="D. $\\frac{x}{-2} = \\frac{y}{-3} = \\frac{z}{1}$",
        semantic_hash="GEO_DT_SONG_SONG_DT"
    )

# Dạng 15: Vị trí tương đối của hai đường thẳng
def gen_geo_15_vttd_hai_dt():
    content = "Trong không gian $Oxyz$, hai đường thẳng $d_1: \\frac{x-1}{1} = \\frac{y}{2} = \\frac{z}{1}$ và $d_2: \\frac{x-2}{1} = \\frac{y-2}{2} = \\frac{z-1}{1}$ có vị trí tương đối là:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. Song song với nhau",
        option_a="A. Cắt nhau", option_b="B. Song song với nhau",
        option_c="C. Chéo nhau", option_d="D. Trùng nhau",
        semantic_hash="GEO_VTTD_HAI_DT"
    )

# Dạng 16: Vận dụng ptdt vào giải quyết bài toán thực tế
def gen_geo_16_thuc_te_duong_thang_vdc():
    content = "Một tia laser được phát ra từ vị trí $A(1; 2; 3)$ theo hướng đường thẳng $d: \\frac{x-1}{1} = \\frac{y-2}{2} = \\frac{z-3}{-2}$ hướng về mặt đất $z = 0$. Tọa độ điểm vệt sáng laser chạm mặt đất là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="C. $(\\frac{5}{2}; 5; 0)$",
        option_a="A. $(1; 2; 0)$", option_b="B. $(2; 4; 0)$",
        option_c="C. $(\\frac{5}{2}; 5; 0)$", option_d="D. $(0; 0; 0)$",
        semantic_hash="GEO_THUC_TE_DUONG_THANG_VDC"
    )


# --- C. GÓC TRONG KHÔNG GIAN (4 DẠNG) ---

# Dạng 17: Góc giữa hai đường thẳng
def gen_geo_17_goc_hai_dt():
    content = "Góc giữa hai đường thẳng $d_1$ có VCP $\\vec{u_1} = (1; 0; 0)$ và $d_2$ có VCP $\\vec{u_2} = (0; 1; 0)$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. $90^\\circ$",
        option_a="A. $90^\\circ$", option_b="B. $0^\\circ$",
        option_c="C. $45^\\circ$", option_d="D. $180^\\circ$",
        semantic_hash="GEO_GOC_HAI_DT"
    )

# Dạng 18: Góc giữa đường thẳng và mặt phẳng
def gen_geo_18_goc_dt_va_mp():
    content = "Cho đường thẳng $d$ vuông góc với mặt phẳng $(P)$. Góc giữa đường thẳng $d$ và mặt phẳng $(P)$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="C. $90^\\circ$",
        option_a="A. $0^\\circ$", option_b="B. $45^\\circ$",
        option_c="C. $90^\\circ$", option_d="D. $60^\\circ$",
        semantic_hash="GEO_GOC_DT_VA_MP"
    )

# Dạng 19: Góc giữa hai mặt phẳng
def gen_geo_19_goc_hai_mp():
    content = "Góc giữa mặt phẳng $(Oxy)$ và mặt phẳng $(Oxz)$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="B. $90^\\circ$",
        option_a="A. $0^\\circ$", option_b="B. $90^\\circ$",
        option_c="C. $45^\\circ$", option_d="D. $60^\\circ$",
        semantic_hash="GEO_GOC_HAI_MP"
    )

# Dạng 20: Vận dụng công thức tính góc vào bài toán thực tế
def gen_geo_20_thuc_te_goc_vdc():
    content = "Hai ống dẫn nước trong nhà máy được lắp đặt theo 2 đường thẳng có VCP $\\vec{u_1} = (1; 1; 0)$ và $\\vec{u_2} = (0; 1; 1)$. Góc giữa hai ống dẫn nước đó bằng:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. $60^\\circ$",
        option_a="A. $30^\\circ$", option_b="B. $45^\\circ$",
        option_c="C. $90^\\circ$", option_d="D. $60^\\circ$",
        semantic_hash="GEO_THUC_TE_GOC_VDC"
    )


# --- D. MẶT CẦU (7 DẠNG) ---

# Dạng 21: Xác định các yếu tố cơ bản của mặt cầu
def gen_geo_21_yeu_to_mat_cau():
    a, b, c, R2 = 1, -2, 3, 16
    content = f"Mặt cầu $(S): (x - 1)^2 + (y + 2)^2 + (z - 3)^2 = 16$ có tâm $I$ và bán kính $R$ lần lượt là:"
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="A. $I(1; -2; 3), R = 4$",
        option_a="A. $I(1; -2; 3), R = 4$", option_b="B. $I(-1; 2; -3), R = 16$",
        option_c="C. $I(1; -2; 3), R = 16$", option_d="D. $I(-1; 2; -3), R = 4$",
        semantic_hash="GEO_YEU_TO_MAT_CAU"
    )

# Dạng 22: Viết ptmc có tâm và bán kính cho trước
def gen_geo_22_mc_tam_ban_kinh():
    x0, y0, z0, R = 2, 0, -1, 3
    content = f"Viết phương trình mặt cầu có tâm $I(2; 0; -1)$ và bán kính $R = 3$."
    return Question(
        concept_code="OXYZ", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="B. $(x - 2)^2 + y^2 + (z + 1)^2 = 9$",
        option_a="A. $(x - 2)^2 + y^2 + (z - 1)^2 = 9$",
        option_b="B. $(x - 2)^2 + y^2 + (z + 1)^2 = 9$",
        option_c="C. $(x + 2)^2 + y^2 + (z - 1)^2 = 3$",
        option_d="D. $(x - 2)^2 + y^2 + (z + 1)^2 = 3$",
        semantic_hash="GEO_MC_TAM_BAN_KINH"
    )

# Dạng 23: Viết ptmc có tâm và đi qua 1 điểm
def gen_geo_23_mc_tam_qua_1_diem():
    content = "Mặt cầu tâm $O(0;0;0)$ và đi qua điểm $A(1; 2; 2)$ có phương trình là:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="C. $x^2 + y^2 + z^2 = 9$",
        option_a="A. $x^2 + y^2 + z^2 = 3$", option_b="B. $x^2 + y^2 + z^2 = 5$",
        option_c="C. $x^2 + y^2 + z^2 = 9$", option_d="D. $(x-1)^2 + (y-2)^2 + (z-2)^2 = 9$",
        semantic_hash="GEO_MC_TAM_QUA_1_DIEM"
    )

# Dạng 24: Viết ptmc có đường kính cho trước
def gen_geo_24_mc_duong_kinh():
    content = "Phương trình mặt cầu đường kính $AB$ với $A(1; 0; 0)$ và $B(-1; 0; 0)$ là:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="A. $x^2 + y^2 + z^2 = 1$",
        option_a="A. $x^2 + y^2 + z^2 = 1$", option_b="B. $x^2 + y^2 + z^2 = 4$",
        option_c="C. $(x-1)^2 + y^2 + z^2 = 1$", option_d="D. $x^2 + y^2 + z^2 = 2$",
        semantic_hash="GEO_MC_DUONG_KINH"
    )

# Dạng 25: Viết ptmc đi qua 4 điểm không đồng phẳng
def gen_geo_25_mc_qua_4_diem_vdc():
    content = "Mặt cầu ngoại tiếp tứ diện $OABC$ với $O(0;0;0), A(2;0;0), B(0;4;0), C(0;0;4)$ có bán kính $R$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. $R = 3$",
        option_a="A. $R = 6$", option_b="B. $R = 9$",
        option_c="C. $R = \\sqrt{6}$", option_d="D. $R = 3$",
        semantic_hash="GEO_MC_QUA_4_DIEM_VDC"
    )

# Dạng 26: Viết ptmc có tâm và tiếp xúc với một mặt phẳng
def gen_geo_26_mc_tam_tiep_xuc_mp():
    content = "Phương trình mặt cầu tâm $I(1; 1; 1)$ và tiếp xúc với mặt phẳng $(P): x + 2y - 2z + 8 = 0$ có bán kính $R$ bằng:"
    return Question(
        concept_code="OXYZ", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. $R = 3$",
        option_a="A. $R = 9$", option_b="B. $R = 3$",
        option_c="C. $R = 1$", option_d="D. $R = 27$",
        semantic_hash="GEO_MC_TAM_TIEP_XUC_MP"
    )

# Dạng 27: Vận dụng phương trình mặt cầu vào giải quyết bài toán thực tiện
def gen_geo_27_thuc_te_mat_cau_vdc():
    content = "Một vòm trạm vũ trụ dạng mặt cầu $(S): x^2 + y^2 + z^2 = 100$ (đơn vị: mét). Một tàu không gian tại $M(10; 10; 10)$ di chuyển theo hướng về gốc tọa độ $O$. Khoảng cách từ tàu đến vòm trạm khi chạm tới vòm là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="A. $10\\sqrt{3} - 10$ m",
        option_a="A. $10\\sqrt{3} - 10$ m", option_b="B. $10$ m",
        option_c="C. $10\\sqrt{3}$ m", option_d="D. $10\\sqrt{2} - 10$ m",
        semantic_hash="GEO_THUC_TE_MAT_CAU_VDC"
    )

# ==============================================================================
# BỔ SUNG CHƯƠNG: XÁC SUẤT CÓ ĐIỀU KIỆN (4 DẠNG CHUẨN)
# ==============================================================================

# Dạng 1: Tính xác suất có điều kiện (Định nghĩa & Công thức cơ bản)
def gen_prob_1_xac_suat_dieu_kien_co_ban():
    p_a = round(random.choice([0.4, 0.5, 0.6]), 1)
    p_ab = round(p_a * random.choice([0.3, 0.4, 0.5]), 2)
    ans = round(p_ab / p_a, 2)
    content = f"Cho hai biến cố $A$ và $B$ thỏa mãn $P(A) = {p_a}$ và $P(AB) = {p_ab}$. Tính xác suất có điều kiện $P(B|A)$."
    return Question(
        concept_code="XAC_SUAT", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. {ans}",
        option_a=f"A. {ans}", option_b=f"B. {round(p_a / p_ab, 2)}",
        option_c=f"C. {round(p_a + p_ab, 2)}", option_d=f"D. {round(p_a - p_ab, 2)}",
        semantic_hash="PROB_XAC_SUAT_DIEU_KIEN_CO_BAN"
    )

# Dạng 2: Tính xác suất có điều kiện bằng cách sử dụng sơ đồ hình cây
def gen_prob_2_so_do_hinh_cay():
    content = "Một hộp chứa 3 viên bi đỏ và 2 viên bi xanh. Lần thứ nhất lấy ngẫu nhiên 1 viên bi và không hoàn lại. Lần thứ hai lấy ngẫu nhiên 1 viên bi. Sử dụng sơ đồ hình cây, tính xác suất để lần thứ hai lấy được bi xanh biết lần thứ nhất đã lấy được bi đỏ."
    return Question(
        concept_code="XAC_SUAT", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="B. $\\frac{2}{4} = 0.5$",
        option_a="A. $\\frac{2}{5} = 0.4$", option_b="B. $\\frac{2}{4} = 0.5$",
        option_c="C. $\\frac{3}{4} = 0.75$", option_d="D. $\\frac{1}{4} = 0.25$",
        semantic_hash="PROB_SO_DO_HINH_CAY"
    )

# Dạng 3: Các bài toán liên quan đến công thức xác suất toàn phần
def gen_prob_3_xac_suat_toan_phan():
    ratio_x1 = random.choice([60, 70])
    ratio_x2 = 100 - ratio_x1
    p_x1 = ratio_x1 / 100
    p_x2 = ratio_x2 / 100
    
    # Tỷ lệ phế phẩm
    f1 = 0.01
    f2 = 0.02
    p_fe = round(p_x1 * f1 + p_x2 * f2, 4)
    
    content = f"Một nhà máy có hai xưởng X1 và X2 sản xuất với tỷ lệ sản lượng lần lượt là {ratio_x1}\\% và {ratio_x2}\\%. Tỷ lệ phế phẩm của xưởng X1 là 1\\%, xưởng X2 là 2\\%. Chọn ngẫu nhiên 1 sản phẩm của nhà máy, tính xác suất sản phẩm đó là phế phẩm."
    return Question(
        concept_code="XAC_SUAT", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"C. {p_fe}",
        option_a=f"A. {round(p_fe * 1.5, 4)}", option_b=f"B. {round(p_fe * 0.8, 4)}",
        option_c=f"C. {p_fe}", option_d=f"D. 0.03",
        semantic_hash="PROB_XAC_SUAT_TOAN_PHAN"
    )

# Dạng 4: Các bài toán liên quan đến công thức Bayes
def gen_prob_4_cong_thuc_bayes_vdc():
    content = "Tỷ lệ mắc bệnh X trong cộng đồng là 1\\%. Xét nghiệm chuẩn đoán bệnh X có độ chính xác 95\\% với người mắc bệnh (kết quả Dương tính) và 90\\% với người không mắc bệnh (kết quả Âm tính). Chọn ngẫu nhiên một người nhận kết quả Dương tính, tính xác suất thực sự người đó mắc bệnh X."
    # P(D) = 0.01, P(+|D) = 0.95, P(+|~D) = 0.10
    # P(+) = 0.01*0.95 + 0.99*0.10 = 0.0095 + 0.099 = 0.1085
    # P(D|+) = 0.0095 / 0.1085 ≈ 0.087558 (8.76%)
    return Question(
        concept_code="XAC_SUAT", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. Khoảng 8.76%",
        option_a="A. Khoảng 95.0%", option_b="B. Khoảng 50.0%",
        option_c="C. Khoảng 1.0%", option_d="D. Khoảng 8.76%",
        semantic_hash="PROB_CONG_THUC_BAYES_VDC"
    )

# ==============================================================================
# BỔ SUNG CHUYÊN ĐỀ: BÀI TOÁN THỰC TẾ LỚP 12 (11 DẠNG CHUẨN)
# ==============================================================================

# Dạng 1: Bài toán thực tế - Tính đơn điệu và cực trị của hàm số
def gen_app_1_thuc_te_don_dieu_cuc_tri():
    v0 = random.choice([20, 30, 40])
    content = f"Đạn pháo được bắn lên từ mặt đất theo chuyển động có phương trình độ cao $h(t) = {v0}t - 5t^2$ (mét), $t$ tính bằng giây. Vận tốc của đạn pháo đạt giá trị bằng $0$ m/s tại thời điểm nào?"
    t_ans = v0 // 10
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"B. $t = {t_ans}$ s",
        option_a=f"A. $t = {t_ans * 2}$ s", option_b=f"B. $t = {t_ans}$ s",
        option_c=f"C. $t = {t_ans + 1}$ s", option_d=f"D. $t = {t_ans // 2}$ s",
        semantic_hash="APP_THUC_TE_DON_DIEU_CUCTRI"
    )

# Dạng 2: Bài toán thực tế - Giá trị lớn nhất và giá trị nhỏ nhất của hàm số
def gen_app_2_thuc_te_min_max():
    L = random.choice([40, 80, 100])
    s_max = (L // 4) ** 2
    content = f"Một người nông dân muốn rào một khu đất hình chữ nhật dọc theo một bức tường thẳng có sẵn (không cần rào phía bức tường) bằng sợi dây dài {L} m. Diện tích lớn nhất của khu đất rào được là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer=f"A. {s_max} $m^2$",
        option_a=f"A. {s_max} $m^2$", option_b=f"B. {s_max // 2} $m^2$",
        option_c=f"C. {s_max + 50} $m^2$", option_d=f"D. {L * 10} $m^2$",
        semantic_hash="APP_THUC_TE_MIN_MAX"
    )

# Dạng 3: Bài toán thực tế - Đường tiệm cận của đồ thị hàm số
def gen_app_3_thuc_te_tiem_can():
    c0 = random.choice([10, 20, 30])
    k0 = random.choice([50, 100])
    content = f"Chi phí trung bình (nghìn đồng) để sản xuất $x$ sản phẩm tại một xưởng cơ khí được cho bởi hàm số $C(x) = \\frac{{{c0}x + {k0}}}{{x}}$. Khi số lượng sản phẩm $x$ tăng lên rất lớn, chi phí trung bình sản xuất 1 sản phẩm tiệm cận về giá trị nào?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"C. {c0} nghìn đồng",
        option_a=f"A. {k0} nghìn đồng", option_b=f"B. 0 nghìn đồng",
        option_c=f"C. {c0} nghìn đồng", option_d=f"D. {c0 + k0} nghìn đồng",
        semantic_hash="APP_THUC_TE_TIEM_CAN"
    )

# Dạng 4: Bài toán thực tế - Ứng dụng đạo hàm để giải quyết bài toán liên quan thực tiễn
def gen_app_4_thuc_te_ud_dao_ham_vdc():
    content = "Tốc độ sinh trưởng của một quần thể vi khuẩn tuân theo công thức $N'(t) = 1000e^{0.1t}$ (con/giờ). Biết ban đầu $t=0$ có 5000 con. Số lượng vi khuẩn sau 10 giờ gần nhất với giá trị nào?"
    # N(10) - N(0) = 10000*(e^1 - 1) => N(10) = 5000 + 10000*(2.718 - 1) = 22180
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="D. 22 180 con",
        option_a="A. 15 000 con", option_b="B. 10 000 con",
        option_c="C. 30 000 con", option_d="D. 22 180 con",
        semantic_hash="APP_THUC_TE_UD_DAO_HAM_VDC"
    )

# Dạng 5: Bài toán thực tế - Vectơ và tọa độ của vectơ trong không gian
def gen_app_5_thuc_te_vecto_khong_gian():
    f1 = random.choice([100, 200, 300])
    content = f"Một chiếc đèn chùm khối lượng $m$ được giữ cân bằng bởi 3 sợi dây cáp chịu lực không co giãn có độ lớn lực căng bằng nhau và bằng {f1} N. Hợp lực của 3 lực căng cáp tác dụng lên đèn chùm có độ lớn bằng:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer="A. Bằng trọng lực $\\vec{P}$ tác dụng lên đèn (hợp lực bằng $\\vec{0}$)",
        option_a="A. Bằng trọng lực $\\vec{P}$ tác dụng lên đèn (hợp lực bằng $\\vec{0}$)",
        option_b=f"B. {f1 * 3} N", option_c=f"C. {f1} N", option_d="D. 0 N",
        semantic_hash="APP_THUC_TE_VECTO_KHONG_GIAN"
    )

# Dạng 6: Bài toán thực tế - Thống kê
def gen_app_6_thuc_te_thong_ke():
    content = "Để đánh giá độ rủi ro giữa hai danh mục đầu tư A và B có cùng lợi nhuận kỳ vọng, nhà đầu tư dựa vào đại lượng thống kê nào của mẫu số liệu ghép nhóm thu nhập?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="B. Phương sai và độ lệch chuẩn",
        option_a="A. Số trung bình", option_b="B. Phương sai và độ lệch chuẩn",
        option_c="C. Trung vị", option_d="D. Mốt",
        semantic_hash="APP_THUC_TE_THONG_KE"
    )

# Dạng 7: Bài toán thực tế - Ứng dụng nguyên hàm giải bài toán thực tiễn
def gen_app_7_thuc_te_nguyen_ham():
    v0 = random.choice([5, 10, 15])
    content = f"Một xe máy đang chạy với vận tốc {v0} m/s thì người lái xe tăng tốc với gia tốc $a(t) = 2t + 1$ ($m/s^2$). Công thức tính vận tốc $v(t)$ của xe máy sau $t$ giây là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"C. $v(t) = t^2 + t + {v0}$",
        option_a=f"A. $v(t) = 2t + {v0}$", option_b=f"B. $v(t) = t^2 + {v0}$",
        option_c=f"C. $v(t) = t^2 + t + {v0}$", option_d=f"D. $v(t) = t^2 + t$",
        semantic_hash="APP_THUC_TE_NGUYEN_HAM"
    )

# Dạng 8: Bài toán thực tế - Ứng dụng tích phân giải bài toán thực tiễn liên quan đến Vật lí
def gen_app_8_thuc_te_tich_phan_vat_li_vdc():
    a0 = random.choice([2, 4])
    t0 = random.choice([3, 5])
    s_ans = (a0 // 2) * (t0 ** 2)
    content = f"Một vật chuyển động từ trạng thái nghỉ ($v(0) = 0$) với gia tốc $a(t) = {a0}t$ ($m/s^2$). Quãng đường $S$ vật đi được trong {t0} giây đầu tiên là:"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer=f"B. {s_ans} m",
        option_a=f"A. {s_ans * 2} m", option_b=f"B. {s_ans} m",
        option_c=f"C. {a0 * t0} m", option_d=f"D. {s_ans // 2} m",
        semantic_hash="APP_THUC_TE_TICH_PHAN_VAT_LI_VDC"
    )

# Dạng 9: Bài toán thực tế - Ứng dụng hình học của tích phân
def gen_app_9_thuc_te_hinh_hoc_tich_phan():
    r = random.choice([2, 3, 4])
    content = f"Mặt cắt ngang của một đường hầm có dạng đường parabol $y = {r**2} - x^2$ (mét) so với mặt đất ($y=0$). Diện tích mặt cắt ngang của đường hầm bằng:"
    # S = int_{-r}^{r} (r^2 - x^2) dx = 2 * (r^3 - r^3/3) = 4/3 * r^3
    s_val = round((4/3) * (r**3), 2)
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"A. {s_val} $m^2$",
        option_a=f"A. {s_val} $m^2$", option_b=f"B. {round(s_val * 1.5, 2)} $m^2$",
        option_c=f"C. {r**2} $m^2$", option_d=f"D. {r**3} $m^2$",
        semantic_hash="APP_THUC_TE_HINH_HOC_TICH_PHAN"
    )

# Dạng 10: Bài toán thực tế - Phương pháp tọa độ trong không gian
def gen_app_10_thuc_te_phuong_phap_toa_do_vdc():
    content = "Một trạm phát sóng radar tại $O(0;0;0)$ phát hiện một máy bay di chuyển theo đường thẳng $d: \\frac{x-1}{2} = \\frac{y-2}{1} = \\frac{z-3}{2}$. Khoảng cách ngắn nhất từ trạm radar $O$ đến đường bay của máy bay gần nhất với giá trị nào?"
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer="C. 2.42 km",
        option_a="A. 3.74 km", option_b="B. 1.50 km",
        option_c="C. 2.42 km", option_d="D. 5.00 km",
        semantic_hash="APP_THUC_TE_PHUONG_PHAP_TOA_DO_VDC"
    )

# Dạng 11: Bài toán thực tế - Xác suất có điều kiện
def gen_app_11_thuc_te_xac_suat_dieu_kien():
    content = "Tỷ lệ mắc bệnh cúm trong một trường học là 5%. Xét nghiệm nhanh có độ chính xác 90% đối với người mắc bệnh. Tính xác suất một học sinh được chọn ngẫu nhiên có kết quả xét nghiệm dương tính biết học sinh đó thực sự mắc bệnh cúm."
    return Question(
        concept_code="BAI_TOAN_THUC_TE", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer="D. 90%",
        option_a="A. 5%", option_b="B. 95%",
        option_c="C. 4.5%", option_d="D. 90%",
        semantic_hash="APP_THUC_TE_XAC_SUAT_DIEU_KIEN"
    )

# ==============================================================================
# BỔ SUNG CHUYÊN ĐỀ: XÁC SUẤT CÓ ĐIỀU KIỆN (5 DẠNG CHUẨN BỘ GD&ĐT)
# ==============================================================================

# Dạng 1: Tính trực tiếp từ định nghĩa và bảng số liệu / sơ đồ
def gen_prob_1_dinh_nghia_bang():
    nA = random.randint(30, 50)
    nB = random.randint(40, 60)
    nAB = random.randint(15, min(nA, nB) - 5)
    
    p_ans = round(nAB / nB, 2)
    p_fake1 = round(nAB / nA, 2)
    p_fake2 = round(nA / (nA + nB), 2)
    p_fake3 = round((nAB + 5) / nB, 2)
    
    content = f"Cho hai biến cố $A$ và $B$. Biết số phần tử thuận lợi cho biến cố $B$ là $n(B) = {nB}$ và số phần tử thuận lợi cho cả hai biến cố $A$ và $B$ xảy ra đồng thời là $n(A \\cap B) = {nAB}$. Xác suất có điều kiện $P(A|B)$ bằng:"
    
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Nhận biết", question_type="PART_I", content=content,
        correct_answer=f"A. ${p_ans}$",
        option_a=f"A. ${p_ans}$", option_b=f"B. ${p_fake1}$",
        option_c=f"C. ${p_fake2}$", option_d=f"D. ${p_fake3}$",
        semantic_hash="PROB_1_DINH_NGHIA"
    )

# Dạng 2: Quy tắc nhân xác suất
def gen_prob_2_quy_tac_nhan():
    pA = round(random.choice([0.4, 0.5, 0.6, 0.7]), 2)
    pBA = round(random.choice([0.3, 0.4, 0.5, 0.8]), 2)
    
    pAB = round(pA * pBA, 2)
    p_fake1 = round(pA + pBA, 2)
    p_fake2 = round(pBA / pA if pA > 0 else 0.5, 2)
    p_fake3 = round(abs(pA - pBA), 2)
    
    content = f"Cho hai biến cố $A$ và $B$ thỏa mãn $P(A) = {pA}$ và $P(B|A) = {pBA}$. Xác suất của biến cố giao $P(A \\cap B)$ bằng:"
    
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=f"A. ${pAB}$",
        option_a=f"A. ${pAB}$", option_b=f"B. ${p_fake1}$",
        option_c=f"C. ${p_fake2}$", option_d=f"D. ${p_fake3}$",
        semantic_hash="PROB_2_QUY_TAC_NHAN"
    )

# Dạng 3: Công thức xác suất toàn phần
def gen_prob_3_xac_suat_toan_phan():
    # Giả sử có 2 nhà máy H1, H2
    pH1 = round(random.choice([0.6, 0.7, 0.55]), 2)
    pH2 = round(1 - pH1, 2)
    
    pBH1 = round(random.choice([0.02, 0.03, 0.05]), 2) # Tỷ lệ phế phẩm nhà máy 1
    pBH2 = round(random.choice([0.04, 0.06, 0.08]), 2) # Tỷ lệ phế phẩm nhà máy 2
    
    pB = round(pH1 * pBH1 + pH2 * pBH2, 4)
    p_fake1 = round(pBH1 + pBH2, 4)
    p_fake2 = round(pH1 * pBH1, 4)
    p_fake3 = round((pBH1 + pBH2) / 2, 4)
    
    content = f"Một công ty mua linh kiện từ hai nhà máy $H_1$ và $H_2$ với tỷ lệ tương ứng là ${int(pH1*100)}\\%$ và ${int(pH2*100)}\\%$. Tỷ lệ phế phẩm của nhà máy $H_1$ là ${int(pBH1*100)}\\%$, của nhà máy $H_2$ là ${int(pBH2*100)}\\%$. Chọn ngẫu nhiên một linh kiện, xác suất để linh kiện đó là phế phẩm bằng:"
    
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Vận dụng", question_type="PART_I", content=content,
        correct_answer=f"A. ${pB}$",
        option_a=f"A. ${pB}$", option_b=f"B. ${p_fake1}$",
        option_c=f"C. ${p_fake2}$", option_d=f"D. ${p_fake3}$",
        semantic_hash="PROB_3_TOAN_PHAN"
    )

# Dạng 4: Công thức Bayes (Xác suất nguyên nhân)
def gen_prob_4_cong_thuc_bayes():
    pH1 = round(random.choice([0.4, 0.6]), 2)
    pH2 = round(1 - pH1, 2)
    
    pBH1 = round(random.choice([0.03, 0.05]), 2)
    pBH2 = round(random.choice([0.02, 0.04]), 2)
    
    pB = pH1 * pBH1 + pH2 * pBH2
    pH1B = round((pH1 * pBH1) / pB, 4)
    
    p_fake1 = round(pH1 * pBH1, 4)
    p_fake2 = round(pBH1, 4)
    p_fake3 = round(1 - pH1B, 4)
    
    content = f"Một kho hàng chứa sản phẩm từ hai xưởng $H_1$ (chiếm ${int(pH1*100)}\\%$) và $H_2$ (chiếm ${int(pH2*100)}\\%$). Tỷ lệ sản phẩm hỏng của xưởng $H_1$ là ${int(pBH1*100)}\\%$, xưởng $H_2$ là ${int(pBH2*100)}\\%$. Lấy ngẫu nhiên một sản phẩm và phát hiện nó bị hỏng. Xác suất để sản phẩm hỏng đó do xưởng $H_1$ sản xuất xấp xỉ bằng:"
    
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Vận dụng cao", question_type="PART_I", content=content,
        correct_answer=f"A. ${pH1B}$",
        option_a=f"A. ${pH1B}$", option_b=f"B. ${p_fake1}$",
        option_c=f"C. ${p_fake2}$", option_d=f"D. ${p_fake3}$",
        semantic_hash="PROB_4_BAYES"
    )

# Dạng 5: Kiểm tra tính độc lập của hai biến cố
def gen_prob_5_doc_lap_bien_co():
    is_independent = random.choice([True, False])
    pA = round(random.choice([0.3, 0.4, 0.5]), 2)
    pB = round(random.choice([0.2, 0.5, 0.6]), 2)
    
    if is_independent:
        pAB = round(pA * pB, 2)
        correct_str = "A. Hai biến cố $A$ và $B$ độc lập vì $P(A \\cap B) = P(A) \\cdot P(B)$."
        opt_b = "B. Hai biến cố $A$ và $B$ không độc lập vì $P(A \\cap B) \\neq P(A) \\cdot P(B)$."
    else:
        pAB = round(pA * pB + 0.1, 2)
        correct_str = "A. Hai biến cố $A$ và $B$ không độc lập vì $P(A \\cap B) \\neq P(A) \\cdot P(B)$."
        opt_b = "B. Hai biến cố $A$ và $B$ độc lập vì $P(A \\cap B) = P(A) \\cdot P(B)$."
        
    opt_c = "C. Hai biến cố $A$ và $B$ xung khắc."
    opt_d = "D. Không đủ dữ kiện để kết luận về tính độc lập."
    
    content = f"Cho hai biến cố $A$ và $B$ có $P(A) = {pA}$, $P(B) = {pB}$ và $P(A \\cap B) = {pAB}$. Khẳng định nào sau đây là đúng?"
    
    return Question(
        concept_code="XAC_SUAT_DIEU_KIEN", bloom_level="Thông hiểu", question_type="PART_I", content=content,
        correct_answer=correct_str,
        option_a=correct_str, option_b=opt_b,
        option_c=opt_c, option_d=opt_d,
        semantic_hash="PROB_5_DOC_LAP"
    )

# ==============================================================================
# 🚀 PHÂN LOẠI CÁC DẠNG BÀI THEO MỨC ĐỘ TƯ DUY (BLOOM LEVEL)
# ==============================================================================

DANG_BAI_NHAN_BIET = [
    generate_dang_1, generate_dang_4, generate_dang_5, generate_dang_6, 
    generate_dang_8, generate_dang_10, generate_dang_14, generate_dang_20, 
    generate_dang_21, generate_dang_22,
    # Các dạng Đạo hàm / Hàm số (Nhận biết)
    gen_ud_1_dau_dao_ham_don_dieu, gen_ud_2_bbt_don_dieu, gen_ud_4_dau_dao_ham_cuc_tri,
    gen_ud_5_bbt_cuc_tri, gen_ud_10_minmax_bbt, gen_ud_14_tiemcan_bbt,
    gen_ud_15_tim_tiem_can, gen_ud_18_nhan_dang_do_thi,
    # Các dạng Vectơ & Thống kê (Nhận biết)
    gen_vec_1_khai_niem, gen_vec_3_goc_tich_vo_huong, gen_vec_5_xac_dinh_toa_do,
    gen_vec_7_tich_vo_huong_oxyz, gen_stat_1_khoang_bien_thien, gen_stat_2_khoang_tu_phan_vi,
    # Các dạng Phương pháp tọa độ trong không gian (Nhận biết)
    gen_geo_1_yeu_to_mat_phang,
    gen_geo_2_mp_1diem_1vpt,
    gen_geo_6_mp_song_song_mp,
    gen_geo_8_vttd_hai_mp,
    gen_geo_10_yeu_to_duong_thang,
    gen_geo_11_dt_1diem_1vcp,
    gen_geo_13_dt_vuong_goc_mp,
    gen_geo_17_goc_hai_dt,
    gen_geo_18_goc_dt_va_mp,
    gen_geo_19_goc_hai_mp,
    gen_geo_21_yeu_to_mat_cau,
    gen_geo_22_mc_tam_ban_kinh,
    # Các dạng xác suất có điều kiện (Nhận biết)
    gen_prob_1_dinh_nghia_bang,
    # Các dạng chuyên đề toán thực tế (Nhận biết)
    gen_app_3_thuc_te_tiem_can,
    gen_app_6_thuc_te_thong_ke,
    gen_app_11_thuc_te_xac_suat_dieu_kien
]

DANG_BAI_THONG_HIEU = [
    generate_dang_2, generate_dang_3, generate_dang_7, generate_dang_9, 
    generate_dang_11, generate_dang_12, generate_dang_13, generate_dang_15, 
    generate_dang_16, generate_dang_17, generate_dang_19, generate_part3_dang_6,
    # Các dạng Đạo hàm / Hàm số (Thông hiểu)
    gen_ud_3_dothi_fphay_don_dieu, gen_ud_6_dothi_fphay_cuc_tri, gen_ud_7_thuc_te_don_dieu_cuc_tri,
    gen_ud_8_tham_so_cuc_tri, gen_ud_11_minmax_doan, gen_ud_12_thuc_te_minmax,
    gen_ud_16_tiemcan_thamso, gen_ud_17_thuc_te_tiem_can,
    # Các dạng Vectơ & Thống kê (Thông hiểu)
    gen_vec_2_phan_tich, gen_vec_4_thuc_te_co_dien, gen_vec_6_phep_toan_do_dai,
    # Các dạng Phương pháp tọa độ trong không gian (Thông hiểu)
    gen_geo_3_mp_1diem_cap_vcp,
    gen_geo_4_mp_qua_3_diem,
    gen_geo_5_mp_trung_truc,
    gen_geo_7_khoang_cach_diem_mp,
    gen_geo_12_dt_qua_2_diem,
    gen_geo_14_dt_song_song_dt,
    gen_geo_15_vttd_hai_dt,
    gen_geo_23_mc_tam_qua_1_diem,
    gen_geo_24_mc_duong_kinh,
    gen_geo_26_mc_tam_tiep_xuc_mp,
    # Các dạng xác suất có điều kiện (Thông hiểu)
    gen_prob_2_quy_tac_nhan,
    gen_prob_3_xac_suat_toan_phan,
    gen_prob_5_doc_lap_bien_co,
    # Các dạng chuyên đề toán thực tế (Thông hiểu)
    gen_app_1_thuc_te_don_dieu_cuc_tri,
    gen_app_5_thuc_te_vecto_khong_gian,
    gen_app_7_thuc_te_nguyen_ham,
    gen_app_9_thuc_te_hinh_hoc_tich_phan
]

DANG_BAI_VAN_DUNG_CAO = [
    generate_dang_18, generate_part3_dang_1, generate_part3_dang_2, 
    generate_part3_dang_3, generate_part3_dang_4, generate_part3_dang_5, 
    generate_part3_dang_7, generate_part3_dang_8,
    # Các dạng Đạo hàm / Hàm số (Vận dụng cao)
    gen_ud_9_ham_hop_cuc_tri, gen_ud_13_ham_hop_minmax, gen_ud_19_vdc_thuc_tien_dothi,
    # Các dạng Vectơ & Thống kê (Vận dụng cao)
    gen_vec_8_thuc_te_oxyz_vdc, gen_stat_3_phuong_sai_rui_ro_vdc,
    # Các dạng Phương pháp tọa độ trong không gian (Vận dụng cao)
    gen_geo_9_thuc_te_mat_phang_vdc,
    gen_geo_16_thuc_te_duong_thang_vdc,
    gen_geo_20_thuc_te_goc_vdc,
    gen_geo_25_mc_qua_4_diem_vdc,
    gen_geo_27_thuc_te_mat_cau_vdc,
    # Các dạng xác suất có điều kiện (Vận dụng cao)
    gen_prob_4_cong_thuc_bayes,
    # Các dạng chuyên đề toán thực tế (Vận dụng cao)
    gen_app_2_thuc_te_min_max,
    gen_app_4_thuc_te_ud_dao_ham_vdc,
    gen_app_8_thuc_te_tich_phan_vat_li_vdc,
    gen_app_10_thuc_te_phuong_phap_toa_do_vdc
]


def generate_adaptive_exam(user_level="Khá"):
    """
    Hàm sinh đề thi thích ứng (Adaptive Exam) sau khi khảo sát đầu vào.
    
    Cấu trúc ma trận tỉ lệ theo Năng lực học sinh:
    * Yếu : 70% Nhận biết | 30% Thông hiểu | 0% Vận dụng cao  (Giúp củng cố nền tảng)
    * Khá : 30% Nhận biết | 50% Thông hiểu | 20% Vận dụng cao (Tối ưu điểm 7-8)
    * Giỏi: 10% Nhận biết | 40% Thông hiểu | 50% Vận dụng cao (Luyện chinh phục 9-10)
    """
    questions_pool = []
    
    # Thiết lập số lượng câu cho đề thi 15 câu thích ứng
    if user_level in ["Yếu", "Trung bình"]:
        count_nb, count_th, count_vdc = 10, 5, 0
    elif user_level in ["Giỏi", "Xuất sắc"]:
        count_nb, count_th, count_vdc = 2, 6, 7
    else: # Mặc định là trình độ "Khá"
        count_nb, count_th, count_vdc = 5, 7, 3

    # 1. Bốc thăm câu hỏi Nhận biết
    for i in range(count_nb):
        func = random.choice(DANG_BAI_NHAN_BIET)
        q = func()
        q.semantic_hash = f"adaptive_{user_level}_nb_{i}_{random.randint(1000, 9999)}"
        questions_pool.append(q)

    # 2. Bốc thăm câu hỏi Thông hiểu
    for i in range(count_th):
        func = random.choice(DANG_BAI_THONG_HIEU)
        q = func()
        q.semantic_hash = f"adaptive_{user_level}_th_{i}_{random.randint(1000, 9999)}"
        questions_pool.append(q)

    # 3. Bốc thăm câu hỏi Vận dụng cao
    for i in range(count_vdc):
        func = random.choice(DANG_BAI_VAN_DUNG_CAO)
        q = func()
        q.semantic_hash = f"adaptive_{user_level}_vdc_{i}_{random.randint(1000, 9999)}"
        questions_pool.append(q)

    # Trộn ngẫu nhiên thứ tự các câu hỏi để đề thi tự nhiên
    random.shuffle(questions_pool)
    return questions_pool