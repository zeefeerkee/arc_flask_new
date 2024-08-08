from flask import Flask, render_template, Response, request
import cv2
from flask.json import jsonify
from control.ContolByte import ControlByte
import serial

app = Flask(__name__)
camera = cv2.VideoCapture(0)
control_byte = ControlByte()
arduino = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
current_colormap = None


id_control = {
    '1': (control_byte.increase, "increase"),
    '2': (control_byte.decrease, "decrease"),
    '4': (lambda: control_byte.direction(0), "forward"),
    '3': (lambda: control_byte.direction(1), "backward"),
    '5': (control_byte.stop, "stop"),
    '6': (lambda: control_byte.servo(0), "expansion"),
    '7': (lambda: control_byte.servo(1), "closing"),
    '8': (lambda: set_colormap(None), "standart"),
    '9': (lambda: set_colormap(cv2.COLORMAP_COOL), "cool colormap"),
    '10': (lambda: set_colormap(cv2.COLORMAP_RAINBOW), "rainbow colormap"),
    '11': (lambda: set_colormap(cv2.COLORMAP_HOT), "hot colormap"),
    '12': (lambda: set_colormap(cv2.COLORMAP_JET), "jet colormap"),
}



def set_colormap(colormap):
    global current_colormap
    current_colormap = colormap

def getFramesGenerator():
    """ Генератор фреймов для вывода в веб-страницу"""
    while True:
        success, frame = camera.read()  # Получаем фрейм с камеры
        if success:
            # уменьшаем разрешение кадров
            frame = cv2.resize(frame, (1080, 720), interpolation=cv2.INTER_AREA)

            if current_colormap:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.applyColorMap(gray_frame, current_colormap)


            height, width = frame.shape[:2]
            cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 2)  # вертикальная линия
            cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 2)  # горизонтальная линия


            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/update_values', methods=['POST'])
def update_values():
    """
    Обработка обновления значений direction и progress
    """
    move_id = request.form['move']
    id_control[move_id][0]()
    arduino.write(control_byte.get_byte().to_bytes(1, byteorder="big"))
    print(
        f"Команда: ({move_id, id_control[move_id][1]})", 
        f"Raspberry: {bin(control_byte.get_byte())}, Arduino: {arduino.read()}"
        )

    return jsonify({'speed': int((control_byte.get_byte() & 0b00011111)/31*100)})


@app.route("/")
def index():
    return render_template('index.html')

            
@app.route('/video_feed')
def video_feed():
    """
    Генерируем и отправляем изображения с камеры
    """
    return Response(getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')