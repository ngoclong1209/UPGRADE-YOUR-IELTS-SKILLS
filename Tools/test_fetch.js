const url = "https://script.google.com/macros/s/AKfycbx7lOgaMcHm0ofxpG3V9bi52rMbL7wBXIzAHovP5xBrp9XbyuZp7QNKbSg2-UTJoauyOg/exec";

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "text/plain;charset=utf-8"
  },
  body: JSON.stringify({
    action: "login",
    student_id: "TEST",
    device_id: "test_device"
  })
})
.then(res => res.text())
.then(data => console.log("RESPONSE:", data))
.catch(err => console.error("ERROR:", err));
