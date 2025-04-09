#!/bin/bash
# This script generates a full-duration black screen video
# and combines it with a looping short audio file.
#
# Requirements:
# - A short audio WAV file specified in AUDIO_FILE.
# - ffmpeg installed on your system

# --- Configuration ---
TOTAL_DURATION=1200          # Total duration in seconds (20 minutes)
AUDIO_FILE="binaural_beat/binaural_beat_100Hz_L_102.0Hz_R_5.0s.wav" # Input audio file
AUDIO_DURATION=5             # Duration of the audio file in seconds (must match the actual audio)
RESOLUTION="1920x1080"        # Video resolution
FINAL_OUTPUT="binaural_beat_100Hz_L_102.0Hz_R_1200s.mp4" # Final output filename
TEMP_VIDEO_FILE="black_video_temp.mp4" # Temporary video file

# Video encoding options (adjust preset for speed vs quality if needed)
VIDEO_OPTS="-c:v libx264 -crf 18 -preset veryslow -pix_fmt yuv420p"
# Audio encoding options
AUDIO_OPTS="-c:a aac -b:a 192k"
# --- End Configuration ---

# Basic validation
if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file not found: $AUDIO_FILE"
    exit 1
fi
if [ "$AUDIO_DURATION" -le 0 ]; then
    echo "Error: AUDIO_DURATION must be greater than 0."
    exit 1
fi
if [ "$TOTAL_DURATION" -le 0 ]; then
    echo "Error: TOTAL_DURATION must be greater than 0."
    exit 1
fi
# Check if total duration is a multiple of audio duration for clean looping
REMAINDER=$(( TOTAL_DURATION % AUDIO_DURATION ))
if [ $REMAINDER -ne 0 ]; then
    echo "Warning: TOTAL_DURATION ($TOTAL_DURATION) is not a perfect multiple of AUDIO_DURATION ($AUDIO_DURATION)."
    echo "The final video duration might be slightly shorter or longer than specified due to audio looping."
    # Optionally adjust total duration to the nearest multiple? Or just warn.
    # TOTAL_DURATION=$(( TOTAL_DURATION - REMAINDER ))
    # echo "Adjusted TOTAL_DURATION to ${TOTAL_DURATION}s for clean looping."
fi


echo "Generating a ${TOTAL_DURATION}-second black screen video (${TEMP_VIDEO_FILE})..."
ffmpeg -y -f lavfi -i color=c=black:s=${RESOLUTION}:d=${TOTAL_DURATION} \
       ${VIDEO_OPTS} \
       "${TEMP_VIDEO_FILE}"

if [ $? -ne 0 ]; then
    echo "Error: Failed to generate black video."
    exit 1
fi

echo ""
# Calculate loop count for the audio stream.
# -stream_loop N repeats the input N *additional* times.
# Loops needed = floor(Total Duration / Audio Duration) - 1
# Bash integer division handles floor automatically.
AUDIO_LOOP_COUNT=$(( TOTAL_DURATION / AUDIO_DURATION - 1 ))
if [ $AUDIO_LOOP_COUNT -lt 0 ]; then
    AUDIO_LOOP_COUNT=0 # Handle cases where total duration is less than audio duration
fi
echo "Looping the ${AUDIO_DURATION}-second audio file ${AUDIO_LOOP_COUNT} additional times..."

echo ""
echo "Combining the video with the looped audio file..."
# Use -c:v copy to avoid re-encoding the black video (faster)
# Use -shortest to ensure output duration matches the video stream length
ffmpeg -y -i "${TEMP_VIDEO_FILE}" -stream_loop ${AUDIO_LOOP_COUNT} -i "${AUDIO_FILE}" \
       -map 0:v:0 -map 1:a:0 \
       -c:v copy \
       ${AUDIO_OPTS} \
       -shortest \
       "${FINAL_OUTPUT}"

if [ $? -ne 0 ]; then
    echo "Error: Failed to combine video and audio."
    # Keep temp file for debugging if combination fails
    exit 1
fi

echo ""
echo "Cleaning up temporary files..."
rm "${TEMP_VIDEO_FILE}"

echo ""
echo "Final video generated: ${FINAL_OUTPUT}"


#-shortest \