from flask import session
from app import db
from app.models import Question, User, ExamResult, StudentAnswer
try:
    from app.services.adaptive_engine import AdaptiveEngine
except ImportError:
    AdaptiveEngine = None

class Grader:
    @staticmethod
    def grade_exam(user, exam, user_answers, duration_seconds):
        submitted_qids = set()
        for key in user_answers.keys():
            if 'question_' in key:
                clean_key = key.replace('question_', '')
                if '_' in clean_key:
                    submitted_qids.add(clean_key.split('_')[0])
                else:
                    submitted_qids.add(clean_key)
        
        all_questions = Question.query.filter(
            Question.id.in_([int(uid) for uid in submitted_qids if uid.isdigit()])
        ).order_by(
            db.case(
                (Question.question_type == 'PART_I', 1),
                (Question.question_type == 'PART_II', 2),
                (Question.question_type == 'PART_III', 3),
                else_=4
            ),
            Question.id.asc()
        ).all()
        
        if not all_questions:
            part_1 = Question.query.filter_by(question_type="PART_I").limit(12).all()
            part_2 = Question.query.filter_by(question_type="PART_II").limit(4).all()
            part_3 = Question.query.filter_by(question_type="PART_III").limit(6).all()
            all_questions = part_1 + part_2 + part_3

        exam_title = ""
        if isinstance(exam, dict):
            exam_title = str(exam.get('title', '')).upper()
        else:
            exam_title = str(getattr(exam, 'title', '')).upper()

        current_type = session.get('current_exam_type', '')

        is_millionaire = ('TRIỆU PHÚ' in exam_title or 'TRIEU PHU' in exam_title or current_type == 'millionaire')
        is_roadmap = ('LỘ TRÌNH' in exam_title or 'LO TRINH' in exam_title or current_type == 'roadmap')
        is_standard_22 = ('22 CÂU' in exam_title or 'CHUẨN THPT' in exam_title or current_type == 'standard_22' or current_type == 'official')

        part_2_count = sum(1 for q in all_questions if getattr(q, 'question_type', 'PART_I') == 'PART_II')
        part_3_count = sum(1 for q in all_questions if getattr(q, 'question_type', 'PART_I') == 'PART_III')

        # Phân định đúng 3 mốc số lượng
        is_15_q_mode = is_millionaire or is_roadmap or (part_2_count == 0 and part_3_count == 0 and len(all_questions) == 15)

        if is_15_q_mode:
            total_questions = 15
        elif is_standard_22 or len(all_questions) == 22:
            total_questions = 22
        else: # 18 câu
            total_questions = 18
        
        final_calculated_score = 0.0
        total_fully_correct_questions = 0

        exam_id_val = exam.get('id', 100) if isinstance(exam, dict) else getattr(exam, 'id', 100)

        result_obj = ExamResult(
            user_id=user.id,
            exam_id=exam_id_val,
            score=0.0,
            total_correct=0,
            total_questions=total_questions,
            duration_seconds=duration_seconds
        )
        db.session.add(result_obj)
        db.session.flush()

        for q in all_questions:
            q_type = getattr(q, 'question_type', 'PART_I')
            is_correct = False
            selected_str = ""
            current_q_score = 0.0

            # --- PHẦN I ---
            if q_type == 'PART_I':
                selected = user_answers.get(f"question_{q.id}")
                selected_str = str(selected).strip().upper() if selected else ""
                
                db_correct_raw = str(getattr(q, 'correct_option', None) or getattr(q, 'correct_answer', None) or getattr(q, 'answer', '') or "").strip().upper()
                db_correct = db_correct_raw[0] if db_correct_raw else ""
                
                is_correct = (selected_str == db_correct) and selected_str != ""
                if is_correct:
                    if total_questions == 15:
                        current_q_score = 10.0 / 15.0  # 15 câu: ~0.67đ (Tổng 10đ)
                    elif total_questions == 22:
                        current_q_score = 0.25         # 22 câu THPT: 0.25đ (12 câu = 3.0đ)
                    else:
                        current_q_score = 1.0 / 3.0    # 18 câu thích ứng: 1/3đ (12 câu = 4.0đ)
                    
                    total_fully_correct_questions += 1

            # --- PHẦN II ---
            elif q_type == 'PART_II':
                db_correct_str = str(getattr(q, 'correct_option', None) or getattr(q, 'correct_answer', None) or getattr(q, 'answer', '') or "")
                
                # Tách linh hoạt theo dấu phẩy ',' hoặc dấu gạch đứng '|'
                if ',' in db_correct_str:
                    db_answers = db_correct_str.split(',')
                else:
                    db_answers = db_correct_str.split('|')

                sub_results = []
                correct_sub_count = 0
                
                for idx, sub in enumerate(['a', 'b', 'c', 'd']):
                    key = f"question_{q.id}_{sub}"
                    user_ans_sub = str(user_answers.get(key) or "").strip()
                    sub_results.append(user_ans_sub if user_ans_sub else "Bỏ trống")
                    
                    if idx < len(db_answers):
                        db_ans = db_answers[idx].strip()
                        def normalize_tf(val):
                            val_upper = val.upper()
                            if 'ĐÚNG' in val_upper or 'Đ' in val_upper or 'T' in val_upper or 'TRUE' in val_upper:
                                return 'ĐÚNG'
                            if 'SAI' in val_upper or 'S' in val_upper or 'F' in val_upper or 'FALSE' in val_upper:
                                return 'SAI'
                            return val
                        
                        if normalize_tf(user_ans_sub) == normalize_tf(db_ans) and user_ans_sub != "":
                            correct_sub_count += 1
                
                # Thang lũy tiến chuẩn Bộ GD&ĐT 2025: 0.1 | 0.25 | 0.5 | 1.0 (4 câu = Tối đa 4.0đ)
                if correct_sub_count == 1:
                    current_q_score = 0.1
                elif correct_sub_count == 2:
                    current_q_score = 0.25
                elif correct_sub_count == 3:
                    current_q_score = 0.5
                elif correct_sub_count == 4:
                    current_q_score = 1.0
                    total_fully_correct_questions += 1
                
                selected_str = "|".join(sub_results)
                is_correct = (correct_sub_count == 4)

            # --- PHẦN III ---
            elif q_type == 'PART_III':
                selected = user_answers.get(f"question_{q.id}")
                selected_str = str(selected).strip() if selected else ""
                db_correct = str(getattr(q, 'correct_option', None) or getattr(q, 'correct_answer', None) or getattr(q, 'answer', '') or "").strip()
                
                # Chuẩn hóa dấu phẩy ',' thành dấu chấm '.' để so sánh số thập phân
                user_ans_clean = selected_str.replace(',', '.').strip()
                db_ans_clean = db_correct.replace(',', '.').strip()
                
                # So sánh độ chính xác dạng số thập phân hoặc chuỗi văn bản
                try:
                    is_correct = (abs(float(user_ans_clean) - float(db_ans_clean)) < 1e-4) and selected_str != ""
                except ValueError:
                    is_correct = (user_ans_clean == db_ans_clean) and selected_str != ""

                if is_correct:
                    if total_questions == 22:
                        current_q_score = 0.5   # 22 câu THPT: 0.5đ (6 câu = 3.0đ)
                    else:
                        current_q_score = 1.0   # 18 câu thích ứng: 1.0đ (2 câu = 2.0đ)
                    
                    total_fully_correct_questions += 1

            final_calculated_score += current_q_score

            sa = StudentAnswer(
                result_id=result_obj.id,
                user_id=user.id,
                question_id=q.id,
                selected_option=selected_str,
                is_correct=is_correct
            )
            db.session.add(sa)

        result_obj.score = round(min(max(final_calculated_score, 0.0), 10.0), 2)
        result_obj.total_correct = total_fully_correct_questions
        correct_rate = result_obj.score / 10.0

        if user:
            if AdaptiveEngine:
                try:
                    is_survey_flag = getattr(exam, 'is_survey', False) or (isinstance(exam, dict) and exam.get('is_survey'))
                    if is_survey_flag:
                        new_level = AdaptiveEngine.determine_level_by_rate(correct_rate)
                    else:
                        new_level = AdaptiveEngine.adjust_difficulty_level(getattr(user, 'current_level', 'Trung bình'), correct_rate)
                    user.current_level = new_level if new_level else "Trung bình"
                except Exception:
                    if result_obj.score >= 8.0:
                        user.current_level = "Giỏi"
                    elif result_obj.score >= 6.5:
                        user.current_level = "Khá"
                    elif result_obj.score >= 5.0:
                        user.current_level = "Trung bình"
                    else:
                        user.current_level = "Yếu"
            else:
                if result_obj.score >= 8.0:
                    user.current_level = "Giỏi"
                elif result_obj.score >= 6.5:
                    user.current_level = "Khá"
                elif result_obj.score >= 5.0:
                    user.current_level = "Trung bình"
                else:
                    user.current_level = "Yếu"

            from app.models import StudentPerformanceProfile
            profile = StudentPerformanceProfile.query.filter_by(student_id=user.id).first()
            if not profile:
                profile = StudentPerformanceProfile(student_id=user.id, predicted_thpt_score=7.50)
                db.session.add(profile)
                db.session.flush()

            past_results = ExamResult.query.filter_by(user_id=user.id).all()
            if past_results:
                avg_score = sum([r.score for r in past_results]) / len(past_results)
                predicted = round(min(max(avg_score + 1.2, 1.0), 10.0), 2)
                profile.predicted_thpt_score = predicted
            else:
                profile.predicted_thpt_score = round(result_obj.score, 2)
        
        db.session.commit()
        return result_obj