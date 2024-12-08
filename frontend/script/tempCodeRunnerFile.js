document.getElementById('create-meeting-button').addEventListener('click', async () => {
    const meetingData = {
        content: document.getElementById('meeting-type').value,
        languages: document.getElementById('languages').value.split(','), // 多語言以逗號分隔
        city: document.getElementById('city').value,
        place: document.getElementById('place').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start-time').value,
        end_time: document.getElementById('end-time').value,
        max_participants: document.getElementById('max-participants').value,
        holder_id: localStorage.getItem('user_id') // 假設用戶 ID 保存在 localStorage
    };

    try {
        const response = await fetch('/create-meeting', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(meetingData)
        });

        const result = await response.json();
        if (result.status === 'success') {
            alert(result.message);
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    }
});
