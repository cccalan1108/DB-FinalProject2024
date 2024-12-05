document.querySelector('.submit-button').addEventListener('click', function(event) {
    // 取得所有必填欄位
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        // 如果欄位為空，設置邊框為紅色
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = 'red'; // 提示未填欄位
        } else {
            field.style.borderColor = ''; // 恢復正常顏色
            sessionStorage.setItem(field.id, field.value);
        }
    });

    if (!isValid) {
        event.preventDefault(); // 阻止跳轉
        alert('Please fill in all required fields before registering.');
        window.location.href = 'login.html';
    } else {
        // 跳轉到目標頁面
        window.location.href = 'lobby.html';
    }
});

// 還原用戶輸入
document.addEventListener('DOMContentLoaded', function () {
    const fields = document.querySelectorAll('input, select');
    fields.forEach(field => {
        const savedValue = sessionStorage.getItem(field.id);
        if (savedValue) {
            field.value = savedValue; // 恢復用戶輸入的值
        }
    });
});