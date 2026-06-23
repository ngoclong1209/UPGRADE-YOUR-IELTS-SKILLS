import re

with open('/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/pte-listening-audios/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change Title
html = html.replace('IELTS Listening Practice', 'IELTS Reading Practice')

# Remove Audio Player CSS
html = re.sub(r'\.audio-fixed-bottom\s*\{[^}]*\}', '', html)
html = re.sub(r'\.audio-fixed-bottom\s*audio\s*\{[^}]*\}', '', html)

# Remove Audio HTML
html = re.sub(r'<div class="audio-fixed-bottom" id="audio-player-container".*?</div>', '', html, flags=re.DOTALL)

# Adjust padding-bottom of panes since no audio player
html = html.replace('padding-bottom: 110px;', 'padding-bottom: 40px;')
html = html.replace('padding-bottom: 100px;', 'padding-bottom: 40px;')

# Change HUD header
html = html.replace('🌸 AUDIO TRANSCRIPT', '📖 READING PASSAGE')
html = html.replace('✨ HAPPY LEARNING! ✨', '<span id="timer-display" style="font-size: 1.1rem;">⏱ 20:00</span>')

# Remove transcript lock HTML
lock_html_pattern = r'<div id="transcript-lock">.*?</div>'
html = re.sub(lock_html_pattern, '', html, flags=re.DOTALL)

# Change transcript content id to passage content and remove display: none
html = html.replace('id="transcript-content" style="display: none;"', 'id="passage-content"')
html = html.replace('{{TRANSCRIPT_HTML}}', '{{PASSAGE_HTML}}')

# Swap the panes (answer-pane and passage-pane)
# Currently: 
# <div class="answer-pane fairytale-panel"> ... </div>
# <div class="passage-pane fairytale-panel"> ... </div>
main_layout_match = re.search(r'(<div class="main-layout" id="main-layout".*?>)(.*?)(</div>\s*<!-- Hidden audio elements)', html, re.DOTALL)

if main_layout_match:
    prefix = main_layout_match.group(1)
    content = main_layout_match.group(2)
    suffix = main_layout_match.group(3)
    
    # find passage pane and answer pane
    answer_match = re.search(r'<div class="answer-pane fairytale-panel">.*?(?=<div class="passage-pane fairytale-panel">)', content, re.DOTALL)
    passage_match = re.search(r'<div class="passage-pane fairytale-panel">.*', content, re.DOTALL)
    
    if answer_match and passage_match:
        answer_html = answer_match.group(0)
        passage_html = passage_match.group(0)
        # Swap
        new_content = passage_html + "\n" + answer_html
        html = html.replace(content, new_content)

# Add Timer JS
timer_js = """
        // Timer Logic
        let timeLeft = 20 * 60; // 20 minutes
        const timerDisplay = document.getElementById('timer-display');
        let timerInterval;

        function startTimer() {
            timerInterval = setInterval(() => {
                timeLeft--;
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                if(timerDisplay) {
                    timerDisplay.innerText = `⏱ ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
                }
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('btn-submit').click();
                }
            }, 1000);
        }
"""
html = html.replace('const correctAnswers = {{CORRECT_ANSWERS_JSON}};', timer_js + '\n        const correctAnswers = {{CORRECT_ANSWERS_JSON}};')

# Start timer when login succeeds
html = html.replace("document.getElementById('main-layout').style.display = 'flex';", "document.getElementById('main-layout').style.display = 'flex'; startTimer();")

# Remove unlockTranscript logic
html = re.sub(r'function unlockTranscript\(\) \{.*?\}', '', html, flags=re.DOTALL)
html = html.replace('unlockTranscript();', '')

with open('/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS LISTENING/ReadingA1-C2/frontend/template_reading.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Successfully generated template_reading.html")
