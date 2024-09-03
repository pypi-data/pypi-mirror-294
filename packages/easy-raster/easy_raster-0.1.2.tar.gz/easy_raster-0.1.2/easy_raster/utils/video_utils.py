from pathlib import Path


def make_video(input_glob: Path | str, output: Path | str, fps: int = 1):
    import ffmpeg

    (
        ffmpeg
        .input(str(input_glob), pattern_type='glob', framerate=fps)
        .output(str(output), loglevel="quiet")
        .overwrite_output()
        .run()
    )
