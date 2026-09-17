import math
import json
from app.models import Question, StudentPerformanceProfile

class AdaptiveTestEngine:
    """
    Engine điều phối bài thi thích ứng (Adaptive Testing) dựa trên Lý thuyết Ứng đáp Câu hỏi (IRT).
    Quản lý cấu trúc đề thi tốt nghiệp THPT mới: 12 trắc nghiệm đơn, 2 câu Đúng/Sai, 4 trả lời ngắn.
    """

    # Ánh xạ mức độ Bloom sang giá trị tham số độ khó (Difficulty parameter - b) trong mô hình IRT
    DIFFICULTY_MAP = {
        "Nhận biết": -1.5,
        "Thông hiểu": -0.2,
        "Vận dụng": 1.0,
        "Vận dụng cao": 2.2
    }

    @classmethod
    def select_next_question_spec(cls, student_theta, current_question_index):
        """
        Bước 1: Xác định cấu trúc phần thi và mức độ khó mục tiêu cho câu hỏi tiếp theo.
        - current_question_index: Chạy từ 1 đến 18 (Tổng 18 câu chuẩn cấu trúc mới).
        """
        # Xác định phần thi (PART) bám sát ma trận cấu trúc của Bộ GD&ĐT
        if current_question_index <= 12:
            question_type = "PART_I"      # 12 câu trắc nghiệm khách quan (4 lựa chọn)
        elif current_question_index <= 14:
            question_type = "PART_II"     # 2 câu hỏi Đúng/Sai (Mỗi câu gồm 4 ý nhỏ)
        else:
            question_type = "PART_III"    # 4 câu hỏi trắc nghiệm trả lời ngắn (Điền số)

        # Ánh xạ điểm năng lực Theta hiện tại (-3.0 đến 3.0) sang mức độ Bloom mục tiêu
        if student_theta < -0.6:
            target_level = "Nhận biết"
        elif student_theta < 0.6:
            target_level = "Thông hiểu"
        elif student_theta < 1.6:
            target_level = "Vận dụng"
        else:
            target_level = "Vận dụng cao"

        return {
            "question_type": question_type,
            "target_level": target_level
        }

    @classmethod
    def evaluate_answer(cls, question, student_answer):
        """
        Bước 2: Hệ thống chấm điểm thời gian thực dựa trên từng loại hình câu hỏi của cấu trúc mới.
        - PART_I / PART_III: So khớp chuỗi trơn.
        - PART_II: Học sinh gửi lên mảng JSON/List dạng [True, False, True, True] đại diện 4 ý a,b,c,d.
        """
        if not student_answer:
            return 0, 0.0

        if question.question_type in ["PART_I", "PART_III"]:
            is_correct = 1 if str(student_answer).strip().lower() == str(question.correct_answer).strip().lower() else 0
            # Tính điểm thô (Raw score): PART_I là 0.25đ/câu; PART_III là 1.0đ/câu
            score_earned = 0.25 if question.question_type == "PART_I" else 1.0
            return is_correct, (score_earned if is_correct else 0.0)

        elif question.question_type == "PART_II":
            try:
                # Chuyển đổi đáp án chuẩn từ JSON string sang List nếu cần
                actual_answers = json.loads(question.correct_answer) if isinstance(question.correct_answer, str) else question.correct_answer
                student_answers = json.loads(student_answer) if isinstance(student_answer, str) else student_answer
                
                # Tính số ý nhỏ (a, b, c, d) học sinh trả lời đúng
                correct_sub_int = sum(1 for act, stud in zip(actual_answers, student_answers) if bool(act) == bool(stud))
                
                # Cập nhật trạng thái Đúng/Sai cho thuật toán IRT: Đúng >= 3 ý được tính là hành vi tích cực
                is_correct = 1 if correct_sub_int >= 3 else 0
                
                # Quy đổi điểm chuẩn Bộ GD&ĐT cho câu Đúng/Sai: Đúng 1 ý=0.1đ; 2 ý=0.25đ; 3 ý=0.5đ; 4 ý=1.0đ
                score_map = {0: 0.0, 1: 0.1, 2: 0.25, 3: 0.5, 4: 1.0}
                return is_correct, score_map.get(correct_sub_int, 0.0)
            except Exception:
                return 0, 0.0

        return 0, 0.0

    @classmethod
    def update_student_theta(cls, current_theta, question_level, is_correct):
        """
        Bước 3: Thuật toán Bayesian cập nhật Theta dựa trên mô hình phản hồi câu hỏi (IRT Rasch).
        Tự động tăng/giảm độ khó động sau từng câu làm bài.
        """
        # Lấy tham số độ khó câu hỏi (b)
        q_difficulty = cls.DIFFICULTY_MAP.get(question_level, 0.0)
        
        # Hàm Logistic tính xác suất lý thuyết học sinh làm đúng câu hỏi dựa trên năng lực hiện tại
        p_success = 1.0 / (1.0 + math.exp(-(current_theta - q_difficulty)))
        
        # Hệ số điều chỉnh độ nhạy thông tin học tập (Learning Rate)
        k_factor = 0.4
        
        # Cập nhật vị trí Theta mới
        new_theta = current_theta + k_factor * (is_correct - p_success)
        
        # Giới hạn Theta trong phân mảnh chuẩn hóa quốc tế [-3.0, 3.0]
        return max(-3.0, min(3.0, new_theta))

    @staticmethod
    def predict_thpt_score(theta):
        """
        Bước 4: Ánh xạ điểm định vị năng lực liên tục Theta sang thang điểm 10 thi tốt nghiệp THPT.
        """
        # Hàm chuyển đổi phân bố chuẩn tuyến tính sang thang điểm 10 bài thi quốc gia
        raw_score = 5.0 + (theta * 1.65)
        return round(max(0.0, min(10.0, raw_score)), 2)

    @classmethod
    def generate_learning_analytics(cls, theta, concept_logs):
        """
        Bước 5: AI sinh Báo cáo phân tích thế mạnh, điểm yếu và tự động lên lộ trình cá nhân hóa.
        - concept_logs: Dictionary lưu kết quả làm theo dạng chuyên đề: {"Chủ đề": [Đúng, Tổng]}
        """
        weak_topics = []
        strong_topics = []
        
        for concept, log in concept_logs.items():
            correct, total = log[0], log[1]
            accuracy = (correct / total) * 100 if total > 0 else 0
            if accuracy < 60:
                weak_topics.append(concept)
            else:
                strong_topics.append(concept)
                
        # Tự động lập kế hoạch ôn tập thông minh (Personalized Learning Path)
        personalized_schedule = []
        if weak_topics:
            for idx, topic in enumerate(weak_topics[:3]):
                personalized_schedule.append({
                    "day": idx + 1,
                    "focus": f"Trọng tâm ôn tập: {topic}",
                    "tasks": [
                        f"Quét lại 15 câu mức độ Nhận biết/Thông hiểu để củng cố nền tảng.",
                        f"Xem lời giải chi tiết và các sai lầm thường gặp của chuyên đề này."
                    ]
                })
        else:
            # Nếu học sinh giỏi toàn diện, AI sinh lộ trình nâng cao Vận dụng cao
            personalized_schedule.append({
                "day": 1,
                "focus": "Thử thách Vận dụng cao (Cực trị Hàm số & Hệ tọa độ Oxyz nâng cao)",
                "tasks": ["Giải quyết 20 câu tích hợp mức độ phân hóa để giành điểm 9, 10."]
            })

        return {
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "personalized_schedule": personalized_schedule
        }