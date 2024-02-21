import sys
from PySide6 import QtCore, QtWidgets, QtGui

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os  # Добавляем импорт модуля os

from vosk import Model, KaldiRecognizer
import wave



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('mp4-wav-txt')
        self.setGeometry(100, 100, 400, 200)

        layout = QtWidgets.QVBoxLayout()

        self.path_mp4 = ''
        self.path_wav = ''
        self.path_txt = ''

        # mp4 1
        self.file_path_label1 = QtWidgets.QLabel('mp4 file path: ')
        layout.addWidget(self.file_path_label1)

        file_path_button1 = QtWidgets.QPushButton('get file mp4')
        file_path_button1.clicked.connect(self.file_path1)
        layout.addWidget(file_path_button1)

        # wav 2
        self.file_path_label2 = QtWidgets.QLabel('wav file path: ')
        layout.addWidget(self.file_path_label2)

        file_path_button2 = QtWidgets.QPushButton('name file and dir wav: ')
        file_path_button2.clicked.connect(self.file_path2)
        layout.addWidget(file_path_button2)

        # txt 3
        self.file_path_label3 = QtWidgets.QLabel('txt file path: ')
        layout.addWidget(self.file_path_label3)

        file_path_button3 = QtWidgets.QPushButton('name file and dir txt: ')
        file_path_button3.clicked.connect(self.file_path3)
        layout.addWidget(file_path_button3)


        #button mp4-wav
        self.file_path_label4 = QtWidgets.QLabel('mp4 in wav: NOT')
        layout.addWidget(self.file_path_label4)

        file_path_button4 = QtWidgets.QPushButton('Button mp4 in wav')
        file_path_button4.clicked.connect(self.extract_audio)
        layout.addWidget(file_path_button4)


        #button wav-txt
        self.file_path_label5 = QtWidgets.QLabel('Button wav in txt: NOT')
        layout.addWidget(self.file_path_label5)

        file_path_button5 = QtWidgets.QPushButton('wav in txt')
        file_path_button5.clicked.connect(self.transcribe_audio)
        layout.addWidget(file_path_button5)

        #button refresh
        file_path_button6 = QtWidgets.QPushButton('wav in txt')
        file_path_button6.clicked.connect(self.refresh)
        layout.addWidget(file_path_button6)

        self.setLayout(layout)


    def file_path1(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose file mp4', '/')
        self.file_path_label1.setText(f'Selected mp4 Path: {file_path}')
        self.path_mp4 = file_path

    def file_path2(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose file and dir wav', '/')
        self.file_path_label2.setText(f'Selected wav Path: {file_path}')
        self.path_wav = file_path

    def file_path3(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose file and dir txt', '/')
        self.file_path_label3.setText(f'Selected txt Path: {file_path}')
        self.path_txt = file_path  
    
    def extract_audio(self):
        """
        Извлекает аудиодорожку из видеофайла, преобразует ее в моно и устанавливает
        частоту дискретизации 16kHz, затем сохраняет в формате WAV.

        Args:
        - video_filepath: Путь к исходному видеофайлу.
        - output_audio_filepath: Путь к выходному аудиофайлу в формате WAV.
        """
        video_filepath, output_audio_filepath = self.path_mp4[0], self.path_wav[0]
        print(video_filepath, '\n', output_audio_filepath)
        # Загружаем видео и извлекаем аудио как временный файл
        video_clip = VideoFileClip(video_filepath)
        temp_audio_filepath = "temp_audio.mp3"  # Используем временный файл для аудио
        video_clip.audio.write_audiofile(temp_audio_filepath)

        # Используем pydub для конвертации аудио в моно и установки нужной частоты дискретизации
        audio = AudioSegment.from_file(temp_audio_filepath)
        audio = audio.set_channels(1)  # Преобразуем в моно
        audio = audio.set_frame_rate(16000)  # Устанавливаем частоту дискретизации 16kHz

        # Сохраняем обработанное аудио в WAV
        audio.export(output_audio_filepath, format="wav", parameters=["-acodec", "pcm_s16le"])

        # Удаляем временный аудиофайл
        os.remove(temp_audio_filepath)
        self.file_path_label4.setText('mp4 in wav: YES')

    def transcribe_audio(self):

        file_path, file_path2 = self.path_wav[0], self.path_txt[0]

        model_path = 'vosk-model-ru'
        model = Model(model_path)

        # Откройте аудиофайл с помощью wave
        wf = wave.open(file_path, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)  # Чтобы получать слова вместо простых результатов

        # Чтение данных и распознавание
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print("Процесс распознавания...")  # Логирование процесса

        # Получение итогового результата
        text = rec.FinalResult()

        with open(file_path2, "w") as text_file:
            start_index = text.find("\"text\" : \"")
            text_file.write(text[start_index : ])
            print("Текст успешно сохранен в файл 'transcribed_text.txt'.")
            
        self.file_path_label5.setText('wav in txt: YES')


    def refresh(self):
        self.file_path_label4.setText('mp4 in wav: NO')
        self.file_path_label5.setText('wav in txt: NO')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())
