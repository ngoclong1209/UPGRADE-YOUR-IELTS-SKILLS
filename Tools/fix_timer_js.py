import os
import glob
import re

base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"

def fix_timer_js(html, minutes=60):
    if "function startTimer" not in html:
        timer_js = f"""
        let timeLeft = {minutes} * 60;
        let timerInterval;
        function startTimer() {{
            const display = document.getElementById('timer-display');
            if(!display) return;
            timerInterval = setInterval(() => {{
                timeLeft--;
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                display.innerText = `⏱ ${{m < 10 ? '0' : ''}}${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
                
                if(timeLeft <= 60 && timeLeft > 0) {{
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio && tickAudio.paused) {{
                        tickAudio.play().catch(e=>{{}});
                    }}
                }}
                
                if (timeLeft <= 0) {{
                    clearInterval(timerInterval);
                    const tickAudio = document.getElementById('sfx-tick');
                    if(tickAudio) tickAudio.pause();
                    let btn = document.getElementById('btn-submit');
                    if(btn) btn.click();
                }}
            }}, 1000);
        }}
        """
        # Find the last </script> in the file
        idx = html.rfind("</script>")
        if idx != -1:
            html = html[:idx] + timer_js + html[idx:]
    return html

reading_tpl = os.path.join(base_dir, 'ReadingA1-C2/frontend/template_reading.html')
if os.path.exists(reading_tpl):
    with open(reading_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = fix_timer_js(html, minutes=10)
    with open(reading_tpl, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed Reading Template")

listening_tpl = os.path.join(base_dir, 'pte-listening-audios/template.html')
if os.path.exists(listening_tpl):
    with open(listening_tpl, 'r', encoding='utf-8') as f:
        html = f.read()
    html = fix_timer_js(html, minutes=60)
    with open(listening_tpl, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed Listening Template")

for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/reading/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = fix_timer_js(html, minutes=60)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

for file_path in glob.glob(os.path.join(base_dir, 'data/practicepteonline/listening/**/*.html'), recursive=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = fix_timer_js(html, minutes=60)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Fixed Full Tests")
