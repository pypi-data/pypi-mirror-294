import typer
from pynput import keyboard
import time
import mss
from rich import print
from rich.table import Table
from rich.panel import Panel
from .recorder import create_video, recorder
from .utils import display_timer, console

app = typer.Typer()

stop_recording = False


def on_press(key):
    global stop_recording
    try:
        if key.char == "Q":
            console.print(Panel(
                "[bold red]Are you sure you want to stop recording? (y/n): [/bold red]",
                border_style="bold red",
                title="Warning!",
                style="red",
            ))

            user_input = input(">> ")
            if user_input.lower() == "y":
                stop_recording = True
    except AttributeError:
        pass


@app.command()
def record(
    fps: int = 100,
    mp4: bool = True,
    monitor_index: int = 0,
    output_dir: str = "Outputs",
):
    """
    Start recording from the selected monitor.

    Args:
    fps: Frames per second for the video.
    mp4: If set to True, the video will be saved in .mp4 format, else .avi.
    monitor_index: Index of the monitor to record from. Default is monitor 0.
    output_dir: Directory where the video will be saved. Default is "Outputs".
    """
    monitors = mss.mss().monitors
    if monitor_index < 0 or monitor_index >= len(monitors):
        typer.echo("Invalid monitor index. Please provide a valid index.")
        raise typer.Exit()

    selected_monitor = monitors[monitor_index]
    screen_size = (selected_monitor["width"], selected_monitor["height"])
    out, file_path = create_video(fps, mp4, screen_size, output_dir)

    print(
        Panel(
            f"[bold green]Recording from monitor: [/bold green][bold magenta]{monitor_index} [{screen_size[0]}x{screen_size[1]}] [/bold magenta]\n[bold red]Press 'Q' to stop recording![/bold red]",
            border_style="bold green",
            title="Recording Status",
            style="green",
        )
    )
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    start_time = time.time()

    while not stop_recording:
        current_time = time.time()
        elapsed_time = current_time - start_time
        # display_timer(console, elapsed_time)
        recorder(out, selected_monitor)
        time.sleep(0.1)

    listener.stop()
    out.release()

    console.print(" " * 50, end="\r")

    print(
        Panel(
            f"[bold green]Recording finished and saved.[/bold green]\n"
            f"[bold magenta]File saved at: {file_path}[/bold magenta]",
            border_style="bold green",
            title="Recording Status",
            subtitle="File saved successfully",
            style="green",
        )
    )


@app.command()
def list_monitors():
    monitors = mss.mss().monitors
    table = Table(title="Available Monitors", width=50, show_lines=True)
    table.add_column("Monitor", justify="center", style="cyan", no_wrap=True)
    table.add_column("Resolution", justify="center", style="magenta")

    for i, monitor in enumerate(monitors):
        width = monitor["width"]
        height = monitor["height"]
        table.add_row(f"{i}", f"{width}x{height}")

    print(table)
