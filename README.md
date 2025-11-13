# content-making-scripts
Scripts and shortcuts for editing audio/video (e.g batch ffmpeg commands).

# FFmpeg Video Audio Processor

A Python script for Windows 11 that automates the workflow of extracting audio from videos, editing it in a DAW (like Reaper), and merging the edited audio back with the original video—all without re-encoding the video.

## 🎯 Purpose

This tool is perfect for content creators who need to:
- Extract audio from videos for editing in a DAW
- Replace video audio with professionally edited tracks
- Maintain original video quality (no re-encoding)
- Process multiple videos in batch

## ✨ Features

- **Extract audio** from MP4 videos without re-encoding (preserves original quality)
- **Merge edited audio** (WAV format) back with original video
- **No video re-encoding** - keeps original video stream intact
- **High-quality audio encoding** - 320 kbps AAC for maximum quality
- **Batch processing** - handles multiple videos automatically
- **Detailed logging** - see exactly what's happening at every step
- **Social media ready** - outputs MP4 files compatible with Instagram, YouTube, TikTok

## 📋 Prerequisites

### 1. Python
- Python 3.6 or higher
- Check if installed: `python --version` in Command Prompt

### 2. FFmpeg

#### Download and Install
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Get **ffmpeg-release-essentials.zip**
3. Extract to `C:\ffmpeg`

#### Add to System PATH
1. Press `Win + X` → **System** → **Advanced system settings**
2. Click **Environment Variables**
3. Under "System variables", find `Path` → **Edit** → **New**
4. Add: `C:\ffmpeg\bin`
5. Click **OK** on all dialogs
6. **Restart any open Command Prompt windows**

#### Verify Installation
```cmd
ffmpeg -version
```
You should see FFmpeg version information.

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ffmpeg-video-processor.git
cd ffmpeg-video-processor
```

2. No additional dependencies needed - uses Python standard library only!

## 📖 Usage

### Method 1: Command Line with Argument
```cmd
python process_videos.py "C:\path\to\your\video\folder"
```

### Method 2: Interactive Mode
```cmd
python process_videos.py
```
The script will prompt you to enter the folder path.

### Method 3: Drag and Drop (Easiest!)
1. Create a file named `run_processor.bat` with this content:
```batch
@echo off
python process_videos.py %1
pause
```
2. Drag your video folder onto the `.bat` file

## 🔄 Workflow Example

### Step 1: Initial Folder Structure
```
my_videos/
  ├── vacation.mp4
  └── tutorial.mp4
```

### Step 2: Run Script (First Time)
```cmd
python process_videos.py "C:\my_videos"
```

**Result:** Audio files are extracted
```
my_videos/
  ├── vacation.mp4
  ├── vacation.m4a          ← Extracted audio
  ├── tutorial.mp4
  └── tutorial.m4a          ← Extracted audio
```

### Step 3: Edit Audio in Your DAW
1. Import `.m4a` files into Reaper (or your preferred DAW)
2. Edit the audio (mixing, effects, etc.)
3. Export as **WAV** with the naming convention: `video_name-mix.wav`

**Recommended Reaper Export Settings:**
- **Format:** WAV
- **Sample Rate:** 48000 Hz (match video)
- **Bit Depth:** 24-bit or 32-bit float
- **Resample Mode:** r8brain free (or Medium/Good)

```
my_videos/
  ├── vacation.mp4
  ├── vacation.m4a
  ├── vacation-mix.wav      ← Your edited audio from Reaper
  ├── tutorial.mp4
  ├── tutorial.m4a
  └── tutorial-mix.wav      ← Your edited audio from Reaper
```

### Step 4: Run Script Again
```cmd
python process_videos.py "C:\my_videos"
```

**Result:** Final videos are created
```
my_videos/
  ├── vacation.mp4
  ├── vacation.m4a
  ├── vacation-mix.wav
  ├── vacation-mix.mp4      ← ✓ Final video with edited audio!
  ├── tutorial.mp4
  ├── tutorial.m4a
  ├── tutorial-mix.wav
  └── tutorial-mix.mp4      ← ✓ Final video with edited audio!
