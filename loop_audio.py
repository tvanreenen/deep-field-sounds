import numpy as np
import soundfile as sf
from tqdm import tqdm
import argparse
import os
from humanize import naturalsize

def get_audio_duration(audio_data, sample_rate):
    """
    Calculate the duration of an audio file in seconds.
    
    Parameters:
    - audio_data: The audio data array
    - sample_rate: The sample rate of the audio
    
    Returns:
    - float: Duration in seconds
    """
    return len(audio_data) / sample_rate

def calculate_required_repeats(input_duration, target_duration_minutes):
    """
    Calculate the number of repeats needed to reach the target duration.
    
    Parameters:
    - input_duration: Duration of the input audio in seconds
    - target_duration_minutes: Target duration in minutes
    
    Returns:
    - int: Number of repeats needed
    - float: Target duration in seconds
    """
    target_duration_seconds = target_duration_minutes * 60
    num_repeats = int(np.ceil(target_duration_seconds / input_duration))
    return num_repeats, target_duration_seconds

def create_long_binaural_beat(input_file, output_file, target_duration_minutes=60.0, duration_unit='minutes'):
    """
    Create a longer version of a binaural beat targeting a specific duration.
    Uses a memory-efficient approach by writing chunks to disk.
    
    Parameters:
    - input_file: Path to the input binaural beat file
    - output_file: Path to save the longer binaural beat. 
                   If None, defaults to 'long_<input_filename>' 
                   in the same directory as the input file.
    - target_duration_minutes: Target duration in minutes (default: 60.0)
    - duration_unit: Unit of the target duration ('minutes' or 'hours')
    """
    if duration_unit == 'hours':
        duration_str = f"{target_duration_minutes/60:.1f} hours"
    else:
        duration_str = f"{target_duration_minutes:.1f} minutes"
    
    print(f"Creating a {duration_str} version based on {input_file}...")
    print(f"Output will be saved to: {output_file}")
    
    audio_data, sample_rate = sf.read(input_file)
    input_duration = get_audio_duration(audio_data, sample_rate)
    num_repeats, target_duration_seconds = calculate_required_repeats(input_duration, target_duration_minutes)
    
    print(f"Length of sample file: {input_duration:.2f} seconds")
    print(f"Target duration: {duration_str}")
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
    print(f"Final file size: {naturalsize(os.path.getsize(output_file))}")
    print("Done!")

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
        duration_unit = 'hours'
    elif args.minutes is not None:
        target_duration_minutes = args.minutes
        duration_unit = 'minutes'
    
    create_long_binaural_beat(args.input, args.output, target_duration_minutes, duration_unit)