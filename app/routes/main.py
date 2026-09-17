import os
import json
import time
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, UserRoadmap, Feedback, Notification, UserNotificationRead, ForumPost, ForumComment, Document
from app.routes.auth import teacher_required

# Khai báo duy nhất MỘT đối tượng Blueprint
main_bp = Blueprint('main', __name__)

# ==============================================================================
# CONTEXT PROCESSOR (TỰ ĐỘNG TRUYỀN THÔNG BÁO RA TOÀN BỘ BASE.HTML)
# ==============================================================================

@main_bp.app_context_processor
def inject_global_data():
    try:
        latest_notifs = Notification.query.order_by(Notification.created_at.desc()).limit(10).all()
        
        if current_user.is_authenticated:
            read_notif_ids = db.session.query(UserNotificationRead.notification_id)\
                .filter_by(user_id=current_user.id).subquery()
            
            unread_count = Notification.query.filter(Notification.id.not_in(read_notif_ids)).count()
        else:
            unread_count = 0
    except Exception as e:
        latest_notifs = []
        unread_count = 0
        
    return dict(latest_notifications=latest_notifs, unread_count=unread_count)


@main_bp.route('/api/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    if not current_user.is_authenticated:
        return jsonify({'status': 'error', 'message': 'Chưa đăng nhập!'}), 401
        
    try:
        all_notifs = Notification.query.all()
        existing_reads = {r.notification_id for r in UserNotificationRead.query.filter_by(user_id=current_user.id).all()}
        
        for notif in all_notifs:
            if notif.id not in existing_reads:
                read_record = UserNotificationRead(user_id=current_user.id, notification_id=notif.id)
                db.session.add(read_record)
                
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Đã đánh dấu tất cả thông báo là đã đọc!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==============================================================================
# KHU VỰC ROUTE HỆ THỐNG CHÍNH
# ==============================================================================

# Route cho Landing Page (hiện đầu tiên khi chưa đăng nhập)
@main_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('landing.html')

# Route trang chủ sau khi đăng nhập (giữ nguyên tên 'index' để không lỗi base.html)
@main_bp.route('/dashboard')
@login_required
def index():
    return render_template('main/index.html')

@main_bp.route('/profile')
@login_required
def profile_page():
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/survey')
@login_required
def survey():
    if current_user.current_level != 'Chưa khảo sát':
        return redirect(url_for('exam.dashboard'))
    return render_template('main/survey.html')

@main_bp.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('Không tìm thấy file tải lên!', 'danger')
        return redirect(url_for('main.profile_page'))

    file = request.files['avatar']
    if file.filename == '':
        flash('Chưa chọn hình ảnh nào!', 'warning')
        return redirect(url_for('main.profile_page'))

    if file:
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            flash('Chỉ chấp nhận các file ảnh có định dạng JPG, PNG, GIF, WEBP!', 'danger')
            return redirect(url_for('main.profile_page'))

        filename = f"avatar_user_{current_user.id}_{int(time.time())}.{ext}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        current_user.avatar = filename
        db.session.commit()
        
        flash('Đã cập nhật ảnh đại diện thành công!', 'success')

    return redirect(url_for('main.profile_page'))


# ==============================================================================
# API TIẾP NHẬN FEEDBACK TỪ HỌC SINH
# ==============================================================================

@main_bp.route('/api/send-feedback', methods=['POST'])
def send_feedback():
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'status': 'error', 'message': 'Nội dung phản hồi không được để trống!'}), 400
        
    user_id = current_user.id if current_user.is_authenticated else None
    
    try:
        new_fb = Feedback(user_id=user_id, content=content)
        db.session.add(new_fb)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Cảm ơn bạn đã gửi phản hồi! Admin sẽ xem xét sớm nhất.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Có lỗi xảy ra khi gửi: {str(e)}'}), 500


# ==============================================================================
# KHU VỰC QUẢN LÝ DÀNH CHO GIÁO VIÊN & ADMIN
# ==============================================================================

