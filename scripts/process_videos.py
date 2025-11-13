import os
import subprocess
import sys
from pathlib import Path

def run_ffmpeg_command(command, description):
    """
    Execute an ffmpeg command and provide detailed logging
    
    Args:
        command: List of command arguments for ffmpeg
        description: Human-readable description of what the command does
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"STARTING: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}\n")
    
    try:
        # Run the command and capture output
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Print output in real-time
        for line in process.stderr:
            print(line, end='')
        
        # Wait for completion
        process.wait()
        
        if process.returncode == 0:
            print(f"\n✓ SUCCESS: {description}")
            return True
        else:
            print(f"\n✗ FAILED: {description} (Exit code: {process.returncode})")
            return False
            
    except FileNotFoundError:
        print("\n✗ ERROR: ffmpeg not found! Make sure ffmpeg is installed and in your PATH.")
        print("Download from: https://www.gyan.dev/ffmpeg/builds/")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {description} - {str(e)}")
        return False

def extract_audio(video_path, audio_path):
    """Extract audio from video without re-encoding"""
    command = [
        'ffmpeg',
        '-i', str(video_path),
        '-vn',  # No video
        '-acodec', 'copy',  # Copy audio codec without re-encoding
        '-y',  # Overwrite output file if exists
        str(audio_path)
    ]
    
    return run_ffmpeg_command(
        command,
        f"Extracting audio from {video_path.name}"
    )

def merge_audio_video(video_path, audio_path, output_path):
    """Merge edited audio with original video without re-encoding video"""
    command = [
        'ffmpeg',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'copy',  # Copy video without re-encoding
        '-c:a', 'aac',  # Encode audio to AAC
        '-b:a', '320k',  # Maximum quality AAC
        '-map', '0:v:0',  # Take video from first input
        '-map', '1:a:0',  # Take audio from second input
        '-y',  # Overwrite output file if exists
        str(output_path)
    ]
    
    return run_ffmpeg_command(
        command,
        f"Merging {audio_path.name} with {video_path.name}"
    )

def process_folder(folder_path):
    """
    Process all videos in the specified folder
    
    Args:
        folder_path: Path to the folder containing video files
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"✗ ERROR: Folder '{folder_path}' does not exist!")
        return
    
    # Find all .mp4 files
    video_files = list(folder.glob("*.mp4"))
    
    # Filter out files that end with -mix.mp4 (these are output files)
    video_files = [v for v in video_files if not v.stem.endswith("-mix")]
    
    if not video_files:
        print(f"✗ No .mp4 video files found in '{folder_path}'")
        return
    
    print(f"\n{'#'*60}")
    print(f"FFMPEG VIDEO AUDIO PROCESSOR")
    print(f"{'#'*60}")
    print(f"Folder: {folder.absolute()}")
    print(f"Found {len(video_files)} video file(s) to process\n")
    
    stats = {
        'audio_extracted': 0,
        'videos_merged': 0,
        'errors': 0
    }
    
    for video_file in video_files:
        video_stem = video_file.stem  # Filename without extension
        
        print(f"\n{'*'*60}")
        print(f"PROCESSING: {video_file.name}")
        print(f"{'*'*60}")
        
        # Step 1: Extract audio as .m4a
        audio_m4a_path = folder / f"{video_stem}.m4a"
        
        print(f"\n[STEP 1/2] Extracting audio to: {audio_m4a_path.name}")
        if extract_audio(video_file, audio_m4a_path):
            stats['audio_extracted'] += 1
            print(f"✓ Audio extracted successfully: {audio_m4a_path.name}")
        else:
            stats['errors'] += 1
            print(f"✗ Failed to extract audio from: {video_file.name}")
            continue
        
        # Step 2: Check if there's a corresponding -mix.wav file
        mix_wav_path = folder / f"{video_stem}-mix.wav"
        
        if mix_wav_path.exists():
            print(f"\n[STEP 2/2] Found edited audio: {mix_wav_path.name}")
            output_video_path = folder / f"{video_stem}-mix.mp4"
            
            print(f"Creating new video: {output_video_path.name}")
            if merge_audio_video(video_file, mix_wav_path, output_video_path):
                stats['videos_merged'] += 1
                print(f"✓ Video created successfully: {output_video_path.name}")
            else:
                stats['errors'] += 1
                print(f"✗ Failed to merge audio with video")
        else:
            print(f"\n[STEP 2/2] No edited audio found (looking for: {mix_wav_path.name})")
            print("Skipping video merge step.")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Audio files extracted: {stats['audio_extracted']}")
    print(f"Videos merged: {stats['videos_merged']}")
    print(f"Errors: {stats['errors']}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("\nFFmpeg Video Audio Processor")
    print("=" * 60)
    
    # Check if folder path was provided as argument
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # Ask user for folder path
        folder_path = input("Enter the folder path containing video files: ").strip('"')
    
    if folder_path:
        process_folder(folder_path)
    else:
        print("✗ No folder path provided!")
    
    input("\nPress Enter to exit...")
