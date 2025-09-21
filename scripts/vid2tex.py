import argparse
import os
import subprocess
import numpy as np
import png
import json

def check_prog(name):
    from shutil import which
    return which(name) is not None

def ffmpeg_extract_frames(video_path, fps, width, height, pad_color="black", debug_frame=None):
    """
    Extract RGBA frames from video scaled to width x height with padding as needed.
    Returns a vertically stacked NumPy array.
    Optionally saves a debug frame for inspection.
    """
    # FFmpeg pad color syntax
    pad_arg = {
        "black": "black",
        "white": "white",
        "transparent": "color=0x00000000"
    }[pad_color.lower()]

    vf = f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease," \
         f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:{pad_arg},format=rgba"

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", video_path,
        "-vf", vf,
        "-vsync", "0",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "pipe:1"
    ]

    frame_size = width * height * 4
    frames = []

    print(f"Extracting frames from {video_path} at {width}x{height}, fps={fps} ...")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8) as proc:
        idx = 0
        while True:
            raw = proc.stdout.read(frame_size)
            if not raw:
                break
            if len(raw) != frame_size:
                print(f"[WARN] Frame {idx} has {len(raw)} bytes (expected {frame_size}). Skipping.")
                idx += 1
                continue

            frame = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 4))

            # Save debug frame if requested
            if debug_frame is not None and idx == debug_frame:
                png.from_array(frame.reshape(-1, 4), "RGBA").save(f"debug_frame_{debug_frame}.png")
                print(f"[DEBUG] Saved frame {debug_frame} as debug_frame_{debug_frame}.png")
                print(f"[DEBUG] Frame shape: {frame.shape}")
                print(f"[DEBUG] First 5 pixels of first row: {frame[0,:5]}")

            frames.append(frame)
            idx += 1

        proc.wait()

    if not frames:
        raise RuntimeError("No frames extracted. Check ffmpeg input/filters.")

    stacked = np.vstack(frames)
    print(f"Extracted {len(frames)} frames, stacked shape: {stacked.shape}")
    return stacked, len(frames)

def save_vertical_png(image: np.ndarray, out_path: str):
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    # Each row flattened for PyPNG
    rows = [row.flatten().tolist() for row in image]
    png.from_array(rows, "RGBA").save(out_path)
    print(f"[PNG Save] Saved {image.shape[1]}x{image.shape[0]} RGBA -> {out_path}")

def generate_mcmeta(png_path, frame_width, frame_height, fps=20, interpolate=False, total_frames=None):
    """
    Generate a .mcmeta file for a vertically stacked texture.
    """
    if total_frames is None:
        raise ValueError("total_frames must be provided.")

    frametime = max(1, min(20, int(round(20 / fps))))
    mcmeta = {
        "animation": {
            "interpolate": interpolate,
            "width": frame_width,
            "height": frame_height,
            "frametime": frametime,
            "frames": list(range(total_frames))
        }
    }

    mcmeta_path = os.path.splitext(png_path)[0] + ".png.mcmeta"
    with open(mcmeta_path, "w") as f:
        json.dump(mcmeta, f, indent=4)
    print(f"Generated {mcmeta_path} with {total_frames} frames.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument("--fps", "-r", type=float, default=20.0)
    parser.add_argument("--output", "-o", default="texture.png")
    parser.add_argument("--pad", choices=["black","white","transparent"], default="black")
    parser.add_argument("--debug_frame", type=int, default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise SystemExit("Input file not found.")
    if not check_prog("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH.")

    stacked, total_frames = ffmpeg_extract_frames(
        args.input, fps=args.fps,
        width=args.width, height=args.height,
        pad_color=args.pad, debug_frame=args.debug_frame
    )
    save_vertical_png(stacked, args.output)
    generate_mcmeta(args.output, frame_width=args.width, frame_height=args.height, fps=args.fps, total_frames=total_frames)
    print("Done.")

if __name__ == "__main__":
    main()
