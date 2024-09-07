# TimeLapser

**TimeLapser** is a Python CLI tool for recording screen activity and saving it as a video file. It uses OpenCV and FFMPEG for video encoding and supports multiple monitor setups. You can customize the recording settings such as frame rate, video format, and monitor selection. The tool also provides functionality to list available monitors and display a recording timer.

## Features

- Record screen activity from a selected monitor.
- Save recordings in MP4 or AVI format.
- Specify the output directory.
- Option to set the frames per second (FPS) for recording.
- Display a timer showing elapsed recording time.
- List available monitors with their resolutions.

## Requirements

- Python 3.10+
- [OpenCV](https://opencv.org/) (`cv2`)
- [NumPy](https://numpy.org/)
- [MSS](https://github.com/BoboTiG/python-mss)
- [Pynput](https://pypi.org/project/pynput/)
- [Rich](https://github.com/Textualize/rich)
- [FFMPEG](https://ffmpeg.org/) (Ensure FFMPEG is installed and accessible in your PATH)

## Installation

1. Install using `pip`:

   ```bash
   pip install timelapser
   ```

   Or install from [GitHub](https://github.com/asibhossen897/TimeLapser):

   ```bash
   pip install git+https://github.com/asibhossen897/timelapser.git
   ```

2. **Ensure FFMPEG is installed:**

    To check if FFMPEG is installed, run the following command:

   ```bash
   ffmpeg -version
   ```

   If FFMPEG is not installed, you can install it using the following commands:

   - **Linux:**
    
      - Ubuntu/Debian

        ```bash
        sudo apt-get update
        sudo apt-get install ffmpeg
        ```

      - RHEL/CentOS/Fedora

        ```bash
        sudo yum install ffmpeg
        ```

      - Arch Linux

        ```bash
        sudo pacman -S ffmpeg
        ```

   - **macOS:**

     ```bash
     brew install ffmpeg
     ```

   - **Windows:**
     Download and install from the [FFMPEG official site](https://ffmpeg.org/download.html) and add it to your PATH.

> Important:
> The program will not work if FFMPEG is not installed.


## Usage

### Start Recording

To start recording, use the `record` command:

```bash
timelapser record --fps 30 --mp4 --monitor_index 0 --output_dir Recordings
```

or Download and use `timelapser.py` file from the [GitHub repository](https://github.com/asibhossen897/TimeLapser):

```bash
python timelapser.py record --fps 30 --mp4 --monitor_index 0 --output_dir Recordings
```

**Options:**

- `--fps`: Frames per second (e.g., 30, Default is 100).
- `--mp4`: Save the video in MP4 format. Use `--avi` for AVI format.
- `--monitor_index`: Index of the monitor to record from (default is 0).
- `--output_dir`: Directory where the video will be saved (default is "Outputs").

### Stop Recording

To stop recording, press `Q` on your keyboard.

### List Monitors

To list all available monitors and their resolutions, use:

```bash
timelapser list-monitors
```

## Code Organization

- `timelapser/main.py`: Contains the CLI commands and main logic for recording and listing monitors.
- `timelapser/recorder.py`: Contains functions for creating videos, recording frames, and handling output directories.
- `timelapser/utils.py`: Contains utility functions for generating timestamps and video formats.
- `requirements.txt`: Lists the Python dependencies.

## Bugs and Feature Requests
- When you have any bug or feature request, please [open an issue](https://github.com/asibhossen897/TimeLapser/issues/new/choose) on GitHub.

## Contributing

Feel free to contribute to this project by submitting issues, feature requests, or pull requests. Ensure you follow the coding style and include tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [dev.asib@proton.me](mailto:dev.asib@proton.me).
