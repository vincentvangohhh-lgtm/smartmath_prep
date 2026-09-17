from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user 
from app.models import Question, StudentPerformanceProfile, User, ExamResult, StudentAnswer
from app import db
from app.question_generator import generate_parametric_questions, generate_roadmap_questions
from app.services.grader import Grader  
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import json
import random

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exam/dashboard')
@login_required  
def dashboard():
    profile = StudentPerformanceProfile.query.filter_by(student_id=current_user.id).first()
    
    if not profile:
        profile = StudentPerformanceProfile(
            student_id=current_user.id,
            theta_ability=0.5,
            predicted_thpt_score=5.0,  
            topic_mastery=json.dumps({"HAM_SO": [0, 15], "MU_LOGARIT": [0, 14]}),
            weak_topics=json.dumps([])
        )
        db.session.add(profile)
        db.session.commit()
        
    results = ExamResult.query.filter_by(user_id=current_user.id).order_by(ExamResult.id.desc()).all()
    return render_template('exam/dashboard.html', profile=profile, results=results, user=current_user)

@exam_bp.route('/take/<int:exam_id>', methods=['GET', 'POST'])
@exam_bp.route('/exam/take/<int:exam_id>', methods=['GET', 'POST'])
@login_required  
def take_exam(exam_id):
    current_exam_type = session.get('current_exam_type', 'standard_22')

    if current_exam_type == 'roadmap':
        day_id = session.get('roadmap_day_id', 1)
        exam_title = f"📖 LỘ TRÌNH ÔN TẬP NĂNG LỰC - NGÀY {day_id} (Mã đề {exam_id})"
        exam_duration = 45
    elif current_exam_type == 'millionaire':
        exam_title = f"🏆 AI LÀ TRIỆU PHÚ TOÁN HỌC - Mã đề {exam_id}"
        exam_duration = 45
    elif current_exam_type == 'adaptive_18':
        exam_title = f"⚡ Đề khảo sát năng lực thích ứng rút gọn 18 câu - Mã số {exam_id}"
        exam_duration = 60
    elif current_exam_type == 'official':
        year = session.get('official_year', 2025)
        code_id = session.get('official_code', '0101')
        exam_title = f"🏛️ ĐỀ THI CHÍNH THỨC TỐT NGHIỆP THPT NĂM {year} - MÔN TOÁN (MÃ ĐỀ {code_id})"
        exam_duration = 90
    else:
        exam_title = f"📝 Đề thi Chuẩn THPT Quốc Gia Môn Toán (22 câu) - Mã số {exam_id}"
        exam_duration = 90

    mock_exam = {
        "id": exam_id,
        "title": exam_title,
        "duration": exam_duration,
        "is_survey": True
    }

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        try:
            duration_seconds = int(request.form.get('spent_time', exam_duration * 60))
        except ValueError:
            duration_seconds = exam_duration * 60
            
        result = Grader.grade_exam(current_user, mock_exam, user_answers, duration_seconds)
        result.duration_seconds = duration_seconds
        
        calculated_theta = round((result.score - 5.0) / 5.0 * 2.5, 2)
        current_user.theta_ability = calculated_theta
        
        profile = StudentPerformanceProfile.query.filter_by(student_id=current_user.id).first()
        if profile:
            profile.theta_ability = calculated_theta
            profile.predicted_thpt_score = round(result.score, 1)

        if result.score >= 8.0:
            current_user.current_level = "Giỏi"
        elif result.score >= 6.5:
            current_user.current_level = "Khá"
        elif result.score >= 5.0:
            current_user.current_level = "Trung bình"
        else:
            current_user.current_level = "Yếu"
            
        db.session.add(result)
        db.session.add(current_user)
        db.session.commit()
        
        flash("Nộp bài thi thành công!", "success")
        return redirect(url_for('exam.exam_result', result_id=result.id))

    if current_exam_type == 'official':
        year = session.get('official_year', 2025)
        code_id = str(session.get('official_code', '0101')).strip()
        
        questions_list = Question.query.filter_by(year=year, code_id=code_id)\
                                     .order_by(Question.question_number.asc()).all()

        return render_template('exam/take_official.html', exam_id=exam_id, exam=mock_exam, questions=questions_list, year=year, code_id=code_id)

    else:
        generated_qids = session.get('generated_qids', [])
        
        if generated_qids:
            questions_unordered = Question.query.filter(Question.id.in_(generated_qids)).all()
            q_map = {q.id: q for q in questions_unordered}
            questions_list = [q_map[qid] for qid in generated_qids if qid in q_map]
        else:
            if current_exam_type in ['millionaire', 'roadmap']:
                questions_list = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_I").limit(15).all()
            elif current_exam_type == 'adaptive_18':
                p1 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_I").limit(12).all()
                p2 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_II").limit(4).all()
                p3 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_III").limit(2).all()
                questions_list = p1 + p2 + p3
            else:
                p1 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_I").limit(12).all()
                p2 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_II").limit(4).all()
                p3 = Question.query.filter(Question.year.is_(None), Question.question_type == "PART_III").limit(6).all()
                questions_list = p1 + p2 + p3

        return render_template('exam/take.html', exam_id=exam_id, exam=mock_exam, questions=questions_list)

