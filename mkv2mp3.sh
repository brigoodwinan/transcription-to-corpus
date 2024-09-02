#!/bin/zsh

ffmpeg -i $1 -vn -ar 44100 -ac 2 -ab 192k -f mp3 $2

ffmpeg -i input_video.mp4 -vn -acodec copy output_audio.mp4
