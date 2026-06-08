import pathlib
import os
import shutil
import ffmpeg

DEFAULT_CACHE_PATH = pathlib.Path("~/.config/SPlayer/DataCache/music").expanduser()
def concat_tracks(tracklist: list[pathlib.Path], output_file: pathlib.Path):
    # Copied from `track-sorter` (github.com/kyv001/track-sorter, MIT License)
    try:
        # 为每个输入文件明确选择音频流
        audio_streams = []
        for track in tracklist:
            input_file = ffmpeg.input(str(track.resolve()))
            # 明确选择第一个音频流
            audio_streams.append(input_file['a:0'])

        # 使用ffmpeg.concat连接所有音频流，并设置专辑名元数据
        (
            ffmpeg.concat(*audio_streams, v=0, a=1)
            .output(
                str(output_file.resolve()),
                metadata=f"title={output_file.stem}",
                format="mp3",
                audio_bitrate=320_000 # 320kbps
            )
            .run()
        )
    except Exception as e:
        print(f"Error concatenating tracks: {e}")
        return False
    return True

def cli():
    print("CP Cache CLI")
    # ----- Cache Path -----
    print(f"Default cache path: {DEFAULT_CACHE_PATH}")
    ask_path = input("Confirm? (Y/enter path): ").strip()
    if not ask_path or ask_path.lower() == "y":
        cache_path = DEFAULT_CACHE_PATH
    else:
        try:
            cache_path = pathlib.Path(ask_path).expanduser()
        except ValueError:
            print("Invalid cache path")
            return 1
    print(f"Using cache path: {cache_path}")
    # ----- Target Path -----
    target_path = input("Enter target path: ").strip()
    try:
        target_path = pathlib.Path(target_path).expanduser().resolve()
    except ValueError:
        print("Invalid target path")
        return 1
    os.makedirs(target_path, exist_ok=True)
    print(f"Using target path: {target_path}")
    # ----- Main Loop: Match tracks and cached files -----
    count: int = 0
    moving_files: dict[pathlib.Path, pathlib.Path] = {}
    while True:
        try:
            track_id = int(input("Enter track ID (^C or ^D to exit): ").strip())
        except ValueError:
            print("Invalid track ID")
            continue
        except (KeyboardInterrupt, EOFError): # ^C or ^D
            break
        matched_fnames = [*filter(lambda x: x.startswith(f"{track_id}_"), os.listdir(cache_path))]
        if not matched_fnames:
            print(f"No files found for track ID {track_id}")
            continue
        if len(matched_fnames) > 1: # Might be matching multiple files with the same track ID but different quality
            print(f"Multiple files found for track ID {track_id}: {matched_fnames}")
            while True: # Don't ask for track ID again in case of invalid file index
                choice = input(f"Enter file index (0-{len(matched_fnames)-1}): ").strip()
                try:
                    choice = int(choice)
                    fname = matched_fnames[choice]
                except (IndexError, ValueError):
                    print("Invalid file index")
                    continue
                break
        else:
            fname = matched_fnames[0] # Only one file found, use it

        print(f"Using file: {fname}")
        count += 1
        target_fname = input("Enter target file name (without extension): ").strip() + ".mp3"  # Most cached audio seem to be mp3.
                                                                                               # Some might be wav, flac, etc.,
                                                                                               # but don't bother detecting it.
        print(f"{fname} -> {target_fname}")
        moving_files[cache_path / fname] = target_path / target_fname
    # ----- Concatenate Tracks -----
    ask_number = input("Would you like to add track id prefix? (Y/n): ").strip()
    if not ask_number.lower() == "n":
        for i, (fname, target) in enumerate(moving_files.items()):
            prefix = str(i + 1).zfill(len(str(count)))
            moving_files[fname] = target_path / f"{prefix} - {target.name}"
            print(f"{fname} -> {moving_files[fname]}")
    for fname, target in moving_files.items():
        shutil.move(fname, target)
    album_name = input("Enter album name (leave blank to skip): ").strip()
    if not album_name:
        return 0
    output_file = target_path / f"{album_name}.mp3"
    if not concat_tracks([*moving_files.values()], output_file):
        return 1
