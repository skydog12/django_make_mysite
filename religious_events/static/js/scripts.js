document.addEventListener('DOMContentLoaded', function() {
    // 메시지 자동 숨김
    var messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(function() {
            messages.style.display = 'none';
        }, 5000);
    }

    // 예약 버튼 클릭 이벤트
    var reserveButtons = document.querySelectorAll('.btn-reserve');
    reserveButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('이 행사를 예약하시겠습니까?')) {
                e.preventDefault();
            }
        });
    });

    // 예약 취소 버튼 클릭 이벤트
    var cancelButtons = document.querySelectorAll('.btn-cancel');
    cancelButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('이 예약을 취소하시겠습니까?')) {
                e.preventDefault();
            }
        });
    });
});