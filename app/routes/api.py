from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Question, StudentPerformanceProfile, Feedback
from app import db
from app.services.hermes_service import HermesService
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats-overview')
@login_required
def stats_overview():
    """API trả về tổng quan năng lực xử lý biểu đồ thích ứng cho học sinh"""
    # Lấy hồ sơ năng lực của học sinh hiện tại
    profile = StudentPerformanceProfile.query.filter_by(student_id=1).first()
    
    if not profile:
        return jsonify({
            "radar_labels": ["Hàm số", "Mũ - Logarit", "Tích phân", "Hình không gian", "Oxyz", "Xác suất"],
            "radar_data": [50, 50, 50, 50, 50, 50],
            "strong_topic": "Chưa xác định",
            "weak_topic": "Chưa xác định"
        })
        
    # Phân tích chuỗi JSON lưu vết chuyên đề để chuẩn bị dữ liệu cho Chart.js
    try:
        mastery_data = json.loads(profile.topic_mastery) if profile.topic_mastery else {}
    except Exception:
        mastery_data = {}
        
    topics_map = {
        "HAM_SO": "Hàm số",
        "MU_LOGARIT": "Mũ - Logarit",
        "TICH_PHAN": "Tích phân",
        "HHKG": "Hình không gian",
        "OXYZ": "Oxyz",
        "XAC_SUAT": "Xác suất"
    }
    
    radar_labels = []
    radar_data = []
    
    for code, name in topics_map.items():
        radar_labels.append(name)
        if code in mastery_data:
            correct, total = mastery_data[code][0], mastery_data[code][1]
            accuracy = round((correct / total) * 100, 1) if total > 0 else 0.0
            radar_data.append(accuracy)
        else:
            radar_data.append(0.0)
            
    # Xác định sơ bộ điểm mạnh/yếu dựa trên profile thích ứng
    weak_list = json.loads(profile.weak_topics) if profile.weak_topics else []
    weak_topic = topics_map.get(weak_list[0], "Không có") if weak_list else "Đang phân tích"
    strong_topic = "Đang đánh giá"

    return jsonify({
        "radar_labels": radar_labels,
        "radar_data": radar_data,
        "strong_topic": strong_topic,
        "weak_topic": weak_topic
    })

@api_bp.route('/send-feedback', methods=['POST'])
def send_feedback():
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'status': 'error', 'message': 'Nội dung phản hồi không được để trống!'}), 400
        
    user_id = current_user.id if current_user.is_authenticated else None
    
    new_feedback = Feedback(user_id=user_id, content=content)
    db.session.add(new_feedback)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Cảm ơn bạn đã gửi phản hồi!'})

@api_bp.route('/ai/ask', methods=['POST'])
@login_required
def ask_ai_assistant():
    """API endpoint nhận câu hỏi (văn bản hoặc hình ảnh) từ khung chat và gọi trợ lý AI xử lý"""
    data = request.get_json() or {}
    user_prompt = data.get('prompt', '').strip()
    image_data = data.get('image', None) # Nhận ảnh dạng base64 nếu học sinh đính kèm
    
    if not user_prompt and not image_data:
        return jsonify({"status": "error", "message": "Vui lòng nhập nội dung câu hỏi hoặc đính kèm ảnh bài toán!"}), 400
        
    # Định hướng ngữ cảnh chuyên gia toán học THPT & chuẩn LaTeX cho AI
    structured_prompt = f"""
    Bạn là một giáo viên chuyên luyện thi Toán THPT Quốc gia tại Việt Nam. 
    Hãy giải quyết câu hỏi/bài toán sau một cách cực kỳ chi tiết, mạch lạc, dễ hiểu. 
    Yêu cầu định dạng:
    - Sử dụng ký hiệu Toán học chuẩn LaTeX đặt trong dấu $ (ví dụ: $x^2$, $\\frac{{a}}{{b}}$).
    - Trình bày rõ ràng từng bước giải.
    
    Nội dung câu hỏi từ học sinh: {user_prompt}
    """
    
    try:
        client = HermesService.get_client()
        
        messages_payload = [
            {"role": "system", "content": "Bạn là một trợ lý AI toán học thông minh cho dự án 12A3math. Luôn trả về công thức toán học chuẩn LaTeX."},
        ]
        
        # Nếu học sinh có đính kèm hình ảnh, cấu trúc payload gửi kèm ảnh cho model đa phương thức
        if image_data:
            messages_payload.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": structured_prompt},
                    {"type": "image_url", "image_url": {"url": image_data}}
                ]
            })
        else:
            messages_payload.append({
                "role": "user",
                "content": structured_prompt
            })

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages_payload,
            max_tokens=1500
        )
        ai_reply = response.choices[0].message.content
        
        return jsonify({
            "status": "success",
            "reply": ai_reply
        })
    except Exception as e:
        print("CHI TIẾT LỖI AI:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500