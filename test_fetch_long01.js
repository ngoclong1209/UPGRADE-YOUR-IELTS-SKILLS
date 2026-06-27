const url = "https://script.google.com/macros/s/AKfycbwZV0v_osCIN3-6lZuXwmxaFlaMdNTFi4t0RYMxXL6Z6eUkPqpe2B4RJKJg2amP9uRJSg/exec";
fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    redirect: 'follow',
    body: JSON.stringify({ 
        action: 'submit', 
        userId: 'long01', 
        deviceId: 'test_device_01',
        lessonId: 'Advanced Listening Lesson #12',
        score: '12/12',
        percent: 100
    })
})
.then(res => res.text())
.then(data => console.log("Result:", data))
.catch(err => console.error("Error:", err));
