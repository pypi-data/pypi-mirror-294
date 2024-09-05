import os
import argparse
import random
import textwrap
from pydub import AudioSegment
from pydub.playback import play

def get_douroucouli_art(name):
    """Fetch the ASCII art for the specified douroucouli."""
    current_dir = os.path.dirname(__file__)
    asset_path = os.path.join(current_dir, 'assets', f'{name}.txt')
    if not os.path.exists(asset_path):
        raise FileNotFoundError(f"Asset file '{asset_path}' not found.")
    with open(asset_path, 'r') as file:
        return file.read()

def create_speech_bubble(message):
    """Create a speech bubble around the message."""
    wrapped_message = textwrap.fill(message, width=40)
    lines = wrapped_message.splitlines()
    width = max(len(line) for line in lines)
    border = '-' * (width + 2)

    bubble = f"  {border}\n"
    for line in lines:
        bubble += f" < {line.ljust(width)} >\n"
    bubble += f"  {border}"

    return bubble

def get_asset_path(filename):
    """Return the path to an asset file."""
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'assets', filename)

def douroucoulisay(message, douroucouli=None):
    """Print the message with a randomly selected douroucouli ASCII art."""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    
    if douroucouli is None:
        # Randomly select a douroucouli file from the assets directory
        available_douroucouli = [f.split('.')[0] for f in os.listdir(assets_dir) if f.endswith('.txt')]
        douroucouli = random.choice(available_douroucouli)
    
    try:
        douroucouli_art = get_douroucouli_art(douroucouli)
    except FileNotFoundError:
        raise ValueError(f"Douroucouli '{douroucouli}' not found.")
    
    bubble = create_speech_bubble(message)
    print(f"\n{bubble}\n\n{douroucouli_art}")

def tonal_hoot(repeat_count=1):
    """Play the 'tonal hoot' sound the specified number of times."""
    sound = AudioSegment.from_wav(get_asset_path('FemaleAnancymaaeHoot - Pine Girl.wav'))
    for _ in range(repeat_count):
        play(sound)

def gruff_hoot(repeat_count=1):
    """Play the 'gruff hoot' sound the specified number of times."""
    sound = AudioSegment.from_wav(get_asset_path('MaleAnancymaaeHoot - Onassis1.wav'))
    for _ in range(repeat_count):
        play(sound)

def whoop(repeat_count=1):
    """Play the 'whoop' sound the specified number of times."""
    sound = AudioSegment.from_wav(get_asset_path('FemaleAnancymaaeResonantWhoop - Spruce.wav'))
    for _ in range(repeat_count):
        play(sound)

def main():
    parser = argparse.ArgumentParser(description="Print a message with douroucouli ASCII art.")
    parser.add_argument("message", type=str, help="The message to display.")
    parser.add_argument("-d", "--douroucouli", type=str, help="The douroucouli to use. If not provided, a random douroucouli will be selected.")
    
    args = parser.parse_args()
    douroucoulisay(args.message, args.douroucouli)

if __name__ == "__main__":
    main()
