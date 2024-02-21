from vosk import Model, KaldiRecognizer
import wave

# Укажите путь к вашей модели

model_path = 'vosk-model-ru'

model = Model(model_path)

def transcribe_audio(file_path):
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
    result = rec.FinalResult()
    return result

audio_file_path = '1.wav'  # Замените на путь к вашему аудиофайлу
text = transcribe_audio(audio_file_path)
# print(text)

with open("1.txt", "w") as text_file:
    text_file.write(text)
    print("Текст успешно сохранен в файл 'transcribed_text.txt'.")