@exam_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        exam_type = request.form.get('exam_type', 'standard_22')
        session['current_exam_type'] = exam_type
        
        if exam_type == 'official':
            session['official_year'] = request.form.get('year', type=int, default=2025)
            session['official_code'] = request.form.get('code_id', '').strip()
    else:
        # Xử lý khi nhận phương thức GET từ nút "Làm lại"
        exam_type = session.get('current_exam_type', 'standard_22')

    if exam_type == 'official':
        year = session.get('official_year', 2025)
        code_id = session.get('official_code', '')
        
        if not code_id or code_id == 'random':
            available_codes = db.session.query(Question.code_id).filter_by(year=year).distinct().all()
            if available_codes:
                code_id = random.choice([c[0] for c in available_codes if c[0]])
            else:
                code_id = '0101'
                
        session['official_year'] = year
        session['official_code'] = code_id
        flash(f"🏛️ Đã tải thành công Đề thi Chính thức THPT Quốc gia Năm {year} - Mã đề {code_id}!", "success")
        
        random_exam_id = random.randint(100, 999)
        return redirect(url_for('exam.take_exam', exam_id=random_exam_id))
    
    db.session.query(Question).filter(Question.year.is_(None)).delete()
    
    final_questions = []

    if exam_type == 'millionaire':
        raw_questions = generate_parametric_questions()
        part_1_questions = [q for q in raw_questions if q.question_type == "PART_I"]
        
        while len(part_1_questions) < 15:
            more_q = generate_parametric_questions()
            part_1_questions.extend([q for q in more_q if q.question_type == "PART_I"])
            
        millionaire_questions = part_1_questions[:15]
        for idx, q in enumerate(millionaire_questions):
            q.question_number = idx + 1
            if idx < 5:
                q.bloom_level = f"Chặng 1 - Câu {idx+1}: Khởi Động (Dễ)"
            elif idx < 10:
                q.bloom_level = f"Chặng 2 - Câu {idx+1}: Thử Thách (Trung Bình)"
            else:
                q.bloom_level = f"Chặng 3 - Câu {idx+1}: Chinh Phục (Vận Dụng Cao)"
            db.session.add(q)
            
        final_questions = millionaire_questions
        flash("🏆 Đã khởi tạo thành công 15 cột mốc 'Ai Là Triệu Phú Toán Học'!", "warning")

    elif exam_type == 'adaptive_18':
        raw_q = generate_parametric_questions()
        p1 = [q for q in raw_q if q.question_type == "PART_I"]
        p2 = [q for q in raw_q if q.question_type == "PART_II"]
        p3 = [q for q in raw_q if q.question_type == "PART_III"]

        while len(p1) < 12 or len(p2) < 4 or len(p3) < 2:
            more_q = generate_parametric_questions()
            p1.extend([q for q in more_q if q.question_type == "PART_I"])
            p2.extend([q for q in more_q if q.question_type == "PART_II"])
            p3.extend([q for q in more_q if q.question_type == "PART_III"])

        final_18 = p1[:12] + p2[:4] + p3[:2]
        for idx, q in enumerate(final_18):
            q.question_number = idx + 1
            db.session.add(q)
            
        final_questions = final_18
        flash("⚡ Đã khởi tạo Đề Thích Ứng Rút Gọn chuẩn 18 câu!", "info")

    else: 
        raw_q = generate_parametric_questions()
        p1 = [q for q in raw_q if q.question_type == "PART_I"]
        p2 = [q for q in raw_q if q.question_type == "PART_II"]
        p3 = [q for q in raw_q if q.question_type == "PART_III"]

        while len(p1) < 12 or len(p2) < 4 or len(p3) < 6:
            more_q = generate_parametric_questions()
            p1.extend([q for q in more_q if q.question_type == "PART_I"])
            p2.extend([q for q in more_q if q.question_type == "PART_II"])
            p3.extend([q for q in more_q if q.question_type == "PART_III"])

        final_22 = p1[:12] + p2[:4] + p3[:6]
        for idx, q in enumerate(final_22):
            q.question_number = idx + 1
            db.session.add(q)
            
        final_questions = final_22
        flash("📝 Đã khởi tạo Đề Thi Chuẩn THPT Quốc Gia Môn Toán chuẩn 22 câu!", "success")

    db.session.commit()
    
    session['generated_qids'] = [q.id for q in final_questions]

    random_exam_id = random.randint(100, 999)
    return redirect(url_for('exam.take_exam', exam_id=random_exam_id))

@exam_bp.route('/retry/<int:exam_id>', methods=['GET'])
@login_required
def retry_exam(exam_id):
    # exam_id nhận được từ dashboard chính là id của bảng lịch sử (ExamResult.id)
    result = ExamResult.query.filter_by(id=exam_id, user_id=current_user.id).first_or_404()
    
    # Truy vấn các câu hỏi thuộc bài thi lịch sử đó thông qua bảng StudentAnswer
    answers = StudentAnswer.query.filter_by(result_id=result.id).all()
    
    if answers:
        first_q = answers[0].question
        if first_q and first_q.year is not None:
            # Nếu là đề thi chính thức, khôi phục lại đúng năm và mã đề gốc của lần thi đó
            session['current_exam_type'] = 'official'
            session['official_year'] = first_q.year
            session['official_code'] = first_q.code_id
        else:
            # Nếu là đề tự sinh, phân loại dựa vào tổng số câu hỏi trong bài
            total_q = len(answers)
            if total_q == 15:
                session['current_exam_type'] = 'millionaire'
            elif total_q == 18:
                session['current_exam_type'] = 'adaptive_18'
            else:
                session['current_exam_type'] = 'standard_22'
    else:
        # Fallback mặc định an toàn
        session['current_exam_type'] = 'standard_22'
        
    # Chuyển hướng đến generate để tạo bộ câu hỏi mới đúng chuẩn loại đề đó
    return redirect(url_for('exam.generate'))
@exam_bp.route('/exam/result/<int:result_id>')
@login_required
def exam_result(result_id):
    result = ExamResult.query.filter_by(id=result_id, user_id=current_user.id).first_or_404()
    profile = StudentPerformanceProfile.query.filter_by(student_id=current_user.id).first()
    
    student_answers = StudentAnswer.query.filter_by(result_id=result.id).all()
    answers_map = {sa.question_id: sa for sa in student_answers}
    
    q_ids = list(answers_map.keys())
    all_questions = Question.query.filter(Question.id.in_(q_ids)).all() if q_ids else []
    
    questions_data = []
    for q in all_questions:
        if q.id in answers_map:
            sa = answers_map[q.id]
            q.user_answer = sa.selected_option
            q.is_correct = sa.is_correct
        else:
            q.user_answer = "Bỏ trống"
            q.is_correct = False
            
        questions_data.append(q)
        
    return render_template('exam/result.html', profile=profile, result=result, questions=questions_data)

