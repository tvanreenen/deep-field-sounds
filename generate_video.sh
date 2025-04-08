#!/bin/bash
# This script generates a 10-minute black screen video chunk,
# then loops it and combines it with your pre-generated audio file
# (deep_field_12hr.wav) to produce a 12-hour video.
#
# Requirements:
# - A pre-generated WAV file named "deep_field_12hr.wav"
# - ffmpeg installed on your system

# Set parameters
TOTAL_DURATION=600          # Total duration in seconds (10 minutes for test)
CHUNK_DURATION=600            # Duration of the single chunk (10 minutes = 600 seconds)
RESOLUTION="1920x1080"        # Video resolution
CHUNK_FILENAME="black_chunk.mp4"  # Temporary chunk filename
AUDIO_FILE="binaural_beat_100Hz_L_102.0Hz_R_5.0s.wav"    # Your 5-second audio file
FINAL_OUTPUT="binaural_beat_10min_test.mp4"   # Final output filename for test

echo "Generating a ${CHUNK_DURATION}-second black screen video chunk..."
ffmpeg -y -f lavfi -i color=c=black:s=${RESOLUTION}:d=${CHUNK_DURATION} \
       -c:v libx264 -crf 18 -preset veryslow \
       -pix_fmt yuv420p "${CHUNK_FILENAME}"

echo ""
# Calculate loop count.
# -stream_loop N repeats the input N additional times.
# For a 10-minute chunk to reach 12 hours:
#   (43200 / 600) - 1 = 72 - 1 = 71 extra loops.
LOOP_COUNT=$(( TOTAL_DURATION / CHUNK_DURATION - 1 ))
echo "Looping the chunk ${LOOP_COUNT} times to create a ${TOTAL_DURATION}-second video..."

echo ""
echo "Combining the looped video with the audio file..."
ffmpeg -y -stream_loop ${LOOP_COUNT} -i "${CHUNK_FILENAME}" -i "${AUDIO_FILE}" \
       -c:v libx264 -crf 18 -preset veryslow \
       -c:a aac -b:a 192k \
       -pix_fmt yuv420p "${FINAL_OUTPUT}"
echo ""
echo "Final video generated: ${FINAL_OUTPUT}"


#-shortest \