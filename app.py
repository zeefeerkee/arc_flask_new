from flask import Flask, render_template, Response, request
import cv2
from control.ContolByte import ControlByte

app = Flask(__name__)
camera = cv2.VideoCapture(0)
control_byte = ControlByte()

id_control = {
    '1': control_byte.increase,
    '2': control_byte.decrease,
    '3': lambda: control_byte.direction(0),
    '4': lambda: control_byte.direction(1),
    '5': control_byte.stop,
    '6': lambda: control_byte.servo(0),
    '7': lambda: control_byte.servo(1),
}

def getFramesGenerator():
    """ Генератор фреймов для вывода в веб-страницу"""
    while True:
        success, frame = camera.read()  # Получаем фрейм с камеры
        if success:
            # уменьшаем разрешение кадров
            frame = cv2.resize(frame, (1080, 720), interpolation=cv2.INTER_AREA)
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/update_values', methods=['POST'])
def update_values():
    """
    Обработка обновления значений direction и progress
    """
    move_id = request.form['move']
    id_control[move_id]()
    print(move_id, bin(control_byte.get_byte()))

    return 'Success'

@app.route("/")
def index():
    return render_template('index.html')

            
@app.route('/video_feed')
def video_feed():
    """
    Генерируем и отправляем изображения с камеры
    """
    return Response(getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')