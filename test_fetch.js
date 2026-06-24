const url = "https://script.google.com/macros/s/AKfycbw8ggCZFiONZQ6eSuMczrjEyIKcsGk1ZNeK8CUjdsiiAgDon_bz7m5WmA61_ESoiuJb/exec";
fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify({ action: 'login', student_id: 'LONG123', device_id: 'test' })
})
.then(res => res.text())
.then(data => console.log("Result:", data))
.catch(err => console.error("Error:", err));
