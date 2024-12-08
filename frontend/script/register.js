// 替form添加監聽器聽submit
document.getElementById('register-form').addEventListener('submit', async (e) => {
    // 防止表單提交刷新頁面而重整
    e.preventDefault();

    const account = document.getElementById('account').value;
    const password = document.getElementById('password').value;
    const name = document.getElementById('name').value;
    const nickname = document.getElementById('nickname').value;
    const birthday = document.getElementById('birthday').value;
    const nationality = document.getElementById('nationality').value;
    const city = document.getElementById('city').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const admin_code = document.getElementById('admin_code').value;
    const sex = document.getElementById('gender').value;

    try{
        const response = await fetch('/submit-register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ account, password, name, nickname,
                birthday, nationality, city, phone, email, admin_code, sex
             }),
        });
        
        // 解析 JSON
        const data = await response.json();
        if (data.status === 'success') {
            // 跳至大廳
            alert(data.message);
            window.location.href = 'login.html';
            
        } else {
            console.error('Error:', data.message);
            alert(data.message); // 顯示錯誤訊息
        }

    } catch(error){
        console.error('Error:', data.message);
        alert('An unexpected error occurred.');
    }
})