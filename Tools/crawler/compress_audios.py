import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor

LISTENING_DIR = "/Users/vungoclong/Desktop/Antigravity/Youpass.vn/data/practicepteonline/listening"

def compress_audio(audio_path, codec="mp3", bitrate="32k"):
    """
    Compresses an audio file in-place using ffmpeg.
    - codec: "mp3" or "opus"
    - bitrate: "32k" or "16k" or "24k"
    """
    if not os.path.exists(audio_path):
        return False
        
    dir_name = os.path.dirname(audio_path)
    base_name = os.path.basename(audio_path)
    
    # Target file settings
    if codec == "opus":
        ext = ".opus"
        ffmpeg_args = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ac", "1", "-ar", "24000",
            "-c:a", "libopus", "-ab", bitrate,
        ]
    else:
        ext = ".mp3"
        ffmpeg_args = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ac", "1", "-ar", "24000",
            "-ab", bitrate,
        ]
        
    temp_output = os.path.join(dir_name, f"temp_compressed{ext}")
    ffmpeg_args.append(temp_output)
    
    try:
        # Run ffmpeg in quiet mode to keep logs clean
        res = subprocess.run(ffmpeg_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and os.path.exists(temp_output) and os.path.getsize(temp_output) > 0:
            orig_size = os.path.getsize(audio_path)
            new_size = os.path.getsize(temp_output)
            reduction = (orig_size - new_size) / orig_size * 100
            print(f"Success [{base_name}]: {orig_size / (1024*1024):.2f} MB -> {new_size / (1024*1024):.2f} MB ({reduction:.1f}% reduction)")
            
            # Replace original
            os.remove(audio_path)
            final_output = os.path.join(dir_name, base_name.replace(".mp3", ext))
            shutil.move(temp_output, final_output)
            return True
        else:
            print(f"Failed to compress {audio_path}. FFmpeg error:\n{res.stderr}")
            if os.path.exists(temp_output):
                os.remove(temp_output)
            return False
    except Exception as e:
        print(f"Exception during compression of {base_name}: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return False

def main():
    print("Starting parallel batch audio compression...")
    # List all Test_* directories
    folders = [f for f in os.listdir(LISTENING_DIR) if f.startswith("Test_") and os.path.isdir(os.path.join(LISTENING_DIR, f))]
    
    # Sort folders numerically
    folders.sort(key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 9999)
    
    tasks = []
    target_codec = "mp3" 
    target_bitrate = "32k"
    
    for folder in folders:
        folder_path = os.path.join(LISTENING_DIR, folder)
        for file in os.listdir(folder_path):
            if file.startswith("audio_") and file.endswith(".mp3"):
                audio_path = os.path.join(folder_path, file)
                tasks.append(audio_path)
                
    total_count = len(tasks)
    print(f"Found {total_count} audio files to compress.")
    
    # Use max_workers matching CPU count to maximize speed
    cpu_count = os.cpu_count() or 4
    print(f"Compiling with {cpu_count} parallel threads...")
    
    success_count = 0
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        results = executor.map(lambda path: compress_audio(path, target_codec, target_bitrate), tasks)
        for r in results:
            if r:
                success_count += 1
                
    print(f"\nCompression finished! Successfully compressed {success_count}/{total_count} files.")

if __name__ == "__main__":
    main()
