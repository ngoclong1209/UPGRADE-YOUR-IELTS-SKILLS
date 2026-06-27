const WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwZV0v_osCIN3-6lZuXwmxaFlaMdNTFi4t0RYMxXL6Z6eUkPqpe2B4RJKJg2amP9uRJSg/exec";

const payload = {
    action: 'submit',
    userId: "LONG01",
    deviceId: "test_device_01",
    lessonId: "Reading A1-A2 - lesson_001",
    score: "4/5",
    percent: 80
};

fetch(WEB_APP_URL, {
    redirect: "follow",
    method: "POST",
    headers: {
        "Content-Type": "text/plain;charset=utf-8",
    },
    body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => console.log("Response:", data))
.catch(e => console.error("Error:", e));
