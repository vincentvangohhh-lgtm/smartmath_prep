from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user  
from app.models import Question, StudentPerformanceProfile, User, ExamResult, StudentAnswer
from app import db
from app.services.grader import Grader  
import json
import random

# IMPORT CÁC HÀM SINH ĐỀ TỪ GENERATOR
from app.question_generator import generate_parametric_questions, generate_roadmap_questions

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exam/dashboard')
@login_required  
def dashboard():
    """Bảng điều khiển học sinh: Hiển thị đầy đủ lịch sử làm bài thực tế của từng cá nhân"""
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
@login_required  
def take_exam(exam_id):
    # 1. XỬ LÝ POST KHI HỌC SINH NHẤN NỘP BÀI THI
    if request.method == 'POST':
        user_answers = request.form.to_dict()
        
        class MockExamObj:
            id = exam_id
            is_survey = True
        exam_obj = MockExamObj()
        
        try:
            duration_seconds = int(request.form.get('spent_time', 5400))
        except ValueError:
            duration_seconds = 5400
            
        result = Grader.grade_exam(current_user, exam_obj, user_answers, duration_seconds)
        result.duration_seconds = duration_seconds
        
        if result.score >= 8.0:
            current_user.current_level = "Giỏi"
        elif result.score >= 5.0:
            current_user.current_level = "Khá"
        else:
            current_user.current_level = "Yếu"
            
        db.session.add(result)
        db.session.add(current_user)
        db.session.commit()
        
        flash("Nộp bài thi thành công! Hệ thống AI đã chấm điểm và cập nhật lại hồ sơ năng lực.", "success")
        return redirect(url_for('exam.exam_result', result_id=result.id))
        
    # 2. XỬ LÝ GET: LẤY ĐỀ THI HIỆN TẠI TỪ DATABASE RA GIAO DIỆN
    part_1 = Question.query.filter_by(question_type="PART_I").all()
    part_2 = Question.query.filter_by(question_type="PART_II").all()
    part_3 = Question.query.filter_by(question_type="PART_III").all()
    questions_list = part_1 + part_2 + part_3
    
    # Định dạng tiêu đề động dựa vào số lượng câu hỏi để hiển thị giao diện chính xác
    total_q = len(questions_list)
    title = f"Đề Luyện Tập Theo Lộ Trình AI - Mã số #{exam_id}" if total_q == 15 else f"Đề khảo sát năng lực đầu vào THPT Quốc Gia - Mã số #{exam_id}"
    
    mock_exam = {
        "id": exam_id,
        "title": title,
        "duration": 90 if total_q != 15 else 30, # Đề 15 câu cho làm nhanh trong 30 phút
        "is_survey": True
    }
    
    return render_template('exam/take.html', exam_id=exam_id, exam=mock_exam, questions=questions_list)

@exam_bp.route('/exam/generate', methods=['POST'])
@login_required
def generate():
    """Route xử lý khi bấm nút 'Sinh đề mới': Làm mới hoàn toàn Database câu hỏi"""
    db.session.query(Question).delete()
    dynamic_questions = generate_parametric_questions()
    
    for q in dynamic_questions:
        db.session.add(q)
    db.session.commit()
    
    random_exam_id = random.randint(100, 999)
    flash("Hệ thống AI đã khởi tạo cấu trúc đề thi khảo sát thích ứng mới thành công!", "primary")
    return redirect(url_for('exam.take_exam', exam_id=random_exam_id))

@exam_bp.route('/roadmap/practice/<int:day_id>')
@login_required
def roadmap_practice(day_id):
    """Route xử lý sinh đề 15 câu hỏi riêng biệt live-data phục vụ ôn tập theo ngày"""
    if day_id not in [1, 2, 3]:
        flash("Ngày ôn tập trong lộ trình năng lực không hợp lệ!", "danger")
        return redirect(url_for('exam.dashboard'))
    
    try:
        # Bước quan trọng: Xóa sạch câu hỏi cũ trong DB để nạp live-data 15 câu mới vào
        db.session.query(Question).delete()
        
        # Gọi bộ sinh đề từ app/question_generator.py sinh chuẩn 15 câu theo chủ đề của ngày
        roadmap_questions = generate_roadmap_questions(day_id)
        
        for q in roadmap_questions:
            db.session.add(q)
            
        db.session.commit()
        
        random_exam_id = random.randint(1000, 9999)
        flash(f"Khởi tạo thành công bộ 15 câu ôn tập chuyên sâu cho Ngày {day_id}!", "success")
        return redirect(url_for('exam.take_exam', exam_id=random_exam_id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Có lỗi khi khởi tạo đề luyện tập: {str(e)}", "danger")
        return redirect(url_for('exam.dashboard'))

@exam_bp.route('/exam/result/<int:result_id>')
@login_required
def exam_result(result_id):
    """Trang hiển thị điểm số, chi tiết toàn bộ câu hỏi kèm đáp án học sinh đã chọn"""
    result = ExamResult.query.filter_by(id=result_id, user_id=current_user.id).first_or_404()
    profile = StudentPerformanceProfile.query.filter_by(student_id=current_user.id).first()
    
    part_1 = Question.query.filter_by(question_type="PART_I").all()
    part_2 = Question.query.filter_by(question_type="PART_II").all()
    part_3 = Question.query.filter_by(question_type="PART_III").all()
    all_questions = part_1 + part_2 + part_3
    
    student_answers = StudentAnswer.query.filter_by(result_id=result.id).all()
    answers_map = {sa.question_id: sa for sa in student_answers}
    
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
        
    return render_template(
        'exam/result.html', 
        profile=profile, 
        result=result, 
        questions=questions_data
    )