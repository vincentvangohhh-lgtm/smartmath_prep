import os
from app import create_app, db
from app.models import StudentPerformanceProfile

# Khởi tạo ứng dụng từ cấu trúc gói app
app = create_app()

def init_server():
    """Khởi tạo cấu trúc cơ sở dữ liệu và dữ liệu mẫu nếu cần thiết"""
    try:
        with app.app_context():
            # Tạo cấu trúc bảng nếu chưa tồn tại trong hệ thống
            db.create_all()
            
            # Kiểm tra và tạo cấu hình năng lực ban đầu cho học sinh demo (nếu chưa có)
            profile_exists = StudentPerformanceProfile.query.filter_by(student_id=1).first()
            if not profile_exists:
                profile = StudentPerformanceProfile(
                    student_id=1, 
                    theta_ability=0.5, 
                    predicted_thpt_score=7.5
                )
                db.session.add(profile)
                db.session.commit()
                print("[Hệ thống] Đã thiết lập cấu hình môi trường ban đầu thành công!")
            else:
                print("[Hệ thống] Cơ sở dữ liệu đã sẵn sàng hoạt động.")
    except Exception as e:
        print(f"[Cảnh báo] Chưa thể kết nối hoặc khởi tạo DB ngay lúc này: {str(e)}")

# Tự động chạy khởi tạo database ngay khi Gunicorn import app trên Render
init_server()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)