// 替form添加監聽器聽submit
document.getElementById('login-form').addEventListener('submit', async (e) => {
    // 防止表單提交刷新頁面而重整
    console.log("DEBUG: Event listener triggered");
    e.preventDefault();

    const account = document.getElementById('account').value;
    const password = document.getElementById('password').value;
    console.log(account)
    console.log(password)
    try{
        const response = await fetch('/submit-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ account, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.log("noook")
            throw new Error(errorData.message || 'Unexpected error occurred');
        }
        console.log("ok")
        // 解析 JSON
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