@exam_bp.route('/roadmap/practice/<int:day_id>')
@login_required
def roadmap_practice(day_id):
    if day_id not in [1, 2, 3]:
        flash("Ngày ôn tập trong lộ trình năng lực không hợp lệ!", "danger")
        return redirect(url_for('exam.dashboard'))
    
    try:
        db.session.query(Question).filter(Question.year.is_(None)).delete()
        roadmap_questions = generate_roadmap_questions(day_id)
        for idx, q in enumerate(roadmap_questions):
            q.question_number = idx + 1
            db.session.add(q)
            
        db.session.commit()
        
        session['current_exam_type'] = 'roadmap'
        session['roadmap_day_id'] = day_id
        session['generated_qids'] = [q.id for q in roadmap_questions]
        
        random_exam_id = random.randint(1000, 9999)
        flash(f"Khởi tạo thành công bộ 15 câu ôn tập cho Ngày {day_id}!", "success")
        return redirect(url_for('exam.take_exam', exam_id=random_exam_id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Có lỗi khi khởi tạo đề luyện tập: {str(e)}", "danger")
        return redirect(url_for('exam.dashboard'))

@exam_bp.route('/formulas')
def formula_layout():
    formula_type = request.args.get('type', 'algebra')
    
    algebra_segments = {
        'chuong_1': {
            'title': 'Chương 1: Ứng Dụng Đạo Hàm Để Khảo Sát Đồ Thị Hàm Số',
            'lessons': [
                {
                    'lesson_name': '1. Tính Đơn Điệu Của Hàm Số',
                    'formulas': [
                        {
                            'id': 'f_1_1',
                            'name': 'Điều Kiện Đơn Điệu Của Hàm Số',
                            'latex_code': 'y\' \\ge 0 \\quad (\\text{Đồng biến trên } K); \\qquad y\' \\le 0 \\quad (\\text{Nghịch biến trên } K)',
                            'explanation': 'Cho hàm số $y=f(x)$ có đạo hàm trên $K$. $f\'(x) \\ge 0$ mọi $x \\in K$ (dấu bằng tại hữu hạn điểm) thì hàm số đồng biến trên $K$. Tương tự $f\'(x) \\le 0$ thì nghịch biến.',
                            'common_errors': 'Sử dụng ký hiệu hợp $\\cup$ khi kết luận khoảng đơn điệu (Ví dụ: $(-\\infty;-1) \\cup (1;+\\infty)$ là SAI). Phải ghi từ "và" hoặc dấu chấm phẩy ";".',
                            'memory_trick': 'Đạo hàm Dương - Đồ thị Đi lên; Đạo hàm Âm - Đồ thị Đi xuống.',
                            'example_basic': {
                                'question': 'Tìm khoảng đơn điệu của hàm số $y = x^3 - 3x$.',
                                'solution': 'Ta có $y\' = 3x^2 - 3 = 0 \\Leftrightarrow x = \\pm 1$. Bảng xét dấu: $y\' > 0$ trên $(-\\infty; -1)$ và $(1; +\\infty)$, $y\' < 0$ trên $(-1; 1)$.',
                                'final_answer': 'Đồng biến trên $(-\\infty;-1)$ và $(1;+\\infty)$; nghịch biến trên $(-1;1)$.'
                            },
                            'example_advanced': {
                                'question': 'Tìm tất cả giá trị $m$ để hàm số $y = \\frac{1}{3}x^3 - mx^2 + (m+2)x + 1$ đồng biến trên $\\mathbb{R}$.',
                                'solution': '$y\' = x^2 - 2mx + m + 2$. Hàm đồng biến trên $\\mathbb{R} \\Leftrightarrow y\' \\ge 0, \\forall x \\in \\mathbb{R} \\Leftrightarrow \\Delta\' = m^2 - m - 2 \\le 0 \\Leftrightarrow -1 \\le m \\le 2$.',
                                'final_answer': '$-1 \\le m \\le 2$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Cực Trị Của Hàm Số',
                    'formulas': [
                        {
                            'id': 'f_1_2',
                            'name': 'Điều Kiện Đổi Dấu Cực Trị',
                            'latex_code': 'x_0 \\text{ là Cực Đại } \\Leftrightarrow y\' \\text{ đổi dấu từ } (+) \\to (-); \\quad x_0 \\text{ là Cực Tiểu } \\Leftrightarrow y\' \\text{ đổi dấu từ } (-) \\to (+)',
                            'explanation': 'Cực trị là điểm mà tại đó đạo hàm $f\'(x)$ bằng 0 (hoặc không xác định) và đổi dấu khi đi qua điểm đó.',
                            'common_errors': 'Nhầm lẫn giữa 3 khái niệm: Điểm cực trị của hàm số ($x_0$), Giá trị cực trị ($y_0 = f(x_0)$), và Điểm cực trị của đồ thị ($M(x_0; y_0)$).',
                            'memory_trick': 'Dương sang Âm - Lên đỉnh Cực Đại; Âm sang Dương - Chìm xuống Cực Tiểu.',
                            'example_basic': {
                                'question': 'Tìm giá trị cực đại của hàm số $y = -x^3 + 3x + 1$.',
                                'solution': '$y\' = -3x^2 + 3 = 0 \\Leftrightarrow x = \\pm 1$. Qua $x = 1$, $y\'$ đổi dấu từ (+) sang (-). Giá trị cực đại $y(1) = 3$.',
                                'final_answer': '$y_{CĐ} = 3$'
                            },
                            'example_advanced': {
                                'question': 'Tìm $m$ để hàm số $y = x^4 - 2mx^2 + 1$ có 3 điểm cực trị.',
                                'solution': '$y\' = 4x^3 - 4mx = 4x(x^2 - m)$. Hàm số có 3 cực trị $\\Leftrightarrow y\' = 0$ có 3 nghiệm phân biệt $\\Leftrightarrow m > 0$.',
                                'final_answer': '$m > 0$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '3. Giá Trị Lớn Nhất & Giá Trị Nhỏ Nhất (GTLN - GTNN)',
                    'formulas': [
                        {
                            'id': 'f_1_3',
                            'name': 'Quy Tắc Tìm GTLN & GTNN Trên Đoạn [a; b]',
                            'latex_code': '\\max_{[a;b]} f(x) = \\max \\{ f(a), f(b), f(x_i) \\}; \\quad \\min_{[a;b]} f(x) = \\min \\{ f(a), f(b), f(x_i) \\}',
                            'explanation': 'Để tìm GTLN, GTNN của $f(x)$ liên tục trên đoạn $[a; b]$, ta tính các nghiệm $x_i \\in (a; b)$ của $f\'(x)=0$, sau đó so sánh các giá trị $f(a), f(b), f(x_i)$.',
                            'common_errors': 'Quên loại các nghiệm $x_i$ nằm ngoài khoảng $(a; b)$.',
                            'memory_trick': 'Tính hai đầu mút - Thêm nghiệm trong khoảng - So sánh chọn Lớn/Nhỏ.',
                            'example_basic': {
                                'question': 'Tìm GTNN của $y = x^3 - 3x + 5$ trên đoạn $[0; 2]$.',
                                'solution': '$y\' = 3x^2 - 3 = 0 \\Leftrightarrow x = 1 \\in (0; 2)$ (loại $x = -1$). Tính $f(0) = 5, f(1) = 3, f(2) = 7$.',
                                'final_answer': '$\\min_{[0;2]} y = 3$ tại $x = 1$'
                            },
                            'example_advanced': {
                                'question': 'Tìm $m$ để $\\max_{[0;1]} (x + m^2) = 5$.',
                                'solution': 'Hàm số $f(x) = x + m^2$ đồng biến trên $[0;1]$ nên $\\max_{[0;1]} f(x) = f(1) = 1 + m^2$. Ta có $1 + m^2 = 5 \\Leftrightarrow m = \\pm 2$.',
                                'final_answer': '$m = \\pm 2$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '4. Đường Tiệm Cận Của Đồ Thị Hàm Số',
                    'formulas': [
                        {
                            'id': 'f_1_4',
                            'name': 'Đường Tiệm Cận Đứng & Tiệm Cận Ngang',
                            'latex_code': '\\text{TCĐ: } \\lim_{x \\to x_0^{\\pm}} y = \\pm \\infty \\Rightarrow x = x_0; \\qquad \\text{TCN: } \\lim_{x \\to \\pm \\infty} y = y_0 \\Rightarrow y = y_0',
                            'explanation': 'Đường tiệm cận đứng xuất hiện tại điểm gián đoạn của mẫu số; tiệm cận ngang xuất hiện khi $x$ tiến ra vô cực.',
                            'common_errors': 'Nhầm nghiệm của mẫu số luôn là TCĐ mà quên kiểm tra xem nghiệm đó có triệt tiêu với tử số hay không.',
                            'memory_trick': 'Tiệm cận Đứng - x tiến tới Nghiệm mẫu; Tiệm cận Ngang - x tiến tới Vô cùng.',
                            'example_basic': {
                                'question': 'Tìm tiệm cận đứng và tiệm cận ngang của $y = \\frac{2x + 1}{x - 1}$.',
                                'solution': '$\\lim_{x \\to \\pm\\infty} \\frac{2x+1}{x-1} = 2 \\Rightarrow TCN \\ y = 2$. $\\lim_{x \\to 1^+} \\frac{2x+1}{x-1} = +\\infty \\Rightarrow TCĐ \\ x = 1$.',
                                'final_answer': 'TCĐ: $x = 1$, TCN: $y = 2$'
                            },
                            'example_advanced': {
                                'question': 'Tìm số đường tiệm cận của đồ thị $y = \\frac{x - 1}{x^2 - 1}$.',
                                'solution': '$y = \\frac{x - 1}{(x-1)(x+1)} = \\frac{1}{x+1}$ với $x \\neq 1$. TCN $y = 0$, TCĐ $x = -1$ (tại $x=1$ bị triệt tiêu).',
                                'final_answer': '2 đường tiệm cận ($x = -1$ và $y = 0$)'
                            }
                        }
                    ]
                }
            ]
        },
        'chuong_2': {
            'title': 'Chương 2: Các Số Đặc Trưng Đo Mức Độ Phân Tán Của Mẫu Số Liệu Ghép Nhóm',
            'lessons': [
                {
                    'lesson_name': '1. Khoảng Biến Thiên & Khoảng Tứ Phân Vị',
                    'formulas': [
                        {
                            'id': 'f_2_1',
                            'name': 'Khoảng Biến Thiên & Khoảng Tứ Phân Vị Ghép Nhóm',
                            'latex_code': 'R = a_{k+1} - a_1; \\qquad \\Delta_Q = Q_3 - Q_1',
                            'explanation': 'Khoảng biến thiên $R$ đo độ chênh lệch giữa đầu và cuối nhóm. Khoảng tứ phân vị $\\Delta_Q$ đo độ phân tán của $50\\%$ số liệu trung tâm.',
                            'common_errors': 'Lấy giá trị đại diện nhóm để tính khoảng biến thiên thay vì lấy ranh giới đầu/cuối của nhóm ghép.',
                            'memory_trick': 'Biến thiên lấy Cuối trừ Đầu; Tứ phân vị lấy Q3 trừ Q1.',
                            'example_basic': {
                                'question': 'Cho mẫu số liệu ghép nhóm có $Q_1 = 12.5$ và $Q_3 = 24.8$. Tính khoảng tứ phân vị.',
                                'solution': '$\\Delta_Q = Q_3 - Q_1 = 24.8 - 12.5 = 12.3$.',
                                'final_answer': '$\\Delta_Q = 12.3$'
                            },
                            'example_advanced': {
                                'question': 'Cho mẫu số liệu có các nhóm $[10; 20), [20; 30), [30; 40)$. Tính khoảng biến thiên $R$.',
                                'solution': '$a_1 = 10, a_4 = 40 \\Rightarrow R = 40 - 10 = 30$.',
                                'final_answer': '$R = 30$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Phương Sai & Độ Lệch Chuẩn',
                    'formulas': [
                        {
                            'id': 'f_2_2',
                            'name': 'Phương Sai & Độ Lệch Chuẩn Mẫu Số Liệu Ghép Nhóm',
                            'latex_code': 's^2 = \\frac{1}{n} \\sum_{i=1}^k n_i (x_i - \\bar{x})^2; \\qquad s = \\sqrt{s^2}',
                            'explanation': 'Với $x_i$ là giá trị đại diện của nhóm $i$, $n_i$ là tần số nhóm, $n$ là cỡ mẫu, $\\bar{x}$ là số trung bình.',
                            'common_errors': 'Quên căn bậc hai của phương sai khi đề bài hỏi Độ lệch chuẩn.',
                            'memory_trick': 'Phương sai là Trung bình độ lệch bình phương; Độ lệch chuẩn lấy Căn phương sai.',
                            'example_basic': {
                                'question': 'Mẫu số liệu ghép nhóm có phương sai $s^2 = 9$. Tính độ lệch chuẩn $s$.',
                                'solution': '$s = \\sqrt{s^2} = \\sqrt{9} = 3$.',
                                'final_answer': '$s = 3$'
                            },
                            'example_advanced': {
                                'question': 'Nhóm A có độ lệch chuẩn $s_A = 2.1$, Nhóm B có $s_B = 4.5$. Nhóm nào có độ phân tán đồng đều hơn?',
                                'solution': 'Độ lệch chuẩn nhỏ hơn thể hiện số liệu tập trung quanh số trung bình hơn.',
                                'final_answer': 'Nhóm A phân tán đồng đều hơn'
                            }
                        }
                    ]
                }
            ]
        },
        'chuong_3': {
            'title': 'Chương 3: Nguyên Hàm, Tích Phân Và Ứng Dụng',
            'lessons': [
                {
                    'lesson_name': '1. Bảng Nguyên Hàm Cơ Bản',
                    'formulas': [
                        {
                            'id': 'f_3_1',
                            'name': 'Công Thức Nguyên Hàm Cơ Bản',
                            'latex_code': '\\int x^n dx = \\frac{x^{n+1}}{n+1} + C \\ (n \\neq -1); \\quad \\int \\frac{1}{x} dx = \\ln|x| + C; \\quad \\int e^x dx = e^x + C',
                            'explanation': 'Nguyên hàm là phép toán ngược của đạo hàm. Bất kỳ hàm số liên tục nào cũng có nguyên hàm.',
                            'common_errors': 'Quên hằng số $+ C$ khi làm bài tự luận hoặc quên dấu trị tuyệt đối $\\ln|x|$.',
                            'memory_trick': 'Nguyên hàm - Tăng mũ chia mũ mới; Mũ e giữ nguyên; Dấu sin cos ngược với đạo hàm.',
                            'example_basic': {
                                'question': 'Tìm nguyên hàm của $f(x) = 3x^2 + e^x$.',
                                'solution': '$\\int (3x^2 + e^x) dx = 3 \\cdot \\frac{x^3}{3} + e^x + C = x^3 + e^x + C$.',
                                'final_answer': '$F(x) = x^3 + e^x + C$'
                            },
                            'example_advanced': {
                                'question': 'Tìm nguyên hàm $F(x)$ của $f(x) = \\sin 2x$ biết $F(0) = 1$.',
                                'solution': '$F(x) = -\\frac{1}{2}\\cos 2x + C$. Thay $x=0$: $-\\frac{1}{2}(1) + C = 1 \\Rightarrow C = \\frac{3}{2}$.',
                                'final_answer': '$F(x) = -\\frac{1}{2}\\cos 2x + \\frac{3}{2}$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Tính Chất Của Tích Phân',
                    'formulas': [
                        {
                            'id': 'f_3_2',
                            'name': 'Định Nghĩa & Tính Chất Chèn Cận Tích Phân',
                            'latex_code': '\\int_a^b f(x) dx = F(b) - F(a); \\qquad \\int_a^b f(x) dx = \\int_a^c f(x) dx + \\int_c^b f(x) dx',
                            'explanation': 'Tích phân xác định không phụ thuộc vào biến số mà chỉ phụ thuộc vào các cận $a, b$ và dạng hàm $f$.',
                            'common_errors': 'Tính $F(a) - F(b)$ (lấy cận dưới trừ cận trên) dẫn đến bị ngược dấu kết quả.',
                            'memory_trick': 'Tích phân Cận trên trừ Cận dưới; Chèn cận trung gian cắt đôi tích phân.',
                            'example_basic': {
                                'question': 'Cho $\\int_1^3 f(x)dx = 4$ và $\\int_3^5 f(x)dx = 6$. Tính $\\int_1^5 f(x)dx$.',
                                'solution': '$\\int_1^5 f(x)dx = \\int_1^3 f(x)dx + \\int_3^5 f(x)dx = 4 + 6 = 10$.',
                                'final_answer': '10'
                            },
                            'example_advanced': {
                                'question': 'Biết $\\int_0^2 f(x)dx = 5$. Tính $I = \\int_0^2 [2f(x) - 3] dx$.',
                                'solution': '$I = 2\\int_0^2 f(x)dx - \\int_0^2 3dx = 2(5) - 3(2 - 0) = 10 - 6 = 4$.',
                                'final_answer': '$I = 4$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '3. Ứng Dụng Tích Phân Tính Diện Tích & Thể Tích',
                    'formulas': [
                        {
                            'id': 'f_3_3',
                            'name': 'Công Thức Tính Diện Tích Hình Phẳng & Thể Tích Tròn Xoay',
                            'latex_code': 'S = \\int_a^b |f(x) - g(x)| dx; \\qquad V = \\pi \\int_a^b f^2(x) dx',
                            'explanation': 'Tính diện tích miền giới hạn bởi hai đường $y=f(x), y=g(x)$ và hai đường thẳng $x=a, x=b$. Khối tròn xoay tạo thành khi quay quanh trục $Ox$.',
                            'common_errors': 'Quên hằng số $\\pi$ hoặc quên bình phương $f^2(x)$ khi tính thể tích $V$.',
                            'memory_trick': 'Diện tích tích phân Trị tuyệt đối; Thể tích nhân Pi, Bình phương hàm.',
                            'example_basic': {
                                'question': 'Tính thể tích $V$ quay quanh $Ox$ giới hạn bởi $y = \\sqrt{x}, y = 0, x = 0, x = 4$.',
                                'solution': '$V = \\pi \\int_0^4 (\\sqrt{x})^2 dx = \\pi \\int_0^4 x dx = \\pi \\left[ \\frac{x^2}{2} \\right]_0^4 = 8\\pi$.',
                                'final_answer': '$V = 8\\pi$'
                            },
                            'example_advanced': {
                                'question': 'Tính diện tích hình phẳng giới hạn bởi $y = x^2$ và $y = x + 2$.',
                                'solution': 'Hoành độ giao điểm $x^2 - x - 2 = 0 \\Leftrightarrow x = -1, x = 2$. $S = \\int_{-1}^2 |x^2 - x - 2| dx = \\frac{9}{2}$.',
                                'final_answer': '$S = \\frac{9}{2}$'
                            }
                        }
                    ]
                }
            ]
        },
        'chuong_4': {
            'title': 'Chương 4: Xác Suất Điều Kiện Và Công Thức Xác Suất Toàn Phần',
            'lessons': [
                {
                    'lesson_name': '1. Xác Suất Có Điều Kiện',
                    'formulas': [
                        {
                            'id': 'f_4_1',
                            'name': 'Công Thức Xác Suất Điều Kiện & Nhân Xác Suất',
                            'latex_code': 'P(A|B) = \\frac{P(A \\cap B)}{P(B)} \\quad (P(B) > 0); \\qquad P(A \\cap B) = P(B) \\cdot P(A|B)',
                            'explanation': 'Xác suất của biến cố A với điều kiện biến cố B đã xảy ra.',
                            'common_errors': 'Nhầm lẫn giữa $P(A|B)$ và $P(B|A)$ (Biến cố điều kiện biết trước luôn ở mẫu số).',
                            'memory_trick': 'Xác suất A khi biết B: Giao hai biến cố chia xác suất B.',
                            'example_basic': {
                                'question': 'Cho $P(B) = 0.5$ và $P(A \\cap B) = 0.2$. Tính $P(A|B)$.',
                                'solution': '$P(A|B) = \\frac{P(A \\cap B)}{P(B)} = \\frac{0.2}{0.5} = 0.4$.',
                                'final_answer': '$P(A|B) = 0.4$'
                            },
                            'example_advanced': {
                                'question': 'Rút lần lượt 2 lá bài từ bộ 52 lá không hoàn lại. Tính xác suất lá thứ 2 là K biết lá thứ 1 là K.',
                                'solution': 'Khi lá thứ 1 đã là K, bộ bài còn 51 lá với 3 lá K. Do đó $P(K_2|K_1) = \\frac{3}{51} = \\frac{1}{17}$.',
                                'final_answer': '$\\frac{1}{17}$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Công Thức Xác Suất Toàn Phần & Bayes',
                    'formulas': [
                        {
                            'id': 'f_4_2',
                            'name': 'Công Thức Xác Suất Toàn Phần & Bayes',
                            'latex_code': 'P(B) = P(A) \\cdot P(B|A) + P(\\overline{A}) \\cdot P(B|\\overline{A}); \\qquad P(A|B) = \\frac{P(A) \\cdot P(B|A)}{P(B)}',
                            'explanation': 'Cho phép tính xác suất của biến cố B thông qua các kịch bản của nhóm biến cố đầy đủ.',
                            'common_errors': 'Áp dụng sai tỷ lệ phần trăm biến cố $A$ và $\\overline{A}$ làm tổng không bằng 1.',
                            'memory_trick': 'Toàn phần bằng Tổng xác suất từng nhánh; Bayes lấy Nhánh đó chia Tổng toàn phần.',
                            'example_basic': {
                                'question': 'Máy I làm $60\\%$ sản phẩm ($P(A)=0.6$), Máy II làm $40\\%$ ($P(\\overline{A})=0.4$). Tỷ lệ phế phẩm Máy I là $1\\%$, Máy II là $2\\%$. Tính tỷ lệ phế phẩm chung.',
                                'solution': '$P(B) = 0.6 \\times 0.01 + 0.4 \\times 0.02 = 0.014 \\ (1.4\\%)$.',
                                'final_answer': '$1.4\\$'
                            },
                            'example_advanced': {
                                'question': 'Ở ví dụ trên, biết sản phẩm chọn ra là phế phẩm, tính xác suất sản phẩm đó do Máy I làm.',
                                'solution': 'Áp dụng công thức Bayes: $P(A|B) = \\frac{P(A) \\cdot P(B|A)}{P(B)} = \\frac{0.6 \\times 0.01}{0.014} = \\frac{3}{7}$.',
                                'final_answer': '$\\frac{3}{7}$'
                            }
                        }
                    ]
                }
            ]
        }
    }

    geometry_segments = {
        'chuong_5': {
            'title': 'Chương 5: Vectơ Và Hệ Tọa Độ Trong Không Gian',
            'lessons': [
                {
                    'lesson_name': '1. Tọa Độ Của Vectơ & Độ Dài',
                    'formulas': [
                        {
                            'id': 'f_5_1',
                            'name': 'Độ Dài Vectơ & Khoảng Cách Hai Điểm',
                            'latex_code': '|\\vec{u}| = \\sqrt{x^2 + y^2 + z^2}; \\qquad AB = \\sqrt{(x_B - x_A)^2 + (y_B - y_A)^2 + (z_B - z_A)^2}',
                            'explanation': 'Toạ độ vectơ $\\vec{u} = (x; y; z)$ tương ứng $\\vec{u} = x\\vec{i} + y\\vec{j} + z\\vec{k}$.',
                            'common_errors': 'Lấy tọa độ điểm A trừ B khi tính vectơ $\\overrightarrow{AB}$ (đúng là Sau trừ Đầu: B trừ A).',
                            'memory_trick': 'Độ dài bằng Căn tổng bình phương tọa độ; Vectơ AB lấy Sau trừ Đầu.',
                            'example_basic': {
                                'question': 'Tính độ dài vectơ $\\vec{u} = (2; -2; 1)$.',
                                'solution': '$|\\vec{u}| = \\sqrt{2^2 + (-2)^2 + 1^2} = \\sqrt{9} = 3$.',
                                'final_answer': '$|\\vec{u}| = 3$'
                            },
                            'example_advanced': {
                                'question': 'Cho $A(1; 2; 3)$ và $B(3; 0; 2)$. Tìm tọa độ trung điểm $M$ của $AB$.',
                                'solution': '$M\\left(\\frac{1+3}{2}; \\frac{2+0}{2}; \\frac{3+2}{2}\\right) = M\\left(2; 1; \\frac{5}{2}\\right)$.',
                                'final_answer': '$M\\left(2; 1; \\frac{5}{2}\\right)$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Tích Vô Hướng & Tích Có Hướng',
                    'formulas': [
                        {
                            'id': 'f_5_2',
                            'name': 'Biểu Thức Tọa Độ Tích Vô Hướng & Tích Có Hướng',
                            'latex_code': '\\vec{u} \\cdot \\vec{v} = x_1 x_2 + y_1 y_2 + z_1 z_2; \\qquad [\\vec{u}, \\vec{v}] = (y_1 z_2 - y_2 z_1; \\ z_1 x_2 - z_2 x_1; \\ x_1 y_2 - x_2 y_1)',
                            'explanation': 'Tích vô hướng cho ra một số; Tích có hướng cho ra một vectơ vuông góc với cả hai vectơ ban đầu.',
                            'common_errors': 'Nhầm dấu thành phần tung độ (phần giữa) của tích có hướng.',
                            'memory_trick': 'Vô hướng ra Số (Hoành x Hoành + Tung x Tung + Cao x Cao); Có hướng ra Vectơ vuông góc cả hai.',
                            'example_basic': {
                                'question': 'Cho $\\vec{u} = (1; 0; 2)$ và $\\vec{v} = (2; 1; -1)$. Tính $\\vec{u} \\cdot \\vec{v}$.',
                                'solution': '$\\vec{u} \\cdot \\vec{v} = 1(2) + 0(1) + 2(-1) = 0 \\Rightarrow \\vec{u} \\perp \\vec{v}$.',
                                'final_answer': '$0$'
                            },
                            'example_advanced': {
                                'question': 'Tính diện tích tam giác $ABC$ biết $A(1;0;0), B(0;0;1), C(2;1;1)$.',
                                'solution': '$\\overrightarrow{AB} = (-1;0;1), \\overrightarrow{AC} = (1;1;1) \\Rightarrow [\\overrightarrow{AB}, \\overrightarrow{AC}] = (-1; 2; -1)$. $S = \\frac{1}{2} |[\\overrightarrow{AB}, \\overrightarrow{AC}]| = \\frac{\\sqrt{6}}{2}$.',
                                'final_answer': '$S = \\frac{\\sqrt{6}}{2}$'
                            }
                        }
                    ]
                }
            ]
        },
        'chuong_6': {
            'title': 'Chương 6: Phương Pháp Tọa Độ Trong Không Gian (Oxyz)',
            'lessons': [
                {
                    'lesson_name': '1. Phương Trình Mặt Phẳng',
                    'formulas': [
                        {
                            'id': 'f_6_1',
                            'name': 'Phương Trình Mặt Phẳng & Khoảng Cách',
                            'latex_code': 'A(x - x_0) + B(y - y_0) + C(z - z_0) = 0; \\qquad d(M, (P)) = \\frac{|A x_M + B y_M + C z_M + D|}{\\sqrt{A^2 + B^2 + C^2}}',
                            'explanation': 'Mặt phẳng $(P)$ đi qua $M_0(x_0; y_0; z_0)$ nhận $\\vec{n}=(A; B; C)$ làm vectơ pháp tuyến.',
                            'common_errors': 'Quên dấu giá trị tuyệt đối trên tử số khi tính khoảng cách từ điểm đến mặt phẳng.',
                            'memory_trick': 'Mặt phẳng cần Điểm và Pháp tuyến; Khoảng cách lấy Thay điểm chia Độ dài pháp tuyến.',
                            'example_basic': {
                                'question': 'Viết phương trình mặt phẳng $(P)$ qua $A(1; -1; 2)$ có VTPT $\\vec{n} = (2; 1; -3)$.',
                                'solution': '$2(x - 1) + 1(y + 1) - 3(z - 2) = 0 \\Leftrightarrow 2x + y - 3z + 5 = 0$.',
                                'final_answer': '$2x + y - 3z + 5 = 0$'
                            },
                            'example_advanced': {
                                'question': 'Tính khoảng cách từ $O(0;0;0)$ đến $(P): 2x - 2y + z - 6 = 0$.',
                                'solution': '$d = \\frac{|2(0) - 2(0) + 0 - 6|}{\\sqrt{2^2 + (-2)^2 + 1^2}} = \\frac{6}{3} = 2$.',
                                'final_answer': '$d = 2$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '2. Phương Trình Đường Thẳng',
                    'formulas': [
                        {
                            'id': 'f_6_2',
                            'name': 'Phương Trình Tham Số & Chính Tắc Của Đường Thẳng',
                            'latex_code': '\\begin{cases} x = x_0 + at \\\\ y = y_0 + bt \\\\ z = z_0 + ct \\end{cases} \\qquad \\text{hoặc} \\qquad \\frac{x - x_0}{a} = \\frac{y - y_0}{b} = \\frac{z - z_0}{c}',
                            'explanation': 'Đường thẳng đi qua điểm $M_0(x_0; y_0; z_0)$ có vectơ chỉ phương $\\vec{u} = (a; b; c)$.',
                            'common_errors': 'Viết dạng chính tắc khi có một thành phần VTCP bằng 0 ($a,b,c=0$ phải viết dạng tham số).',
                            'memory_trick': 'Đường thẳng lấy Điểm làm gốc, Vectơ chỉ phương gắn kèm t.',
                            'example_basic': {
                                'question': 'Viết phương trình tham số của $d$ qua $M(2; 0; -1)$ có VTCP $\\vec{u} = (1; 3; -2)$.',
                                'solution': '$\\begin{cases} x = 2 + t \\\\ y = 3t \\\\ z = -1 - 2t \\end{cases}$.',
                                'final_answer': '$\\begin{cases} x = 2 + t \\\\ y = 3t \\\\ z = -1 - 2t \\end{cases}$'
                            },
                            'example_advanced': {
                                'question': 'Tìm tọa độ giao điểm của $d: \\frac{x-1}{1} = \\frac{y+2}{-1} = \\frac{z}{2}$ với $(P): x + y + z - 3 = 0$.',
                                'solution': 'Tham số hóa $d$: $x = 1+t, y = -2-t, z = 2t$. Thay vào $(P)$: $(1+t) + (-2-t) + 2t - 3 = 0 \\Leftrightarrow 2t - 4 = 0 \\Leftrightarrow t = 2$. Giao điểm $A(3; -4; 4)$.',
                                'final_answer': '$A(3; -4; 4)$'
                            }
                        }
                    ]
                },
                {
                    'lesson_name': '3. Phương Trình Mặt Cầu',
                    'formulas': [
                        {
                            'id': 'f_6_3',
                            'name': 'Phương Trình Mặt Cầu Dạng Chính Chính & Khai Triển',
                            'latex_code': '(x - a)^2 + (y - b)^2 + (z - c)^2 = R^2; \\qquad R = \\sqrt{a^2 + b^2 + c^2 - d}',
                            'explanation': 'Mặt cầu tâm $I(a; b; c)$ bán kính $R$. Dạng khai triển $x^2 + y^2 + z^2 - 2ax - 2by - 2cz + d = 0$.',
                            'common_errors': 'Quên chia hệ số $x, y, z$ cho $-2$ khi tìm tọa độ tâm $I$ từ dạng khai triển.',
                            'memory_trick': 'Tâm chia âm hai hệ số x, y, z; Bán kính bằng Căn tổng bình phương tâm trừ d.',
                            'example_basic': {
                                'question': 'Tìm tâm $I$ và bán kính $R$ của $(S): x^2 + y^2 + z^2 - 2x + 4y - 4 = 0$.',
                                'solution': 'Tâm $I(1; -2; 0)$, $d = -4 \\Rightarrow R = \\sqrt{1^2 + (-2)^2 + 0^2 - (-4)} = 3$.',
                                'final_answer': 'Tâm $I(1; -2; 0)$, $R = 3$'
                            },
                            'example_advanced': {
                                'question': 'Viết phương trình mặt cầu tâm $I(1; 2; -1)$ tiếp xúc $(P): x + 2y - 2z + 1 = 0$.',
                                'solution': 'Bán kính $R = d(I,(P)) = \\frac{|1 + 2(2) - 2(-1) + 1|}{\\sqrt{1^2 + 2^2 + (-2)^2}} = \\frac{8}{3}$. $(S): (x-1)^2 + (y-2)^2 + (z+1)^2 = \\frac{64}{9}$.',
                                'final_answer': '$(x-1)^2 + (y-2)^2 + (z+1)^2 = \\frac{64}{9}$'
                            }
                        }
                    ]
                }
            ]
        }
    }

    segments = algebra_segments if formula_type == 'algebra' else geometry_segments

    return render_template(
        'exam/formula_layout.html', 
        type=formula_type,
        segments=segments
    )
from app.services.hermes_service import HermesService

@exam_bp.route('/api/ai/ask', methods=['POST'])
@login_required
def ask_ai_assistant():
    """API endpoint nhận câu hỏi toán học từ học sinh và gọi AI giải đáp chi tiết"""
    data = request.get_json() or {}
    user_prompt = data.get('prompt', '').strip()
    
    if not user_prompt:
        return jsonify({"status": "error", "message": "Vui lòng nhập nội dung câu hỏi!"}), 400
        
    # Tạo prompt định hướng chuyên gia toán THPT Quốc Gia
    structured_prompt = f"""
    Bạn là một giáo viên chuyên luyện thi Toán THPT Quốc gia tại Việt Nam. 
    Hãy giải quyết yêu cầu/bài toán sau một cách chi tiết, dễ hiểu, trình bày rõ ràng:
    {user_prompt}
    
    Yêu cầu:
    - Giải thích rõ phương pháp tư duy.
    - Trình bày các bước giải chi tiết có công thức Toán học chuẩn.
    - Cảnh báo các lỗi sai hoặc bẫy hay gặp.
    """
    
    ai_reply = HermesService.ask_ai(structured_prompt)
    
    return jsonify({
        "status": "success",
        "reply": ai_reply
    })

@exam_bp.route('/api/ai/advice', methods=['GET'])
@login_required
def get_ai_study_advice():
    """API lấy lời khuyên ôn tập cá nhân hóa dựa trên năng lực IRT (Theta) của học sinh"""
    profile = StudentPerformanceProfile.query.filter_by(student_id=current_user.id).first()
    
    theta = profile.theta_ability if profile else 0.5
    predicted_score = profile.predicted_thpt_score if profile else 5.0
    weak_topics = profile.weak_topics if profile else "Chưa xác định"
    
    advice_prompt = f"""
    Dựa trên dữ liệu năng lực học tập môn Toán của học sinh ôn thi THPT Quốc gia sau đây:
    - Học sinh: {current_user.username if hasattr(current_user, 'username') else 'Học sinh'}
    - Điểm dự đoán hiện tại: {predicted_score}/10
    - Chỉ số năng lực IRT (Theta): {theta}
    - Các phần đang yếu/cần lưu ý: {weak_topics}
    
    Hãy đưa ra một đoạn nhận xét ngắn gọn, khích lệ tinh thần và cho 3 lời khuyên cụ thể để học sinh cải thiện điểm số trong thời gian tới.
    """
    
    advice_reply = HermesService.ask_ai(advice_prompt)
    
    return jsonify({
        "status": "success",
        "predicted_score": predicted_score,
        "advice": advice_reply
    })