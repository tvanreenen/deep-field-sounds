#!/usr/bin/env python3
from ffmpeg import FFmpeg
import argparse
import soundfile as sf
import time
from datetime import datetime

DEFAULT_CONFIG = {
    #'target_duration': 60*5,
    #'audio_clip': 'binaural_beat/binaural_beat_100Hz_L_102.0Hz_R_5.0s.wav',
    #'final_output': 'binaural_beat/binaural_beat_100Hz_L_102.0Hz_R_120s.mp4',
    'resolution': '1920x1080',
    'video_opts': {
        'c:v': 'libx264',    # Video codec: H.264
        'crf': '18',         # Constant Rate Factor: Lower value = higher quality (18-28 is good)
        'preset': 'veryslow', # Encoding preset: Slower = better compression
        'pix_fmt': 'yuv420p' # Pixel format: Widely compatible format
    },
    'audio_opts': {
        'c:a': 'aac',        # Audio codec: Advanced Audio Coding
        'b:a': '192k'        # Audio bitrate: 192 kbps
    }
}

def get_audio_file_duration(audio_file):
    with sf.SoundFile(audio_file) as audio:
        duration = len(audio) / audio.samplerate
        print(f"Detected audio duration: {duration:.2f} seconds")
        return duration
    
def calculate_audio_loop_count(target_duration, audio_duration): 
    audio_loop_count = target_duration // audio_duration - 1
    if audio_loop_count < 0:
        audio_loop_count = 0
    return audio_loop_count

def generate_video_with_audio(config):
    clip_duration = get_audio_file_duration(config['audio_clip'])
    audio_loop_count = calculate_audio_loop_count(config['target_duration'], clip_duration)
    print(f"Generating {config['target_duration']}s video by looping a {clip_duration}s clip {audio_loop_count} times.")
    
    ffmpeg = (
        FFmpeg()
        .input('color=c=black:s={}:d={}'.format(config['resolution'], config['target_duration']), f='lavfi')
        .input(config['audio_clip'], stream_loop=audio_loop_count)
        .output(
            config['final_output'],
            **config['video_opts'],
            **config['audio_opts'],
            shortest=None
        )
        .overwrite_output()
    )
    
    ffmpeg.execute()
    print(f"File saved to: {config['final_output']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a black screen video with looped audio.')
    parser.add_argument('-i', '--input', type=str, help='Path to the audio clip to loop')
    parser.add_argument('-o', '--output', type=str, help='Path to final output video')
    parser.add_argument('-d', '--duration', type=int, help='Target duration of video in seconds')
    args = parser.parse_args()
    config = DEFAULT_CONFIG.copy()
    config.update({
        'target_duration': args.duration,
        'audio_clip': args.input,
        'final_output': args.output
    })

    start_time = time.time()
    print(f"Started generation at {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    generate_video_with_audio(config)
    end_time = time.time()
    print(f"Completed generation at {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")