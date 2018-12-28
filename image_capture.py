from picamera import PiCamera
import time
import io

class ImageCapture:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.led = False
        self.camera.start_preview()
        time.sleep(2)

    def capture(self):
        tmp_stream = io.BytesIO()
        self.camera.capture(tmp_stream, 'jpeg')
        tmp_stream.seek(0)
        return tmp_stream

    def capture_video(self, duration):
        tmp_stream = io.BytesIO()
        self.camera.start_recording(tmp_stream, format='h264')
        self.camera.wait_recording(duration)
        self.camera.stop_recording()
        tmp_stream.seek(0)
        return tmp_stream

    @staticmethod
    def write_stream(stream, file_path):
        with open(file_path, 'wb') as f:
            f.write(stream.read())
