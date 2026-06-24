import os

def apply_sfx():
    base_dir = "/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS"
    files = [
        "Listening_102_Basic/template.html",
        "Listening_102_Basic/index.html",
        "Reading_1232_Basic/frontend/template_reading.html",
        "Reading_1232_Basic/frontend/index.html"
    ]

    for rel in files:
        path = os.path.join(base_dir, rel)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add or replace audio tags
        audio_tags = """
    <audio id="sfx-start" preload="auto" src="../assets/sfx/freesound_community-medieval-fanfare-6826.mp3"></audio>
    <audio id="sfx-click" preload="auto" src="../assets/sfx/collectcoins.mp3"></audio>
    <audio id="sfx-win" preload="auto" src="../assets/sfx/winningholliwood.mp3"></audio>
    <audio id="sfx-win2" preload="auto" src="../assets/sfx/gamewinner.mp3"></audio>
    <audio id="sfx-tick" loop preload="auto" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3"></audio>
"""
        
        # Remove old audio tags if any
        import re
        content = re.sub(r'<audio[^>]*></audio>', '', content)
        
        # Inject new audio tags before <script>
        if "<script>" in content:
            content = content.replace("<script>", audio_tags + "\n<script>", 1)
        
        # Handle click event listener on inputs
        click_listener = """
        document.addEventListener('click', function(e) {
            if (e.target.tagName === 'INPUT' && (e.target.type === 'radio' || e.target.type === 'text')) {
                const sfx = document.getElementById('sfx-click');
                if (sfx) { sfx.currentTime = 0; sfx.play().catch(e=>{}); }
            }
        });
        """
        
        if click_listener not in content:
            if "window.addEventListener('DOMContentLoaded'" in content:
                content = content.replace("window.addEventListener('DOMContentLoaded', () => {", click_listener + "\n        window.addEventListener('DOMContentLoaded', () => {")

        # Update sfx-success to sfx-start in login flow
        content = content.replace("playSfx('sfx-success');", "playSfx('sfx-start');")
        content = content.replace("document.getElementById('sfx-win').play()", "document.getElementById(Math.random() > 0.5 ? 'sfx-win' : 'sfx-win2').play()")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("SFX logic applied to 102 and 1232.")

if __name__ == "__main__":
    apply_sfx()