```

## 🎬 What the Script Does

### Stage 1: Audio Extraction
For each `.mp4` file in the folder:
```bash
ffmpeg -i video_name.mp4 -vn -acodec copy video_name.m4a
```
- Extracts audio without re-encoding
- Preserves original audio quality
- Creates `.m4a` files ready for DAW import

### Stage 2: Audio-Video Merge
For each `video_name-mix.wav` found:
```bash
ffmpeg -i video_name.mp4 -i video_name-mix.wav -c:v copy -c:a aac -b:a 320k -map 0:v:0 -map 1:a:0 video_name-mix.mp4
```
- Keeps original video stream (no re-encoding = no quality loss)
- Encodes audio to 320 kbps AAC (maximum quality)
- Creates social media-ready MP4 files

## 📝 Output Example

```
============================================================
FFMPEG VIDEO AUDIO PROCESSOR
============================================================
Folder: C:\Users\YourName\Videos\my_videos
Found 2 video file(s) to process

************************************************************
PROCESSING: vacation.mp4
************************************************************

[STEP 1/2] Extracting audio to: vacation.m4a
============================================================
STARTING: Extracting audio from vacation.mp4
============================================================
Command: ffmpeg -i vacation.mp4 -vn -acodec copy -y vacation.m4a

✓ SUCCESS: Extracting audio from vacation.mp4
✓ Audio extracted successfully: vacation.m4a

[STEP 2/2] Found edited audio: vacation-mix.wav
Creating new video: vacation-mix.mp4
============================================================
STARTING: Merging vacation-mix.wav with vacation.mp4
============================================================

✓ SUCCESS: Merging vacation-mix.wav with vacation.mp4
✓ Video created successfully: vacation-mix.mp4

============================================================
PROCESSING COMPLETE
============================================================
Audio files extracted: 2
Videos merged: 2
Errors: 0
============================================================
```

## 🎯 File Naming Convention

**Important:** Follow this naming pattern:

| Original Video | Extracted Audio | Edited Audio (from DAW) | Final Output |
|---------------|-----------------|------------------------|--------------|
| `video.mp4` | `video.m4a` | `video-mix.wav` | `video-mix.mp4` |
| `my_clip.mp4` | `my_clip.m4a` | `my_clip-mix.wav` | `my_clip-mix.mp4` |

The script automatically:
- Ignores files ending with `-mix.mp4` (to avoid processing output files)
- Looks for `-mix.wav` files to determine which videos need audio replacement

## ⚙️ Technical Details

### Why No Video Re-encoding?
- **Preserves quality:** Original video remains untouched
- **Fast processing:** Only audio is encoded
- **No generation loss:** Perfect for iterative editing

### Audio Quality
- **320 kbps AAC:** Indistinguishable from lossless for most listeners
- **Compatible:** Works with Instagram, YouTube, TikTok
- **Professional:** Suitable for content creation

### Platform Compatibility
The output MP4 files with AAC audio are compatible with:
- ✅ Instagram
- ✅ YouTube
- ✅ TikTok
- ✅ Facebook
- ✅ Twitter/X
- ✅ Most video platforms

## 🐛 Troubleshooting

### "ffmpeg not found"
- Make sure FFmpeg is installed
- Check that `C:\ffmpeg\bin` is in your system PATH
- Restart Command Prompt after adding to PATH

### "No .mp4 files found"
- Verify you're pointing to the correct folder
- Make sure video files have `.mp4` extension
- Check that files aren't named with `-mix.mp4` ending

### Audio/Video out of sync
- Ensure your DAW project sample rate matches the video (usually 48000 Hz)
- Check that exported WAV length matches the original audio length

### Script hangs or shows no output
- FFmpeg might be waiting for confirmation to overwrite files
- The script uses `-y` flag to avoid this, but check for error messages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FFmpeg](https://ffmpeg.org/)
- Designed for workflow with [Reaper DAW](https://www.reaper.fm/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for content creators**
