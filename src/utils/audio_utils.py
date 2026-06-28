import sounddevice as sd


def get_audio_devices():
    devices = sd.query_devices()
    inputs = []
    outputs = []

    for idx, dev in enumerate(devices):
        device_info = {"id": idx, "name": dev["name"]}

        if dev["max_input_channels"] > 0:
            inputs.append(device_info)

        if dev["max_output_channels"] > 0:
            outputs.append(device_info)

    return inputs, outputs
