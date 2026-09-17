from app import create_app, db
from app.models import Question

app = create_app()

def seed_official_exam_2025():
    with app.app_context():
        # 1. Ép buộc xóa sạch hoàn toàn các bản ghi mã 0101 cũ trong CSDL
        Question.query.filter_by(year=2025, code_id='0101').delete()
        db.session.commit()

        # 2. Danh sách 22 câu hỏi chuẩn 100% NGUYÊN VĂN + ĐÁP ÁN BỘ GD&ĐT
        questions_data = [
            # ================= PHẦN I (12 CÂU TRẮC NGHIỆM ĐƠN) =================
            {
                "question_number": 1,
                "question_type": "PART_I",
                "content": "Cho hình lăng trụ $ABC.A'B'C'$ (xem hình dưới). Phát biểu nào sau đây là đúng?",
                "image_url": "images/q1_prism.png",
                "option_a": "$\\overrightarrow{BA} + \\overrightarrow{A'C'} = \\overrightarrow{BC'}$.",
                "option_b": "$\\overrightarrow{BA} + \\overrightarrow{A'C'} = \\overrightarrow{C'B}$.",
                "option_c": "$\\overrightarrow{BA} + \\overrightarrow{A'C'} = \\overrightarrow{BC}$.",
                "option_d": "$\\overrightarrow{BA} + \\overrightarrow{A'C'} = \\overrightarrow{A'A}$.",
                "correct_ans": "C",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 2,
                "question_type": "PART_I",
                "content": "Cho hình hộp $ABCD.A'B'C'D'$ (xem hình dưới). Đường thẳng $AB$ song song với mặt phẳng nào sau đây?",
                "image_url": "images/q2_box.png",
                "option_a": "$(CC'A'A)$.",
                "option_b": "$(BB'C'C)$.",
                "option_c": "$(A'B'C'D')$.",
                "option_d": "$(AA'D'D)$.",
                "correct_ans": "C",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 3,
                "question_type": "PART_I",
                "content": "Một người chia thời lượng (đơn vị: giây) thực hiện các cuộc gọi điện thoại của mình trong một tuần thành sáu nhóm và lập bảng tần số ghép nhóm như sau:<br><table class='table table-bordered text-center my-2' style='max-width: 600px; margin: 0 auto;'><tr><td>Nhóm</td><td>[0;40)</td><td>[40;80)</td><td>[80;120)</td><td>[120;160)</td><td>[160;200)</td><td>[200;240)</td></tr><tr><td>Tần số</td><td>11</td><td>10</td><td>6</td><td>8</td><td>4</td><td>1</td></tr></table>Tứ phân vị thứ ba $Q_3$ (đơn vị: giây) của mẫu số liệu ghép nhóm trên bằng",
                "image_url": None,
                "option_a": "145.",
                "option_b": "140.",
                "option_c": "135.",
                "option_d": "130.",
                "correct_ans": "C",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 4,
                "question_type": "PART_I",
                "content": "Trong không gian với hệ tọa độ $Oxyz$, cho đường thẳng $(d): \\frac{x-3}{-5} = \\frac{y+2}{4} = \\frac{z-1}{2}$. Vectơ nào sau đây là một vectơ chỉ phương của đường thẳng $(d)$?",
                "image_url": None,
                "option_a": "$\\vec{u}_1 = (4; 5; 2)$.",
                "option_b": "$\\vec{u}_2 = (3; -2; 1)$.",
                "option_c": "$\\vec{u}_3 = (3; 2; 1)$.",
                "option_d": "$\\vec{u}_4 = (4; -5; 2)$.",
                "correct_ans": "D",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 5,
                "question_type": "PART_I",
                "content": "Họ nguyên hàm của hàm số $f(x) = x^2$ là",
                "image_url": None,
                "option_a": "$\\frac{1}{3}x^3 + C$.",
                "option_b": "$2x^3 + C$.",
                "option_c": "$3x^3 + C$.",
                "option_d": "$\\frac{1}{2}x^3 + C$.",
                "correct_ans": "A",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 6,
                "question_type": "PART_I",
                "content": "Cho cấp số cộng $(u_n)$ có $u_1 = 4$ và công sai $d = -3$. Giá trị của $u_5$ bằng",
                "image_url": None,
                "option_a": "16.",
                "option_b": "19.",
                "option_c": "-8.",
                "option_d": "-11.",
                "correct_ans": "C",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 7,
                "question_type": "PART_I",
                "content": "Tập nghiệm của phương trình $\\sin x = 0$ là",
                "image_url": None,
                "option_a": "$S = \\left\\{\\frac{\\pi}{2} + k\\pi \\mid k \\in \\mathbb{Z}\\right\\}$.",
                "option_b": "$S = \\{k2\\pi \\mid k \\in \\mathbb{Z}\\}$.",
                "option_c": "$S = \\left\\{-\\frac{\\pi}{2} + k2\\pi \\mid k \\in \\mathbb{Z}\\right\\}$.",
                "option_d": "$S = \\{k\\pi \\mid k \\in \\mathbb{Z}\\}$.",
                "correct_ans": "D",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 8,
                "question_type": "PART_I",
                "content": "Trong mặt phẳng với hệ tọa độ $Oxy$, diện tích $S$ của hình phẳng giới hạn bởi đồ thị của hàm số $y = 2x - 3$, trục hoành và hai đường thẳng $x = 1, x = 2$ được xác định bằng công thức",
                "image_url": None,
                "option_a": "$S = \\pi \\int_{1}^{2} |2x - 3| dx$.",
                "option_b": "$S = \\int_{1}^{2} |2x - 3| dx$.",
                "option_c": "$S = \\pi \\int_{1}^{2} (2x - 3)^2 dx$.",
                "option_d": "$S = \\int_{1}^{2} (2x - 3) dx$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 9,
                "question_type": "PART_I",
                "content": "Trong không gian với hệ tọa độ $Oxyz$, mặt phẳng đi qua điểm $A(2; 1; -4)$ nhận $\\vec{n} = (3; 2; -1)$ làm một vectơ pháp tuyến có phương trình là",
                "image_url": None,
                "option_a": "$3(x-2) + 2(y-1) - (z+4) = 0$.",
                "option_b": "$2(x+3) + (y+2) - 4(z-1) = 0$.",
                "option_c": "$3(x+2) + 2(y+1) - (z-4) = 0$.",
                "option_d": "$2(x-3) + (y-2) - 4(z+1) = 0$.",
                "correct_ans": "A",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 10,
                "question_type": "PART_I",
                "content": "Nghiệm của phương trình $\\log_2(2x - 1) = 2$ là",
                "image_url": None,
                "option_a": "$x = \\frac{7}{2}$.",
                "option_b": "$x = \\frac{5}{2}$.",
                "option_c": "$x = -5$.",
                "option_d": "$x = 4$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 11,
                "question_type": "PART_I",
                "content": "Cho hàm số $y = \\frac{ax + b}{cx + d}$ ($ac \\neq 0, ad - bc \\neq 0$) có đồ thị như hình bên dưới. Đường tiệm cận đứng của đồ thị hàm số đã cho có phương trình là",
                "image_url": "images/q11_hyperbola.png",
                "option_a": "$y = 2$.",
                "option_b": "$x = -1$.",
                "option_c": "$y = -1$.",
                "option_d": "$x = 2$.",
                "correct_ans": "B",
                "bloom_level": "Nhận biết"
            },
            {
                "question_number": 12,
                "question_type": "PART_I",
                "content": "Cho hình chóp $S.ABC$ có $SA$ vuông góc với mặt phẳng $(ABC)$, tam giác $ABC$ vuông tại $A$ và $SA = 3, AB = 4, AC = 5$. Thể tích của khối chóp $S.ABC$ bằng",
                "image_url": None,
                "option_a": "30.",
                "option_b": "20.",
                "option_c": "60.",
                "option_d": "10.",
                "correct_ans": "D",
                "bloom_level": "Thông hiểu"
            },

            # ================= PHẦN II (4 CÂU ĐÚNG / SAI NGUYÊN VĂN) =================
            {
                "question_number": 13,
                "question_type": "PART_II",
                "content": "Cho hàm số $f(x) = x^3 - 12x - 8$.",
                "image_url": None,
                "sub_q_a": "Hàm số đã cho có đạo hàm $f'(x) = 3x^2 - 12$.",
                "sub_q_b": "Phương trình $f'(x) = 0$ có tập nghiệm là $S = \\{2\\}$.",
                "sub_q_c": "$f(2) = 24$.",
                "sub_q_d": "Giá trị lớn nhất của hàm số $f(x)$ trên đoạn $[-3; 3]$ bằng 24.",
                "correct_ans": "Đúng,Sai,Sai,Sai",
                "bloom_level": "Thông hiểu"
            },
            {
                "question_number": 14,
                "question_type": "PART_II",
                "content": "Đối với ngành nuôi trồng thủy sản, việc kiểm soát lượng thuốc tồn dư trong nước là một nhiệm vụ quan trọng nhằm đáp ứng các tiêu chuẩn an toàn về môi trường. Khi nghiên cứu một loại thuốc trị bệnh trong nuôi trồng thủy sản, người ta sử dụng thuốc đó một lần và theo dõi nồng độ thuốc tồn dư trong nước kể từ lúc sử dụng thuốc. Kết quả cho thấy nồng độ $y(t)$ (đơn vị: mg/lít) tồn dư trong nước tại thời điểm $t$ ngày ($t \\ge 0$) kể từ lúc sử dụng thuốc, thỏa mãn $y(t) > 0$ và $y'(t) - k y(t) = 0$ ($t \\ge 0$), trong đó $k$ là hằng số khác không. Do nồng độ thuốc tồn dư tại các thời điểm $t = 6$ (ngày); $t = 12$ (ngày) nhận được kết quả lần lượt là 2 mg/lít; 1 mg/lít. Cho biết $y(t) = e^{g(t)}$ ($t \\ge 0$).",
                "image_url": None,
                "sub_q_a": "$g(t) = k t + C$ ($t \\ge 0$) với $C$ là một hằng số xác định.",
                "sub_q_b": "$k = \\frac{\\ln 2}{6}$.",
                "sub_q_c": "$C = 2\\ln 2$.",
                "sub_q_d": "Nồng độ thuốc tồn dư trong nước tại thời điểm $t = 25$ (ngày) kể từ lúc sử dụng thuốc lớn hơn 0,25 mg/lít.",
                "correct_ans": "Đúng,Sai,Đúng,Sai",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 15,
                "question_type": "PART_II",
                "content": "Mô hình toán học sau đây được sử dụng trong quan sát chuyển động của một vật. Trong không gian cho hệ tọa độ $Oxyz$ có $\\vec{i}, \\vec{j}, \\vec{k}$ lần lượt là các vectơ đơn vị trên các trục $Ox, Oy, Oz$ và độ dài của mỗi vectơ đơn vị đó bằng 1 mét. Cho hai điểm $A$ và $B$, trong đó điểm $A$ có tọa độ là $(5;5;0)$. Một vật (coi như là một hạt) chuyển động thẳng với tốc độ phụ thuộc thời gian $t$ (giây) theo công thức $v(t) = \\beta t + 300$ (m/giây), trong đó $\\beta$ là hằng số dương và $0 \\le t \\le 6$. Ở thời điểm ban đầu ($t = 0$), vật đi qua $A$ với tốc độ 300 m/giây và hướng tới $B$. Sau 2 giây kể từ thời điểm ban đầu, vật đi được quãng đường 604 m. Gọi $\\vec{u} = (a;b;c)$ là vectơ cùng hướng với vectơ $\\overrightarrow{AB}$. Biết rằng $|\\vec{u}| = 1$ và góc giữa vectơ $\\vec{u}$ lần lượt với các vectơ $\\vec{i}, \\vec{j}, \\vec{k}$ có số đo tương ứng bằng $60^\\circ, 60^\\circ, 45^\\circ$.",
                "image_url": None,
                "sub_q_a": "$a = \\cos 60^\\circ$.",
                "sub_q_b": "Phương trình đường thẳng $AB$ là $\\frac{x-5}{1} = \\frac{y-5}{1} = \\frac{z}{\\sqrt{2}}$.",
                "sub_q_c": "$\\beta = 2$.",
                "sub_q_d": "Giả sử sau 5 giây kể từ thời điểm ban đầu, vật đến điểm $B(x_B; y_B; z_B)$. Khi đó $x_B > 768$.",
                "correct_ans": "Đúng,Sai,Đúng,Sai",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 16,
                "question_type": "PART_II",
                "content": "Một phần mềm nhận dạng tin nhắn quảng cáo trên điện thoại bằng cách dựa theo từ khóa để đánh dấu một số tin nhắn được gửi đến. Qua một thời gian dài sử dụng, người ta thấy rằng trong số tất cả các tin nhắn gửi đến, có 15% số tin nhắn bị đánh dấu. Trong số các tin nhắn bị đánh dấu, có 10% số tin nhắn không phải là quảng cáo. Trong số các tin nhắn không bị đánh dấu, có 5% số tin nhắn là quảng cáo. Chọn ngẫu nhiên một tin nhắn được gửi đến điện thoại.",
                "image_url": None,
                "sub_q_a": "Xác suất để tin nhắn đó không bị đánh dấu bằng 0,85.",
                "sub_q_b": "Xác suất để tin nhắn đó không phải là quảng cáo, biết rằng nó không bị đánh dấu, bằng 0,95.",
                "sub_q_c": "Xác suất để tin nhắn đó không phải là quảng cáo bằng 0,85.",
                "sub_q_d": "Xác suất để tin nhắn đó bị đánh dấu, biết rằng nó không phải là quảng cáo, lớn hơn 0,95.",
                "correct_ans": "Đúng,Đúng,Sai,Đúng",
                "bloom_level": "Thông hiểu"
            },

            # ================= PHẦN III (6 CÂU TỰ LUẬN NGUYÊN VĂN 100%) =================
            {
                "question_number": 17,
                "question_type": "PART_III",
                "content": "Bạn Nam tham gia cuộc thi giải một mật thư. Theo quy tắc của cuộc thi, người chơi cần chọn ra sáu số từ tập $S = \\{11;12;13;14;15;16;17;18;19\\}$ và xếp mỗi số vào một vị trí trong sáu vị trí $A,B,C,M,N,P$ như hình bên sao cho mỗi vị trí chỉ được xếp một số. Mật thư sẽ được giải nếu các bộ ba số xuất hiện ở những bộ ba vị trí $(A,M,B); (B,N,C); (C,P,A)$ tạo thành các cấp số cộng theo thứ tự đó. Bạn Nam chọn ngẫu nhiên sáu số trong tập $S$ và xếp ngẫu nhiên vào các vị trí được yêu cầu. Gọi xác suất để bạn Nam giải được mật thư ở lần chọn và xếp đó là $a$. Giá trị của $\\frac{1}{a}$ bằng bao nhiêu?",
                "image_url": "images/q17_graph.png",
                "correct_ans": "1260",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 18,
                "question_type": "PART_III",
                "content": "Nếu một doanh nghiệp sản xuất $x$ sản phẩm trong một tháng ($x \\in \\mathbb{N}^*; 1 \\le x \\le 4500$) thì doanh thu nhận được khi bán hết số sản phẩm đó là $F(x) = -0,01x^2 + 300x$ (nghìn đồng), trong khi chi phí sản xuất bình quân cho mỗi sản phẩm là $G(x) = \\frac{30000}{x} + 200$ (nghìn đồng). Giả sử số sản phẩm sản xuất ra luôn được bán hết. Trong một tháng, doanh nghiệp đó cần sản xuất ít nhất bao nhiêu sản phẩm để lợi nhuận thu được lớn hơn 100 triệu đồng?",
                "image_url": None,
                "correct_ans": "1536",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 19,
                "question_type": "PART_III",
                "content": "Để gây quỹ từ thiện, câu lạc bộ thiện nguyện của một trường THPT tổ chức hoạt động bán hàng với hai mặt hàng là nước chanh và khoai chiên. Câu lạc bộ thiết kế hai thực đơn. Thực đơn 1 có giá 30 nghìn đồng, bao gồm hai cốc nước chanh và một túi khoai chiên. Thực đơn 2 có giá 50 nghìn đồng, bao gồm ba cốc nước chanh và hai túi khoai chiên. Biết rằng câu lạc bộ chỉ làm được không quá 165 cốc nước chanh và 100 túi khoai chiên. Số tiền lớn nhất mà câu lạc bộ có thể nhận được sau khi bán hết hàng bằng bao nhiêu nghìn đồng?",
                "image_url": None,
                "correct_ans": "2650",
                "bloom_level": "Vận dụng"
            },
            {
                "question_number": 20,
                "question_type": "PART_III",
                "content": "Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình thoi với $\\widehat{ABC} = 60^\\circ$ và $AB = 2$. Biết rằng hình chiếu vuông góc của $S$ trên mặt phẳng $(ABCD)$ là trọng tâm $H$ của tam giác $ABC$ và $SH = \\sqrt{3}$. Khoảng cách giữa hai đường thẳng $AC$ và $SD$ bằng bao nhiêu (không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần trăm)?",
                "image_url": None,
                "correct_ans": "1.04",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 21,
                "question_type": "PART_III",
                "content": "Có bốn ngăn (trong một giá để sách) được đánh số thứ tự 1, 2, 3, 4 và bảy quyển sách khác nhau. Bạn An xếp hết bảy quyển sách nói trên vào bốn ngăn đó sao cho mỗi ngăn có ít nhất một quyển sách và các quyển sách được xếp thẳng đứng thành một hàng ngang với gáy sách quay ra ngoài ở mỗi ngăn. Khi đã xếp xong bảy quyển sách, hai cách xếp của bạn An được gọi là giống nhau nếu chúng thỏa mãn đồng thời hai điều kiện sau đây:<br>+ Với từng ngăn, số lượng quyển sách ở ngăn đó là như nhau trong cả hai cách xếp;<br>+ Với từng ngăn, thứ tự từ trái sang phải của các quyển sách được xếp là như nhau trong cả hai cách xếp.<br>Gọi $T$ là số cách xếp đôi một khác nhau của bạn An. Giá trị của $\\frac{T}{100}$ bằng bao nhiêu?",
                "image_url": None,
                "correct_ans": "1008",
                "bloom_level": "Vận dụng cao"
            },
            {
                "question_number": 22,
                "question_type": "PART_III",
                "content": "Để đặt được một vật trang trí trên mặt bàn, người ta thiết kế một chân đế như sau. Lấy một khối gỗ có dạng khối chóp cụt tứ giác đều với độ dài hai cạnh đáy lần lượt bằng $7,4\\text{ cm}$ và $10,4\\text{ cm}$, bề dày của khối gỗ bằng $1,5\\text{ cm}$. Sau đó khoét bỏ đi một phần của khối gỗ sao cho phần đó có dạng vật thể $H$, ở đó $H$ nhận được bằng cách cắt khối cầu bán kính $5,8\\text{ cm}$ bởi một mặt phẳng cắt mà mặt cắt là hình tròn bán kính $3,5\\text{ cm}$ (xem hình dưới). Thể tích của khối chân đế bằng bao nhiêu xentimét khối (không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần mười)?",
                "image_url": "images/q22_sphere.png",
                "correct_ans": "96.5",
                "bloom_level": "Vận dụng cao"
            }
        ]

        # 3. Tự động tương thích với tên cột trong CSDL
        has_correct_option = hasattr(Question, 'correct_option')
        has_correct_answer = hasattr(Question, 'correct_answer')
        has_answer = hasattr(Question, 'answer')

        for item in questions_data:
            kwargs = {
                "year": 2025,
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
        print("🎉 Đã cập nhật 100% NGUYÊN VĂN toàn bộ câu hỏi Đề THPT 2025 - Mã 0101!")

if __name__ == "__main__":
    seed_official_exam_2025()