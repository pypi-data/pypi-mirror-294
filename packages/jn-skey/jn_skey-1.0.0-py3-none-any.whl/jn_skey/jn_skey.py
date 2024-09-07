from pynput import keyboard
from datetime import datetime

def main():
    print("SHORTCUT KEY FOR YYYY-MM-DD hh:mm:ss IS SHIFT + ALT + * (main keyboard)")

    def on_press(key):
        print("KEY PRESSED:", str(key))
        try:
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                keys_pressed.add('alt')
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                keys_pressed.add('shift')
            elif key.char == '*':
                keys_pressed.add('asterisk')

            if 'alt' in keys_pressed and 'shift' in keys_pressed and 'asterisk' in keys_pressed:
                type_datetime()
                keys_pressed.clear()  # Clear the set after typing
        except AttributeError:
            pass

    def on_release(key):
        print("KEY RELEASED:", key)
        try:
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                keys_pressed.discard('alt')
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                keys_pressed.discard('shift')
            elif key.char == '*':
                keys_pressed.discard('asterisk')
        except AttributeError:
            pass

    def type_datetime():
        print("Typing datetime...")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        controller.release(keyboard.Key.alt_l)
        controller.release(keyboard.Key.shift_l)
        print("Current Time:", current_time)
        controller.type(current_time)

    keys_pressed = set()
    controller = keyboard.Controller()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
