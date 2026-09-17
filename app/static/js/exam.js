let secondsElapsed = 0;
const timerDisplay = document.getElementById('timer-display');
const durationInput = document.getElementById('duration_seconds');

// Đếm ngược / Đếm lên thời gian làm bài
const timerInterval = setInterval(() => {
    secondsElapsed++;
    let mins = Math.floor(secondsElapsed / 60);
    let secs = secondsElapsed % 60;
    timerDisplay.innerText = 
        (mins < 10 ? '0' + mins : mins) + ':' + (secs < 10 ? '0' + secs : secs);
    if(durationInput) {
        durationInput.value = secondsElapsed;
    }
}, 1000);

// Cuộn mượt tới câu hỏi tương ứng khi nhấn từ Panel phải
function scrollToQuestion(order) {
    const el = document.getElementById(`q-card-${order}`);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Bắt sự kiện chọn đáp án để đổi màu button điều hướng ở Panel bên phải
document.querySelectorAll('.exam-radio-input').forEach(input => {
    input.addEventListener('change', (e) => {
        const order = e.target.getAttribute('data-qorder');
        const navBtn = document.getElementById(`nav-btn-${order}`);
        if(navBtn) {
            navBtn.classList.remove('btn-outline-secondary');
            navBtn.classList.add('btn-success', 'text-white');
        }
    });
});

function submitExamForm() {
    if(confirm("Bạn có chắc chắn muốn nộp bài thi này không?")) {
        clearInterval(timerInterval);
        document.getElementById('exam-form').submit();
    }
}