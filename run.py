import os
import traceback
from app import create_app, db
from app.models import StudentPerformanceProfile

app = None
try:
    app = create_app()
    with app.app_context():
        db.create_all()
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
    print(f"[LỖI KHỞI ĐỘNG NGHIÊM TRỌNG]: {str(e)}")
    traceback.print_exc()

if __name__ == '__main__':
    if app:
        app.run(host='127.0.0.1', port=8080, debug=True)