import argparse
import os
import time
from datetime import datetime, timedelta
import numpy as np
import soundfile as sf
from tqdm import tqdm
from humanize import naturalsize, naturaldelta

def calculate_audio_duration(audio_data, sample_rate):
    return len(audio_data) / sample_rate

def calculate_required_loops(input_duration, target_duration_minutes):
    target_duration_seconds = target_duration_minutes * 60
    num_repeats = int(np.ceil(target_duration_seconds / input_duration))
    return num_repeats

def generate_audio(input_file, output_file, target_duration_minutes):    
    audio_data, sample_rate = sf.read(input_file)
    input_duration = calculate_audio_duration(audio_data, sample_rate)
    num_repeats = calculate_required_loops(input_duration, target_duration_minutes)
    
    print(f"Length of sample file: {input_duration:.2f} seconds")
    print(f"Number of repeats needed: {num_repeats}")
    
    with sf.SoundFile(output_file, 'w', samplerate=sample_rate, channels=audio_data.shape[1], format='WAV') as f:

        chunk_size = 100
        total_chunks = (num_repeats + chunk_size - 1) // chunk_size
        
        for chunk_idx in tqdm(range(total_chunks), desc="Creating long binaural beat", unit="chunk"):
            start_repeat = chunk_idx * chunk_size
            end_repeat = min(start_repeat + chunk_size, num_repeats)
            repeats_in_chunk = end_repeat - start_repeat
            
            if repeats_in_chunk > 0:
                chunk = np.tile(audio_data, (repeats_in_chunk, 1))
                f.write(chunk)
    
    actual_duration = num_repeats * input_duration
    print(f"Final duration: {actual_duration:.2f} seconds")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a longer version of a binaural beat audio file.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input audio clip to loop.')
    parser.add_argument('-o', '--output', type=str, help='Path to write the output looped audio file.')
    
    duration_group = parser.add_mutually_exclusive_group()
    duration_group.add_argument('-m', '--minutes', type=int, help='Target duration in minutes.')
    duration_group.add_argument('-H', '--hours', type=int, help='Target duration in hours.')
    
    args = parser.parse_args()
    
    if args.hours is not None:
        target_duration_minutes = args.hours * 60
    elif args.minutes is not None:
        target_duration_minutes = args.minutes
    
    start_time = time.time()
    print(f"Started at {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    generate_audio(args.input, args.output, target_duration_minutes)
    end_time = time.time()
    print(f"Completed at {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    duration = timedelta(seconds=end_time - start_time)
    print(f"Time taken: {naturaldelta(duration)}")
    print(f"Final file size: {naturalsize(os.path.getsize(args.output))}")
    print(f"Final file written to: {os.path.abspath(args.output)}")
    print("Done!")