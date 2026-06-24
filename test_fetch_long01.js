const url = "https://script.google.com/macros/s/AKfycbw8ggCZFiONZQ6eSuMczrjEyIKcsGk1ZNeK8CUjdsiiAgDon_bz7m5WmA61_ESoiuJb/exec";
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
