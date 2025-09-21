import argparse
import os
import subprocess
import shutil
import json

NAMESPACE = "shrek"
LEFT_POS = "-319.5 93 -324.5"
RIGHT_POS = "-319.5 93 -327.5"

def check_prog(name):
    from shutil import which
    return which(name) is not None

def split_audio(input_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    left_path = os.path.join(out_dir, "left.ogg")
    right_path = os.path.join(out_dir, "right.ogg")

    subprocess.run([
        "ffmpeg", "-y", "-i", input_file,
        "-filter_complex", "channelsplit=channel_layout=stereo[left][right]",
        "-map", "[left]", left_path,
        "-map", "[right]", right_path
    ], check=True)

    return left_path, right_path

def generate_sounds_json(namespace, out_dir):
    sounds = {
        "left": {"sounds": [{"name": f"{namespace}:left", "stream": True}]},
        "right": {"sounds": [{"name": f"{namespace}:right", "stream": True}]}
    }
    path = os.path.join(out_dir, "sounds.json")
    with open(path, "w") as f:
        json.dump(sounds, f, indent=4)
    print(f"Generated {path}")

def create_resourcepack(base_dir, left_file, right_file):
    rp_dir = os.path.join(base_dir, "resourcepack", "assets", NAMESPACE, "sounds")
    os.makedirs(rp_dir, exist_ok=True)
    shutil.copy(left_file, os.path.join(rp_dir, "left.ogg"))
    shutil.copy(right_file, os.path.join(rp_dir, "right.ogg"))

    generate_sounds_json(NAMESPACE, os.path.join(base_dir, "resourcepack", "assets", NAMESPACE))

    # pack.mcmeta
    pack_meta = {
        "pack": {
            "pack_format": 15,
            "description": f"{NAMESPACE} audio pack"
        }
    }
    with open(os.path.join(base_dir, "resourcepack", "pack.mcmeta"), "w") as f:
        json.dump(pack_meta, f, indent=4)

    print("Resourcepack ready!")

def create_datapack(base_dir):
    dp_base = os.path.join(base_dir, "datapack", "data", NAMESPACE)
    functions_dir = os.path.join(dp_base, "functions")
    os.makedirs(functions_dir, exist_ok=True)

    # Function to play audio and mark player
    mcfunction_path = os.path.join(functions_dir, "play_audio.mcfunction")
    with open(mcfunction_path, "w") as f:
        f.write("# Ensure scoreboard exists\n")
        f.write("scoreboard objectives add joined dummy\n")
        # Play sounds only for players who haven't triggered yet
        f.write(f"playsound {NAMESPACE}:left master @a[scores={{joined=0}}] {LEFT_POS}\n")
        f.write(f"playsound {NAMESPACE}:right master @a[scores={{joined=0}}] {RIGHT_POS}\n")
        f.write("scoreboard players set @a[scores={joined=0}] joined 1\n")
    print(f"Generated {mcfunction_path}")

    # Tick tag
    tick_dir = os.path.join(dp_base, "tags", "functions")
    os.makedirs(tick_dir, exist_ok=True)
    tick_path = os.path.join(tick_dir, "tick.json")
    with open(tick_path, "w") as f:
        json.dump({"values": [f"{NAMESPACE}:play_audio"]}, f, indent=4)

    # pack.mcmeta for datapack
    pack_meta = {
        "pack": {
            "pack_format": 15,
            "description": f"{NAMESPACE} join-sound datapack"
        }
    }
    with open(os.path.join(base_dir, "datapack", "pack.mcmeta"), "w") as f:
        json.dump(pack_meta, f, indent=4)

    print("Datapack ready! Tick function ensures sounds play on world join.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input video file (MP4)")
    parser.add_argument("--output", "-o", default="output", help="Base output folder")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise SystemExit("Input file not found.")
    if not check_prog("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH.")

    base_dir = os.path.abspath(args.output)
    os.makedirs(base_dir, exist_ok=True)

    # Split audio
    left_file, right_file = split_audio(args.input, os.path.join(base_dir, "sounds_tmp"))

    # Create resourcepack
    create_resourcepack(base_dir, left_file, right_file)

    # Create datapack
    create_datapack(base_dir)

    # Cleanup temp audio
    shutil.rmtree(os.path.join(base_dir, "sounds_tmp"))
    print(f"All done! Resourcepack and datapack in {base_dir}")

if __name__ == "__main__":
    main()
