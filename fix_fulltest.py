import os
import re

base_dirs = [
    '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Reading_315_FullTest',
    '/Users/vungoclong/Desktop/Antigravity/UPGRADE YOUR ILETS SKILLS/Listening_204_FullTest'
]

count = 0
for base_dir in base_dirs:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find the submit_full_test fetch block
                # We can just look for: action: 'submit_full_test'
                if "action: 'submit_full_test'" in content and "action: 'submit'" not in content:
                    # Let's insert a second fetch
                    
                    # The payload for submit:
                    # payload_submit = {
                    #     action: 'submit',
                    #     userId: localStorage.getItem('youpass_student_id') || 'UNKNOWN',
                    #     deviceId: getDeviceId(),
                    #     lessonId: 'Full Test ' + (isReading ? 'Reading' : 'Listening') + ' - ' + test_name,
                    #     score: totalScore + '/40',
                    #     percent: Math.round((totalScore/40)*100)
                    # };
                    
                    pass # Wait, doing this via regex might be tricky if the variable names are different.
