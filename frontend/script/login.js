// 替form添加監聽器監聽表單（login-form）的 submit 事件
document.getElementById('login-form').addEventListener('submit', async (e) => {
    
    // 防止表單提交刷新頁面而重整
    e.preventDefault();

    // 從表單中獲取用戶輸入的 account 和 password
    const account = document.getElementById('account').value;
    const password = document.getElementById('password').value;
    
    // 向後端發送資料
    // 使用 fetch 發送 HTTP POST 請求到後端 /login API
    try{
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ account, password }),
        });

        // 處理後端伺服器的回應 : 解析 JSON
        const data = await response.json();
        if (data.status === 'success') {
            // 跳至大廳
            window.location.href = 'lobby.html';
        } else {
            alert(data.message); // 顯示錯誤訊息
        }

    } catch(error){
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    }
})