@main_bp.route('/teacher/dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    students = User.query.filter_by(role='student').all()
    
    total_students = len(students)
    excellent_count = sum(1 for s in students if s.current_level in ['Giỏi', 'Xuất sắc'])
    average_count = sum(1 for s in students if s.current_level in ['Khá', 'Trung bình'])
    weak_count = sum(1 for s in students if s.current_level in ['Yếu'])

    return render_template(
        'teacher_dashboard.html', 
        students=students,
        total_students=total_students,
        excellent_count=excellent_count,
        average_count=average_count,
        weak_count=weak_count
    )

@main_bp.route('/teacher/student/<int:student_id>/roadmap')
@login_required
@teacher_required
def view_student_roadmap(student_id):
    student = User.query.get_or_404(student_id)
    roadmaps = UserRoadmap.query.filter_by(user_id=student.id).order_by(UserRoadmap.day_id).all()
    
    return render_template('student_roadmap_detail.html', student=student, roadmaps=roadmaps)


@main_bp.route('/admin/feedbacks')
@login_required
@teacher_required
def admin_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    
    return render_template(
        'admin/feedbacks.html',
        feedbacks=feedbacks,
        notifications=notifications
    )


@main_bp.route('/admin/feedback/delete/<int:feedback_id>', methods=['POST'])
@login_required
@teacher_required
def delete_feedback(feedback_id):
    fb = Feedback.query.get_or_404(feedback_id)
    db.session.delete(fb)
    db.session.commit()
    flash('Đã xóa phản hồi thành công!', 'success')
    return redirect(url_for('main.admin_feedbacks'))


@main_bp.route('/admin/notification/create', methods=['POST'])
@login_required
@teacher_required
def create_notification():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('Vui lòng nhập đầy đủ tiêu đề và nội dung thông báo!', 'danger')
    else:
        notif = Notification(title=title, content=content)
        db.session.add(notif)
        db.session.commit()
        flash('Đã phát thông báo mới thành công!', 'success')
        
    return redirect(url_for('main.admin_feedbacks'))


@main_bp.route('/admin/notification/delete/<int:notif_id>', methods=['POST'])
@login_required
@teacher_required
def delete_notification(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    db.session.delete(notif)
    db.session.commit()
    flash('Đã xóa thông báo!', 'info')
    return redirect(url_for('main.admin_feedbacks'))


# ==============================================================================
# KHU VỰC CHỨC NĂNG TRA CỨU CÔNG THỨC TOÁN 12
# ==============================================================================

def load_formulas_data():
    json_path = os.path.join(current_app.root_path, 'static', 'data', 'formulas.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"algebra": {}, "geometry": {}}

@main_bp.route('/formulas/algebra')
def algebra_hub():
    data = load_formulas_data().get('algebra', {})
    search_query = request.args.get('q', '').strip().lower()
    
    filtered_data = {}
    if search_query:
        for cd_id, cd_info in data.items():
            matched_lessons = []
            for lesson in cd_info['lessons']:
                matched_formulas = [
                    f for f in lesson['formulas'] 
                    if search_query in f['name'].lower() or search_query in lesson['lesson_name'].lower()
                ]
                if matched_formulas:
                    matched_lessons.append({
                        "lesson_name": lesson["lesson_name"],
                        "formulas": matched_formulas
                    })
            if matched_lessons:
                filtered_data[cd_id] = {"title": cd_info["title"], "lessons": matched_lessons}
    else:
        filtered_data = data

    return render_template('exam/formula_layout.html', segments=filtered_data, type="algebra", title="Thư viện Đại Số 12")

@main_bp.route('/formulas/geometry')
def geometry_hub():
    data = load_formulas_data().get('geometry', {})
    search_query = request.args.get('q', '').strip().lower()
    
    filtered_data = {}
    if search_query:
        for cd_id, cd_info in data.items():
            matched_lessons = []
            for lesson in cd_info['lessons']:
                matched_formulas = [
                    f for f in lesson['formulas'] 
                    if search_query in f['name'].lower() or search_query in lesson['lesson_name'].lower()
                ]
                if matched_formulas:
                    matched_lessons.append({
                        "lesson_name": lesson["lesson_name"],
                        "formulas": matched_formulas
                    })
            if matched_lessons:
                filtered_data[cd_id] = {"title": cd_info["title"], "lessons": matched_lessons}
    else:
        filtered_data = data

    return render_template('exam/formula_layout.html', segments=filtered_data, type="geometry", title="Thư viện Hình Học 12")

@main_bp.route('/notifications')
def notifications_page():
    all_notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    return render_template('main/notifications.html', notifications=all_notifications)

@main_bp.route('/upload-cover', methods=['POST'])
@login_required
def upload_cover():
    if 'cover' not in request.files:
        flash('Không tìm thấy file tải lên!', 'danger')
        return redirect(url_for('main.profile_page'))

    file = request.files['cover']
    if file.filename == '':
        flash('Chưa chọn hình ảnh nào!', 'warning')
        return redirect(url_for('main.profile_page'))

    if file:
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            flash('Chỉ chấp nhận các định dạng JPG, PNG, GIF, WEBP!', 'danger')
            return redirect(url_for('main.profile_page'))

        filename = f"cover_user_{current_user.id}_{int(time.time())}.{ext}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'covers')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        current_user.cover_image = filename
        db.session.commit()
        
        flash('Đã cập nhật ảnh bìa thành công!', 'success')

    return redirect(url_for('main.profile_page'))

# ==============================================================================
# DIỄN ĐÀN HỎI ĐÁP (FORUM)
# ==============================================================================
@main_bp.route('/forum/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_forum_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if current_user.role not in ['admin', 'teacher'] and post.user_id != current_user.id:
        flash('Bạn không có quyền xóa bài viết này!', 'danger')
        return redirect(url_for('main.forum_page'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Đã xóa bài viết thành công!', 'success')
    return redirect(url_for('main.forum_page'))

@main_bp.route('/forum/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_forum_comment(comment_id):
    comment = ForumComment.query.get_or_404(comment_id)
    post = ForumPost.query.get(comment.post_id)
    
    # Kiểm tra quyền
    if current_user.role not in ['admin', 'teacher'] and comment.user_id != current_user.id:
        flash('Bạn không có quyền xóa bình luận này!', 'danger')
        return redirect(url_for('main.forum_page'))
        
    try:
        if post and post.comments_count > 0:
            post.comments_count -= 1
        db.session.delete(comment)
        db.session.commit()
        flash('Đã xóa bình luận thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi xóa.', 'danger')
        
    return redirect(url_for('main.forum_page'))

@main_bp.route('/forum')
@login_required
def forum_page():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('main/forum.html', posts=posts)

@main_bp.route('/forum/create-post', methods=['POST'])
@login_required
def create_forum_post():
    content = request.form.get('content', '').strip()
    file = request.files.get('image')

    if not content and (not file or file.filename == ''):
        flash('Vui lòng nhập nội dung hoặc đính kèm ảnh câu hỏi!', 'warning')
        return redirect(url_for('main.forum_page'))

    image_filename = None
    if file and file.filename != '':
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            image_filename = f"post_{current_user.id}_{int(time.time())}.{ext}"
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'forum')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, image_filename))

    user_grade = str(current_user.grade or '12').strip()
    if '12' in user_grade:
        tag_display = "LỚP 12 (ÔN THI THPT) - TRAO ĐỔI HỌC TẬP"
    elif '11' in user_grade:
        tag_display = "LỚP 11 - TRAO ĐỔI HỌC TẬP"
    elif '10' in user_grade:
        tag_display = "LỚP 10 - TRAO ĐỔI HỌC TẬP"
    else:
        tag_display = f"LỚP {user_grade} - TRAO ĐỔI HỌC TẬP"

    new_post = ForumPost(
        content=content,
        image_url=image_filename,
        tag=tag_display,
        user_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()
    
    flash('Đã đăng câu hỏi/chia sẻ thành công!', 'success')
    return redirect(url_for('main.forum_page'))

@main_bp.route('/forum/like/<int:post_id>', methods=['POST'])
@login_required
def like_forum_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    post.likes_count = (post.likes_count or 0) + 1
    db.session.commit()
    return jsonify({'status': 'success', 'likes_count': post.likes_count})

@main_bp.route('/forum/comment/<int:post_id>', methods=['POST'])
@login_required
def add_forum_comment(post_id):
    post = ForumPost.query.get_or_404(post_id)
    content = request.form.get('content', '').strip()
    
    if content:
        comment = ForumComment(
            content=content,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        post.comments_count = (post.comments_count or 0) + 1
        db.session.commit()
        flash('Đã đăng câu trả lời/bình luận!', 'success')
    else:
        flash('Vui lòng nhập nội dung bình luận!', 'warning')
        
    return redirect(url_for('main.forum_page'))

# ==============================================================================
# TÀI LIỆU HỌC TẬP & DOWNLOAD
# ==============================================================================

@main_bp.route('/documents')
@login_required  # Thêm dòng này để bắt buộc đăng nhập
def documents_page():
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('documents.html', documents=documents)

@main_bp.route('/documents/upload', methods=['POST'])
@login_required
def upload_document():
    if current_user.role not in ['admin', 'teacher']:
        flash('Bạn không có quyền đăng tải tài liệu!', 'danger')
        return redirect(url_for('main.documents_page'))

    title = request.form.get('title')
    pdf_file = request.files.get('pdf_file')
    cover_file = request.files.get('cover_file')

    if not pdf_file or not pdf_file.filename.lower().endswith('.pdf'):
        flash('Vui lòng chọn file đúng định dạng PDF!', 'warning')
        return redirect(url_for('main.documents_page'))

    base_upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')

    pdf_filename = secure_filename(f"{int(time.time())}_{pdf_file.filename}")
    pdf_dir = os.path.join(base_upload_dir, 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_file.save(os.path.join(pdf_dir, pdf_filename))

    cover_filename = None
    if cover_file and cover_file.filename != '':
        cover_filename = secure_filename(f"cover_{int(time.time())}_{cover_file.filename}")
        cover_dir = os.path.join(base_upload_dir, 'covers')
        os.makedirs(cover_dir, exist_ok=True)
        cover_file.save(os.path.join(cover_dir, cover_filename))

    new_doc = Document(
        title=title,
        filename=pdf_filename,
        cover_image=cover_filename,
        uploaded_by=current_user.id
    )
    db.session.add(new_doc)
    db.session.commit()

    flash('Đăng tải tài liệu thành công!', 'success')
    return redirect(url_for('main.documents_page'))