import os
import subprocess

LEVELS = ['Basic', 'Intermediate', 'Advanced']
OUTPUT_DIR = '.'

count = 0
for level in LEVELS:
    level_dir = os.path.join(OUTPUT_DIR, level)
    if not os.path.exists(level_dir):
        continue
        
    for lesson_folder in os.listdir(level_dir):
        if lesson_folder.startswith('Lesson_'):
            audio_path = os.path.join(level_dir, lesson_folder, 'audio.mp3')
            temp_audio = os.path.join(level_dir, lesson_folder, 'audio_temp.mp3')
            
            if os.path.exists(audio_path):
                # Apply 1.3x volume (30% increase)
                print(f"Amplifying {audio_path}...")
                cmd = ['ffmpeg', '-y', '-i', audio_path, '-filter:a', 'volume=1.3', temp_audio]
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if result.returncode == 0:
                    os.replace(temp_audio, audio_path)
                    count += 1
                else:
                    print(f"Failed to amplify {audio_path}")
                    if os.path.exists(temp_audio):
                        os.remove(temp_audio)

print(f"Successfully amplified {count} audio files!")
