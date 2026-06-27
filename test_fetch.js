const url = "https://script.google.com/macros/s/AKfycbwZV0v_osCIN3-6lZuXwmxaFlaMdNTFi4t0RYMxXL6Z6eUkPqpe2B4RJKJg2amP9uRJSg/exec";
fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify({ action: 'login', student_id: 'LONG123', device_id: 'test' })
})
.then(res => res.text())
.then(data => console.log("Result:", data))
.catch(err => console.error("Error:", err));
