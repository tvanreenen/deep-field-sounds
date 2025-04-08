import numpy as np
import soundfile as sf
import os
from tqdm import tqdm

def create_long_binaural_beat(input_file, output_file, target_duration_minutes=60.0):
    """
    Create a longer version of a binaural beat targeting a specific duration.
    Uses a memory-efficient approach by writing chunks to disk.
    
    Parameters:
    - input_file: Path to the input binaural beat file
    - output_file: Path to save the longer binaural beat. 
                   If None, defaults to 'long_<input_filename>' 
                   in the same directory as the input file.
    - target_duration_minutes: Target duration in minutes (default: 60.0)
    """
    print(f"Creating a {target_duration_minutes} minute version based on {input_file}...")
    print(f"Output will be saved to: {output_file}")
    
    # Load the input audio file
    audio_data, sample_rate = sf.read(input_file)
    
    # Calculate the number of repeats needed to reach the target duration
    input_duration = len(audio_data) / sample_rate
    target_duration_seconds = target_duration_minutes * 60
    num_repeats = int(np.ceil(target_duration_seconds / input_duration))
    
    print(f"Input duration: {input_duration:.2f} seconds")
    print(f"Target duration: {target_duration_seconds:.2f} seconds")
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
    print(f"Actual duration: {actual_duration:.2f} seconds")
    print("Done!")

# Example usage
if __name__ == '__main__':
    script_directory = os.path.dirname(os.path.abspath(__file__))

    input_filepath = os.path.join(script_directory, "binaural_beat_100Hz_L_102.0Hz_R_5.0s.wav")
    target_duration_minutes = 30
    output_filepath = os.path.join(script_directory, f"binaural_beat_100Hz_L_102.0Hz_R_{target_duration_minutes:.1f}m.wav")
    create_long_binaural_beat(input_filepath, output_filepath, target_duration_minutes)