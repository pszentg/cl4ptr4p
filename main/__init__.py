from main.audio_controller import AudioController

if __name__ == "__main__":
    ac = AudioController()

    while True:
        ac.listen()
