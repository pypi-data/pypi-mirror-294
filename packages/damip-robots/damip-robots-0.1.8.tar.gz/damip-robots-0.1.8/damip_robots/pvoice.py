
import subprocess

def play(file_path):
    try:
        # 使用aplay命令在后台播放音频文件
        subprocess.Popen(['aplay', file_path])
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 使用函数
# wav_file = '/usr/local/voice/mixkit-small-electric-glitch-2595.wav'
# play(wav_file)





