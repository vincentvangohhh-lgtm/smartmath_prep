from app import create_app, db
from app.models import Question

app = create_app()

def seed_official_exam_2026_0101():
    with app.app_context():
        # 1. Xóa triệt để dữ liệu cũ của Mã đề 0101 - Năm 2026 nếu đã tồn tại
        Question.query.filter_by(year=2026, code_id='0101').delete()
        db.session.commit()

        # 2. Danh sách 22 câu hỏi chuẩn nguyên văn Mã đề 0101 (Năm 2026) + Đáp án Bộ GD&ĐT
        questions_data = [
            # ================= PHẦN I (12 CÂU TRẮC NGHIỆM ĐƠN) =================
            {
                "question_number": 1,
                "question_type": "PART_I",
                "content": "Cho cấp số cộng $(u_n)$ có $u_1 = 5$ và công sai $d = -1$. Giá trị của $u_2$ bằng",
                "image_url": None,
                "option_a": "4.",
                "option_b": "-5.",
                "option_c": "5.",
                "option_d": "-4.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 2,
                "question_type": "PART_I",
                "content": "Cho các hàm số $y = f(x)$ và $y = g(x)$ có đạo hàm trên tập số thực $\\mathbb{R}$ thỏa mãn $f'(x) = x$ và $g'(x) = x^2$. Đạo hàm của hàm số $y = f(x) + g(x)$ là",
                "image_url": None,
                "option_a": "$3x$.",
                "option_b": "$1 + x^2$.",
                "option_c": "$x + x^2$.",
                "option_d": "$1 + 2x$.",
                "correct_ans": "C",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 3,
                "question_type": "PART_I",
                "content": "Cho $\\int f(x) dx = \\sin x + C$. Phát biểu nào sau đây là đúng?",
                "image_url": None,
                "option_a": "$\\int [3 + f(x)] dx = 3x + \\cos x + C$.",
                "option_b": "$\\int [3 + f(x)] dx = 3x + \\sin x + C$.",
                "option_c": "$\\int [3 + f(x)] dx = 3x - \\cos x + C$.",
                "option_d": "$\\int [3 + f(x)] dx = 3x - \\sin x + C$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 4,
                "question_type": "PART_I",
                "content": "Nghiệm của phương trình $\\log_3(x - 1) = 1$ là",
                "image_url": None,
                "option_a": "$x = 2$.",
                "option_b": "$x = 3$.",
                "option_c": "$x = 5$.",
                "option_d": "$x = 4$.",
                "correct_ans": "D",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 5,
                "question_type": "PART_I",
                "content": "Trong không gian với hệ tọa độ $Oxyz$, cho hai điểm $A(1; 5; 1)$ và $B(3; 3; 1)$. Vectơ $\\overrightarrow{AB}$ có tọa độ là",
                "image_url": None,
                "option_a": "$(2; -2; 0)$.",
                "option_b": "$(-2; 2; 0)$.",
                "option_c": "$(4; 8; 2)$.",
                "option_d": "$(2; 4; 1)$.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 6,
                "question_type": "PART_I",
                "content": "Cho hai biến cố độc lập $A$ và $B$ có xác suất thỏa mãn $P(A) = 0,5$ và $P(B) = 0,4$. Giá trị của $P(AB)$ bằng",
                "image_url": None,
                "option_a": "0,8.",
                "option_b": "0,1.",
                "option_c": "0,9.",
                "option_d": "0,2.",
                "correct_ans": "D",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 7,
                "question_type": "PART_I",
                "content": "Cho hình lập phương $ABCD.A'B'C'D'$ (xem hình dưới). Vectơ nào sau đây bằng vectơ $\\overrightarrow{AB}$?",
                "image_url": "images/q7_cube_2026.png",
                "option_a": "$\\overrightarrow{AA'}$.",
                "option_b": "$\\overrightarrow{D'C'}$.",
                "option_c": "$\\overrightarrow{CD}$.",
                "option_d": "$\\overrightarrow{AD}$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 8,
                "question_type": "PART_I",
                "content": "Cặp số nào sau đây là nghiệm của hệ bất phương trình $\\begin{cases} x + y - 3 < 0 \\\\ x - y + 1 > 0 \\end{cases}$?",
                "image_url": None,
                "option_a": "$(1; 0)$.",
                "option_b": "$(0; 2)$.",
                "option_c": "$(-1; 1)$.",
                "option_d": "$(1; 2)$.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 9,
                "question_type": "PART_I",
                "content": "Hàm số $F(x) = 4x^3$ là một nguyên hàm của hàm số nào sau đây?",
                "image_url": None,
                "option_a": "$f_2(x) = 3x^2$.",
                "option_b": "$f_3(x) = 12x^2$.",
                "option_c": "$f_1(x) = x^4$.",
                "option_d": "$f_4(x) = 4x^4$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 10,
                "question_type": "PART_I",
                "content": "Cho hàm số $y = \\frac{ax + b}{cx + d}$ ($c \\neq 0, ad - bc \\neq 0$) có bảng biến thiên như hình bên dưới.<br><table class='table table-bordered text-center my-2' style='max-width: 500px; margin: 0 auto;'><tr><td>$x$</td><td>$-\\infty$</td><td>1</td><td>$+\\infty$</td></tr><tr><td>$y'$</td><td>+</td><td>||</td><td>+</td></tr><tr><td>$y$</td><td>$-2 \\nearrow +\\infty$</td><td>||</td><td>$-\\infty \\nearrow -2$</td></tr></table>Đường tiệm cận ngang của đồ thị hàm số đã cho có phương trình là",
                "image_url": None,
                "option_a": "$y = -2$.",
                "option_b": "$x = -2$.",
                "option_c": "$x = 1$.",
                "option_d": "$y = 1$.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 11,
                "question_type": "PART_I",
                "content": "Cho cấp số nhân $(u_n)$ có số hạng đầu $u_1$ và công bội $q$ với $u_1 \\neq 0, q > 1$. Số hạng $u_4$ là",
                "image_url": None,
                "option_a": "$u_4 = u_1 \\cdot q^3$.",
                "option_b": "$u_4 = u_1 \\cdot q^4$.",
                "option_c": "$u_4 = u_1 + 3q$.",
                "option_d": "$u_4 = u_1 + 4q$.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 12,
                "question_type": "PART_I",
                "content": "Khảo sát thời gian (đơn vị: phút) học trực tuyến trong một ngày của 42 học sinh, người ta thu được mẫu số liệu ghép nhóm như sau:<br><table class='table table-bordered text-center my-2' style='max-width: 600px; margin: 0 auto;'><tr><td>Thời gian học trực tuyến</td><td>[10;20)</td><td>[20;30)</td><td>[30;40)</td><td>[40;50)</td><td>[50;60)</td><td>[60;70)</td></tr><tr><td>Số học sinh</td><td>4</td><td>8</td><td>14</td><td>7</td><td>4</td><td>5</td></tr></table>Trung vị của mẫu số liệu trên thuộc nhóm nào sau đây?",
                "image_url": None,
                "option_a": "[30;40).",
                "option_b": "[40;50).",
                "option_c": "[60;70).",
                "option_d": "[50;60).",
                "correct_ans": "A",
                "bloom_level": "Thông hiểu"
            },

            # ================= PHẦN II (4 CÂU ĐÚNG / SAI) =================
            {
                "question_number": 13,
                "question_type": "PART_II",
                "content": "Nhằm đưa ra cảnh báo sớm về tình trạng sức khỏe của cư dân, người ta sử dụng một ứng dụng trí tuệ nhân tạo để sàng lọc nguy cơ mắc bệnh dựa trên hồ sơ y tế được lưu trữ. Khi phát hiện nguy cơ mắc bệnh, ứng dụng này sẽ gửi cảnh báo để giúp người dân đi khám bệnh kịp thời. Người ta dùng ứng dụng này để tầm soát nguy cơ mắc một loại bệnh.<br>Kết quả thu được khi quét thử nghiệm hồ sơ y tế của 10 000 người như sau: Có 1000 người nhận được cảnh báo và 9000 người còn lại không nhận được cảnh báo từ ứng dụng. Trong số 1000 người nhận được cảnh báo thì có 700 người có bệnh và 300 người không có bệnh. Trong số 9000 người không nhận được cảnh báo thì có 100 người có bệnh và 8900 người không có bệnh.<br>Chọn ngẫu nhiên một người trong số 10 000 người nói trên.",
                "image_url": None,
                "sub_q_a": "Xác suất để người đó không nhận được cảnh báo từ ứng dụng bằng 0,9.",
                "sub_q_b": "Xác suất để người đó không có bệnh, biết rằng người đó không nhận được cảnh báo từ ứng dụng, lớn hơn 0,98.",
                "sub_q_c": "Xác suất để người đó không có bệnh bằng 0,9.",
                "sub_q_d": "Xác suất để người đó không nhận được cảnh báo từ ứng dụng, biết rằng người đó không có bệnh, nhỏ hơn 0,95.",
                "correct_ans": "Đúng,Đúng,Sai,Sai",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 14,
                "question_type": "PART_II",
                "content": "Cho hàm số $f(x) = \\frac{1}{3}x^3 - 5x^2 + 9x + 8$.",
                "image_url": None,
                "sub_q_a": "Hàm số đã cho có đạo hàm là $f'(x) = x^2 - 10x + 9$.",
                "sub_q_b": "Phương trình $f'(x) = 0$ có tập nghiệm là $S = \\{1; 9\\}$.",
                "sub_q_c": "Hàm số đã cho nghịch biến trên khoảng $(1; 9)$.",
                "sub_q_d": "Giá trị cực tiểu của hàm số đã cho bằng $\\frac{37}{3}$.",
                "correct_ans": "Đúng,Đúng,Đúng,Sai",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 15,
                "question_type": "PART_II",
                "content": "Một hệ thống pin năng lượng mặt trời gồm các tấm pin được kết nối với một bộ lưu trữ điện. Trong thời gian mặt trời chiếu sáng của một ngày, năng lượng điện thu được từ các tấm pin được lưu trong bộ lưu trữ điện. Gọi $F(t)$ là năng lượng điện (kWh) lưu trữ được kể từ thời điểm hệ thống bắt đầu hoạt động đến thời điểm $t$, trong đó $t$ là thời gian tính theo giờ ($0 \\le t \\le 12$) và thời điểm hệ thống bắt đầu hoạt động ứng với $t = 0$. Biết rằng $F(0) = 0$.<br>Tốc độ lưu trữ năng lượng điện (kW) của hệ thống này là hàm số $f(t) = F'(t)$ với $0 \\le t \\le 12$. Số liệu ghi nhận được ở một ngày cụ thể trong năm cho thấy $f(t) = -0,3t^2 + 3,6t$ với $0 \\le t \\le 12$.",
                "image_url": None,
                "sub_q_a": "$F(t) = -0,1t^3 + 1,8t^2$ với $0 \\le t \\le 12$.",
                "sub_q_b": "Năng lượng điện (kWh) lưu trữ được kể từ thời điểm $t = a$ đến thời điểm $t = b$ ($0 \\le a < b \\le 12$) là $\\int_{a}^{b} f(t) dt$.",
                "sub_q_c": "Năng lượng điện lưu trữ được kể từ thời điểm $t = 1$ đến thời điểm $t = 4$ nhỏ hơn 20,6 kWh.",
                "sub_q_d": "Năng lượng điện lưu trữ được kể từ thời điểm $t = 1$ đến thời điểm $t = 7$ gấp hai lần năng lượng điện lưu trữ được kể từ thời điểm $t = 1$ đến thời điểm $t = 4$.",
                "correct_ans": "Đúng,Đúng,Sai,Sai",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 16,
                "question_type": "PART_II",
                "content": "Trong không gian xét hệ tọa độ $Oxyz$ có một đơn vị dài trên các trục tương ứng với 10 mét trên thực tế. Một mục tiêu cần được bảo vệ có vị trí ở gốc tọa độ $O$. Người ta thiết lập một vành đai bảo vệ quanh mục tiêu theo một đường tròn tâm $O$ có bán kính bằng 7 đơn vị (tương ứng 70 mét trên thực tế) nằm trong mặt phẳng $(Oxy)$. Một máy bay không người lái (được coi như một hạt) bay theo một đường thẳng từ vị trí $M(5; 10; 4)$ đến vị trí $N(14; -2; 4)$. Tại mỗi vị trí của máy bay, khoảng cách từ máy bay đến vành đai bảo vệ là độ dài ngắn nhất của các đoạn thẳng nối từ vị trí đó đến một điểm bất kỳ trên vành đai.",
                "image_url": None,
                "sub_q_a": "$\\overrightarrow{MN} = (9; -12; 0)$.",
                "sub_q_b": "Phương trình tham số của đường thẳng $MN$ là $\\begin{cases} x = 5 + 3t \\\\ y = 10 - 4t \\\\ z = 0 \\end{cases}$ với $t \\in \\mathbb{R}$.",
                "sub_q_c": "Trong quá trình bay từ $M$ đến $N$, khoảng cách ngắn nhất từ máy bay đến vành đai bảo vệ là 50 mét.",
                "sub_q_d": "Trong quá trình bay từ $M$ đến $N$, khoảng cách từ máy bay đến vành đai bảo vệ là ngắn nhất khi máy bay ở vị trí có tọa độ là $(8; 6; 4)$.",
                "correct_ans": "Đúng,Sai,Đúng,Đúng",
                "bloom_level": "Vận dụng cao"
            },

            # ================= PHẦN III (6 CÂU TỰ LUẬN ĐIỀN SỐ) =================
            {
                "question_number": 17,
                "question_type": "PART_III",
                "content": "Cho hình lập phương $ABCD.MNPQ$ có cạnh bằng 6. Gọi $E$ là trung điểm của đoạn thẳng $AB$. Khoảng cách từ điểm $P$ đến mặt phẳng $(MED)$ bằng bao nhiêu (không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần trăm)?",
                "image_url": None,
                "correct_ans": "7.35",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 18,
                "question_type": "PART_III",
                "content": "Trong một trò chơi bạn Bình cần vượt qua một thử thách. Theo yêu cầu của thử thách, Bình cần điền tất cả 15 số thuộc tập hợp $\\{0; 1; 2; 3; 4; 5; 6; 7; 8; 10; 11; 12; 15; 16; 20\\}$ vào 15 ô vuông trong hình dưới thỏa mãn đồng thời ba điều kiện sau:<br>- Mỗi ô điền đúng một số và mỗi số chỉ được sử dụng một lần;<br>- Hiệu hai số ở hai ô bất kỳ khác nhau trên cùng một hàng không chia hết cho 5;<br>- Hiệu hai số ở hai ô bất kỳ khác nhau trên cùng một cột không chia hết cho 5.<br>Hai cách điền gọi là giống nhau nếu số điền ở mỗi ô tương ứng trong 15 ô là giống nhau. Gọi $H$ là số cách điền khác nhau để bạn Bình vượt qua được thử thách. Giá trị của $\\frac{H}{30}$ bằng bao nhiêu?",
                "image_url": "images/q18_grid_2026.png",
                "correct_ans": "1152",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 19,
                "question_type": "PART_III",
                "content": "Để chế tác một hạt cườm, người ta lấy một khối vật thể có dạng một khối tròn xoay được tạo thành khi quay hình phẳng giới hạn bởi trục $Ox$ và nửa trên của elip $\\frac{x^2}{1,5^2} + \\frac{y^2}{1^2} = 1$ quanh trục $Ox$, sau đó khoan dọc theo trục xoay (xem hình dưới). Lỗ khoan có dạng hình trụ với bán kính $0,2\\text{ cm}$ và có trục nằm trên trục xoay. Phần còn lại sau khi khoan là hạt cườm, có dạng một khối tròn xoay. Thể tích của hạt cườm đó bằng bao nhiêu xentimét khối (không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần trăm)?",
                "image_url": "images/q19_bead_2026.png",
                "correct_ans": "5.91",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 20,
                "question_type": "PART_III",
                "content": "Một khung hình trang trí có dạng một đa giác đều 12 cạnh $A_1A_2...A_{12}$ (xem hình dưới) được gắn cố định trên một trần nhà. Bạn Dũng có 12 bóng đèn gồm bốn bóng màu đỏ và tám bóng màu xanh, có công suất đôi một khác nhau. Bạn Dũng lắp ngẫu nhiên 12 bóng đèn trên vào 12 đỉnh $A_1, A_2, ..., A_{12}$ sao cho mỗi đỉnh có đúng một bóng đèn. Gọi $P$ là xác suất để mỗi hình vuông (có bốn đỉnh là các đỉnh của đa giác đã cho) đều có ít nhất một bóng đèn màu đỏ. Giá trị của $3190P$ bằng bao nhiêu?",
                "image_url": "images/q20_polygon_2026.png",
                "correct_ans": "1856",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 21,
                "question_type": "PART_III",
                "content": "Một nông trại cung cấp rau quả cho siêu thị A với số liệu bán hàng của bốn ngày trong tuần được ghi lại trong bảng sau:<br><table class='table table-bordered text-center my-2' style='max-width: 600px; margin: 0 auto;'><tr><td rowspan='2' class='align-middle'>Ngày</td><td colspan='3'>Số ki-lô-gam</td><td rowspan='2' class='align-middle'>Tổng số tiền (nghìn đồng)</td></tr><tr><td>Rau muống</td><td>Bí xanh</td><td>Cà chua</td></tr><tr><td>Thứ Tư</td><td>19</td><td>14</td><td>10</td><td>600</td></tr><tr><td>Thứ Năm</td><td>20</td><td>12</td><td>8</td><td>540</td></tr><tr><td>Thứ Sáu</td><td>25</td><td>12</td><td>7</td><td>570</td></tr><tr><td>Thứ Bảy</td><td>50</td><td>25</td><td>20</td><td>?</td></tr></table>Biết rằng đơn giá theo ki-lô-gam của mỗi loại rau quả trong bảng trên là không đổi. Tổng số tiền nông trại thu được ở ngày thứ Bảy từ ba loại rau quả trên khi cung cấp cho siêu thị A là bao nhiêu nghìn đồng?",
                "image_url": None,
                "correct_ans": "1275",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 22,
                "question_type": "PART_III",
                "content": "Một công ty nông sản có công suất chế biến không quá 200 tấn nguyên liệu một tháng. Nếu công ty chế biến $x$ tấn nguyên liệu trong một tháng ($1 \\le x \\le 200$) thì chi phí sản xuất và doanh thu lần lượt là $C(x) = 0,001x^3 + 30x + 10$ (triệu đồng) và $R(x) = 60x$ (triệu đồng). Lợi nhuận lớn nhất mà công ty đạt được trong một tháng là bao nhiêu triệu đồng?",
                "image_url": None,
                "correct_ans": "1990",
                "bloom_level": "Vận dụng"
            }
        ]

        # 3. Tiến hành thêm từng câu hỏi vào CSDL
        has_correct_option = hasattr(Question, 'correct_option')
        has_correct_answer = hasattr(Question, 'correct_answer')
        has_answer = hasattr(Question, 'answer')

        for item in questions_data:
            kwargs = {
                "year": 2026,
                "code_id": '0101',
                "question_number": item["question_number"],
                "question_type": item["question_type"],
                "content": item["content"],
                "image_url": item.get("image_url"),
                "option_a": item.get("option_a"),
                "option_b": item.get("option_b"),
                "option_c": item.get("option_c"),
                "option_d": item.get("option_d"),
                "sub_q_a": item.get("sub_q_a"),
                "sub_q_b": item.get("sub_q_b"),
                "sub_q_c": item.get("sub_q_c"),
                "sub_q_d": item.get("sub_q_d"),
                "bloom_level": item["bloom_level"]
            }

            val = item["correct_ans"]
            if has_correct_option:
                kwargs["correct_option"] = val
            elif has_correct_answer:
                kwargs["correct_answer"] = val
            elif has_answer:
                kwargs["answer"] = val

            q = Question(**kwargs)
            db.session.add(q)

        db.session.commit()
        print("🎉 Đã thêm MÃ ĐỀ 0101 - THPT NĂM 2026 chuẩn Bộ GD&ĐT vào CSDL thành công!")

if __name__ == "__main__":
    seed_official_exam_2026_0101()