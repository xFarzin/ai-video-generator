from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
import time


def create_video(image_paths, audio_paths, output_path="output/final_video.mp4"):
    """Combine images and audio into a slideshow video"""

    print("=" * 60)
    print("VIDEO ASSEMBLER STARTED")
    print("=" * 60)

    start_time = time.time()

    Path("output").mkdir(parents=True, exist_ok=True)

    clips = []

    print(f"Images count: {len(image_paths)}")
    print(f"Audio count : {len(audio_paths)}")

    for i, (img_path, audio_path) in enumerate(zip(image_paths, audio_paths)):

        print("\n" + "-" * 40)
        print(f"Processing slide {i+1}")
        print("-" * 40)

        if not img_path or not audio_path:
            print(f"Skipping slide {i+1} (missing image or audio)")
            continue

        print(f"Image path: {img_path}")
        print(f"Audio path: {audio_path}")

        try:
            print("Loading audio...")
            audio_clip = AudioFileClip(audio_path)

            duration = audio_clip.duration

            print(f"Audio duration: {duration:.2f} sec")

            print("Creating image clip...")
            image_clip = ImageClip(img_path, duration=duration)

            print("Attaching audio...")
            image_clip = image_clip.set_audio(audio_clip)

            print("Resizing image...")
            image_clip = image_clip.resize(height=1080)

            print("Adding clip to list...")
            clips.append(image_clip)

            print(f"Slide {i+1} ready")

        except Exception as e:
            print(f"ERROR while processing slide {i+1}")
            print(str(e))
            raise

    print("\n" + "=" * 60)
    print(f"Finished preparing clips. Total clips: {len(clips)}")
    print("=" * 60)

    if not clips:
        raise Exception("No valid clips to concatenate")

    try:
        print("Starting concatenate_videoclips()...")
        concat_start = time.time()

        final_clip = concatenate_videoclips(
            clips,
            method="compose"
        )

        print(
            f"Concatenation finished in "
            f"{time.time() - concat_start:.2f} sec"
        )

    except Exception as e:
        print("ERROR during concatenation")
        print(str(e))
        raise

    try:
        print("\n" + "=" * 60)
        print("STARTING VIDEO RENDER")
        print("=" * 60)

        render_start = time.time()
        print("Calling write_videofile()...")
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger="bar"
        )
        print("write_videofile() returned")
        print(
            f"Render completed in "
            f"{time.time() - render_start:.2f} sec"
        )

    except Exception as e:
        print("ERROR during write_videofile()")
        print(str(e))
        raise

    print("\nStarting cleanup...")

    try:
        print("Closing final clip...")
        final_clip.close()
        print("Final clip closed")

        for idx, clip in enumerate(clips):
            print(f"Closing clip {idx+1}...")
            clip.close()

        print("All clips closed")

    except Exception as e:
        print("ERROR during cleanup")
        print(str(e))
        raise

    total_time = time.time() - start_time

    print("\n" + "=" * 60)
    print("VIDEO ASSEMBLER FINISHED")
    print(f"Output file: {output_path}")
    print(f"Total time: {total_time:.2f} sec")
    print("=" * 60)

    return output_path