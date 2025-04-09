import argparse
import os
import time
import sys
from datetime import datetime, timedelta
import ffmpeg
import soundfile as sf
from humanize import naturalsize, precisedelta
from progress_tracker import show_progress

def get_audio_file_duration(audio_file):
    with sf.SoundFile(audio_file) as audio:
        duration = len(audio) / audio.samplerate
        print(f"Detected audio duration: {duration:.2f} seconds")
        return duration
    
def calculate_required_loops(target_duration, audio_duration): 
    audio_loop_count = target_duration // audio_duration - 1
    if audio_loop_count < 0:
        audio_loop_count = 0
    return audio_loop_count

def generate_video(input, output, target_duration_seconds, resolution='1920x1080'):
    clip_duration = get_audio_file_duration(input)
    audio_loop_count = calculate_required_loops(target_duration_seconds, clip_duration)
    print(f"Generating {target_duration_seconds}s video by looping a {clip_duration}s clip {audio_loop_count} times.")
    
    # Create a black video stream
    video_stream = ffmpeg.input(
        'color=c=black:s={}:d={}'.format(resolution, target_duration_seconds),
        f='lavfi'
    )
    
    # Create the audio stream with looping
    audio_stream = ffmpeg.input(input, stream_loop=audio_loop_count)
    
    # Combine and output
    stream = ffmpeg.output(
        video_stream,
        audio_stream,
        output,
        vcodec='libx264',
        crf='18',
        preset='veryslow',
        pix_fmt='yuv420p',
        acodec='aac',
        audio_bitrate='192k'
    )
    
    try:
        with show_progress(target_duration_seconds) as socket_filename:
            stream.global_args('-progress', 'unix://{}'.format(socket_filename)).run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a black screen video with looped audio.')
    parser.add_argument('-i', '--input', type=str, help='Path to the audio clip to loop')
    parser.add_argument('-o', '--output', type=str, help='Path to final output video')
    
    duration_group = parser.add_mutually_exclusive_group()
    duration_group.add_argument('-m', '--minutes', type=int, help='Target duration in minutes')
    duration_group.add_argument('-H', '--hours', type=int, help='Target duration in hours')
    
    args = parser.parse_args()
    
    if args.hours is not None:
        target_duration_seconds = args.hours * 3600
    elif args.minutes is not None:
        target_duration_seconds = args.minutes * 60
    
    start_time = time.time()
    print(f"Started at {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    generate_video(input=args.input, output=args.output, target_duration_seconds=target_duration_seconds)
    end_time = time.time()
    print(f"Completed at {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    duration = timedelta(seconds=end_time - start_time)
    print(f"Time taken: {precisedelta(duration, minimum_unit="seconds")}")
    print(f"Final file size: {naturalsize(os.path.getsize(args.output))}")
    print(f"Final file written to: {os.path.abspath(args.output)}")
    print('Done!')