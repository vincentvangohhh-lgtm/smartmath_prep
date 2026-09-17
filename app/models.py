from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin
import json

class SkillNode(db.Model):
    """Bảng lưu trữ Đồ thị kiến thức (Knowledge Graph Nodes)"""
    __tablename__ = 'skill_nodes'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), default="Toán")
    topic = db.Column(db.String(100), nullable=False)        
    sub_topic = db.Column(db.String(100), nullable=False)    
    concept_code = db.Column(db.String(30), unique=True)     
    prerequisites = db.Column(db.Text)                               

class QuestionTemplate(db.Model):
    """Bảng lưu trữ Mẫu câu hỏi (Templates) để sinh vô hạn câu hỏi biến thể"""
    __tablename__ = 'question_templates'
    id = db.Column(db.Integer, primary_key=True)
    concept_code = db.Column(db.String(30), db.ForeignKey('skill_nodes.concept_code'))
    bloom_level = db.Column(db.String(20)) 
    question_type = db.Column(db.String(20)) 
    template_logic = db.Column(db.Text, nullable=False) 
    solution_template = db.Column(db.Text, nullable=False)

class Question(db.Model):
    """Bảng lưu trữ ngân hàng câu hỏi (Đã nâng cấp hỗ trợ Đề gốc THPTQG & Hình ảnh)"""
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    concept_code = db.Column(db.String(50))
    bloom_level = db.Column(db.String(50))
    question_type = db.Column(db.String(20)) # PART_I, PART_II, PART_III
    content = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text)
    solution_details = db.Column(db.Text)
    semantic_hash = db.Column(db.String(100), unique=True)
    
    # Các tham số IRT (3PL Model)
    difficulty_b = db.Column(db.Float, default=0.0)         # Độ khó câu hỏi
    discrimination_a = db.Column(db.Float, default=1.2)     # Độ phân biệt
    guessing_c = db.Column(db.Float, default=0.25)          # Độ đoán mò
    
    # Mở rộng trường cho Phần I
    option_a = db.Column(db.Text)
    option_b = db.Column(db.Text)
    option_c = db.Column(db.Text)
    option_d = db.Column(db.Text)
    
    # Mở rộng trường cho Phần II
    sub_q_a = db.Column(db.Text)
    sub_q_b = db.Column(db.Text)
    sub_q_c = db.Column(db.Text)
    sub_q_d = db.Column(db.Text) 

    # --- BỔ SUNG NÂNG CẤP ĐỒNG BỘ ĐỀ THI CHÍNH THỨC & HÌNH ẢNH ---
    image_url = db.Column(db.String(255), nullable=True)       # Đường dẫn hình ảnh/đồ thị
    image_type = db.Column(db.String(50), nullable=True)        # 'graph', 'geometry', 'table', ...
    explanation = db.Column(db.Text, nullable=True)           # Lời giải chi tiết
    topic = db.Column(db.String(100), nullable=True)           # Chuyên đề
    year = db.Column(db.Integer, nullable=True)                # Năm thi (2025, 2026, ...)
    code_id = db.Column(db.String(20), nullable=True)          # Mã đề (0101, 0102, ...)
    question_number = db.Column(db.Integer, nullable=True)     # Thứ tự câu trong đề (1-22)

class ExamMatrix(db.Model):
    __tablename__ = 'exam_matrices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    matrix_spec = db.Column(db.Text, nullable=False) 

class StudentPerformanceProfile(db.Model):
    __tablename__ = 'student_profiles'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    theta_ability = db.Column(db.Float, default=0.0)      
    topic_mastery = db.Column(db.Text)                                   
    weak_topics = db.Column(db.Text)                                    
    predicted_thpt_score = db.Column(db.Float, default=5.0) 
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    """Bảng lưu trữ thông tin Người dùng (Học sinh & Giáo viên)"""
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    # Phân quyền hệ thống: 'student' (mặc định) hoặc 'teacher'
    role = db.Column(db.String(20), default='student')

    # Đánh giá trình độ và tham số năng lực IRT
    current_level = db.Column(db.String(20), default="Khá") # Yếu, Khá, Giỏi
    theta_ability = db.Column(db.Float, default=0.0) # Chỉ số IRT Theta (-3.0 đến +3.0)

    # Thông tin bổ sung
    grade = db.Column(db.String(20), default="12")
    school = db.Column(db.String(150), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)  
    cover_image = db.Column(db.String(255), nullable=True)

    # Quan hệ theo dõi lộ trình học tập và kết quả thi
    roadmaps = db.relationship('UserRoadmap', backref='student', lazy=True, cascade="all, delete-orphan")
    exam_results = db.relationship('ExamResult', backref='student', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password_raw):
        self.password = bcrypt.generate_password_hash(password_raw).decode('utf-8')

    def check_password(self, password_raw):
        if not self.password:
            return False
        try:
            return bcrypt.check_password_hash(self.password, password_raw)
        except Exception:
            return False

class UserRoadmap(db.Model):
    """Bảng lưu trữ tiến độ Lộ trình theo ngày của Học sinh"""
    __tablename__ = 'user_roadmaps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day_id = db.Column(db.Integer, nullable=False)           # Ngày 1, Ngày 2, ...
    topic_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='In Progress') # Completed, In Progress
    score = db.Column(db.Float, nullable=True)

class ExamResult(db.Model):
    """Bảng lưu trữ tổng điểm bài kiểm tra"""
    __tablename__ = 'exam_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    total_correct = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, default=5400)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quan hệ liên kết lấy câu trả lời chi tiết
    answers = db.relationship('StudentAnswer', backref='result', lazy=True, cascade="all, delete-orphan")

class StudentAnswer(db.Model):
    """Bảng lưu trữ chi tiết lựa chọn của học sinh cho từng câu hỏi"""
    __tablename__ = 'student_answers'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('exam_results.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option = db.Column(db.Text) # Lưu đáp án học sinh chọn
    is_correct = db.Column(db.Boolean, nullable=False)
    
    # Liên kết trực tiếp sang bảng Question để lấy Lời giải chi tiết
    question = db.relationship('Question', backref='student_answers_rel', lazy=True)
class Feedback(db.Model):
    """Bảng lưu trữ Phản hồi / Báo lỗi từ người dùng"""
    __tablename__ = 'feedbacks'
    __table_args__ = {'extend_existing': True}  # 👈 Thêm dòng này
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quan hệ liên kết lấy thông tin người gửi
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
class UserNotificationRead(db.Model):
    """Bảng lưu vết học sinh nào đã đọc thông báo nào"""
    __tablename__ = 'user_notification_reads'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'notifications'
    # 👇 THÊM DÒNG NÀY ĐỂ TRÁNH LỖI OVERWRITE
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class ForumPost(db.Model):
    """Bảng lưu trữ bài viết thảo luận trên diễn đàn"""
    __tablename__ = 'forum_posts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.String(100), default="VACT KHÓA 3 - TRAO ĐỔI HỌC TẬP")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('forum_posts', lazy=True))
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
class ForumComment(db.Model):
    """Bảng lưu bình luận/giải đáp trong bài viết diễn đàn"""
    __tablename__ = 'forum_comments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    author = db.relationship('User', backref=db.backref('forum_comments', lazy=True))
    post = db.relationship('ForumPost', backref=db.backref('comments', lazy=True, cascade="all, delete-orphan"))
class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 🟢 SỬA 'user.id' THÀNH 'users.id' (Thêm chữ s)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)