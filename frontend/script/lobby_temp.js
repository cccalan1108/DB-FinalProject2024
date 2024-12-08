// document.getElementById('create-meeting-button').addEventListener('click', async () => {
//     const meetingData = {
//         content: document.getElementById('meeting-type').value,
//         languages: document.getElementById('languages').value.split(','), // 多語言以逗號分隔
//         city: document.getElementById('city').value,
//         place: document.getElementById('place').value,
//         date: document.getElementById('date').value,
//         start_time: document.getElementById('start-time').value,
//         end_time: document.getElementById('end-time').value,
//         max_participants: document.getElementById('max-participants').value,
//         holder_id: localStorage.getItem('user_id') // 假設用戶 ID 保存在 localStorage
//     };

//     try {
//         const response = await fetch('/create-meeting', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(meetingData)
//         });

//         const result = await response.json();
//         if (result.status === 'success') {
//             alert(result.message);
//         } else {
//             alert(`Error: ${result.message}`);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An unexpected error occurred.');
//     }
// });



// 綁定按鈕事件
document.getElementById('exit-button').addEventListener('click', () => {
    alert("Goodbye!");
    window.location.href = '/logout';
});



// 綁定事件
document.getElementById('submit-meeting-button').addEventListener('click', async () => {
    const meetingData = {
        content: document.getElementById('meeting-type').value.trim(),
        languages: document.getElementById('languages').value
            .split(',')
            .map(lang => lang.trim())
            .filter(lang => lang !== ''),
        city: document.getElementById('city').value.trim(),
        place: document.getElementById('place').value.trim(),
        date: document.getElementById('date').value,
        start_time: document.getElementById('start-time').value,
        end_time: document.getElementById('end-time').value,
        max_participants: document.getElementById('max-participants').value.trim(),
        holder_id: localStorage.getItem('holder_id')
    };

    if (
        !meetingData.content ||
        !meetingData.city ||
        !meetingData.place ||
        !meetingData.date ||
        !meetingData.start_time ||
        !meetingData.end_time ||
        !meetingData.max_participants ||
        !meetingData.holder_id
    ) {
        alert('Please fill in all required fields!');
        return;
    }

    try {
        console.log("Submitting meeting data:", meetingData); // 調試用
        const response = await fetch('/create-meeting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(meetingData)
        });
        console.log("Response received:", response); // 查看是否有回應


        const result = await response.json();
        console.log("Parsed response:", result); // 確認返回的結果

        if (result.status === 'success') {
            alert(result.message);
            clearForm();
            document.getElementById('create-meeting-form').style.display = 'none';
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    }
});

// 清空表單函式
function clearForm() {
    document.getElementById('meeting-type').value = '';
    document.getElementById('languages').value = '';
    document.getElementById('city').value = '';
    document.getElementById('place').value = '';
    document.getElementById('date').value = '';
    document.getElementById('start-time').value = '';
    document.getElementById('end-time').value = '';
    document.getElementById('max-participants').value = '';
    document.getElementById('holder-id').value = '';
}



// 取得並顯示會議列表
async function fetchMeetings() {
    try {
        const response = await fetch('/list-meeting', {
            method: 'GET',
        });
        const result = await response.json();

        if (result.status === 'success') {
            const meetings = result.meetings;

            // 清空現有列表
            const meetingList = document.getElementById('meeting-list');
            meetingList.innerHTML = '';

            // 動態生成會議項目
            meetings.forEach(meeting => {
                const meetingItem = document.createElement('li');
                meetingItem.innerHTML = `
                    <strong>${meeting.content}</strong><br>
                    Date: ${meeting.event_date}, Time: ${meeting.start_time} - ${meeting.end_time}<br>
                    City: ${meeting.event_city}, Place: ${meeting.event_place}<br>
                    Participants: ${meeting.current_participants}/${meeting.max_participants}<br>
                    Languages: ${meeting.languages.join(', ')}
                `;
                meetingList.appendChild(meetingItem);
            });
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    }
}
