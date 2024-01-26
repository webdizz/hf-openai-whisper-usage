## Convert video to wav

```bash
 ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav
```

## Convert wav audio to optimized audio ogg chunked in 10 minutes

```bash
ffmpeg -i ./wav/audio.wav -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -f segment -segment_time 600 -application voip  ./wav/audio_%03d.ogg
```

## Convert wav audio to optimized audio ogg (batch)

```bash
for file in ./wav/*.wav; do
    ffmpeg -i "$file" -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -f segment -segment_time 600 -application voip "${file%.wav}_%03d.ogg"
done
```

## How to run

### Create `.env` file to set environment variables

```bash
HF_API_TOKEN=hf_....
# Whisper large-v2 https://huggingface.co/openai/whisper-large-v2
HF_API_URL=https://.....endpoints.huggingface.cloud
```