from google.cloud import speech
import pyttsx3
import pyaudio
import wave
import pocketsphinx
import requests
import speech_recognition as sr
import pytesseract


class Deaf_healper():
    def __init(self,choice,audio,text,image):
        self.choice=choice
        self.audio=audio
        self.image=image
        self.text=text

    def input_datas(self):
        choice=input("enter your operation 1, speech to text \n 2, text to speech \n 3. ocr extraction")
        audio_user_input=input("please inter your audio for process:")
        text_user_input=input("enter your text to process: ")
        image_user_input=input("enter your image for processing: ")
        if choice == "1":
            print(audio_user_input)
        elif choice == "2":
            print(text_user_input)
        elif choice == "3":
            print(image_user_input)
        else:
            print("you take a wrong choice")

    def File_reader(self,file_name):
        super().__init__(self)
        audio_file=pyaudio.PyAudio()
        file_name=input("enter your file pathways:  ")

        chunk=1024
        format=pyaudio.paInt32
        channels=1
        quitrate=44100
        record_seconds=4*3600
        wave_output=file_name

        stream=audio_file.open(format=FORMAT,channels=CHANNELS,
                               rate=RATE,frames_per_buffer=CHUNK)
        PRINT("RECORDING,,,,,,,,,")
        frames=[]
        for i in range(0,int(RATE/CHUNK*record_seconds)):
            DATA=stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()

        audio_file.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_file.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"Audio saved as {file_name}")

    def speech_to_text():
        super().__init__(self)
        url="https://iamcredentials.googleapis.com"
        respon=requests.get(url)


        if respon.server_code == 200:
            print("your are succefully connected with google!!!!")
            speechoff=speech.SpeechClient()
            audio=speech.RecognitionAudio(uri="C:\\Users\\Programming\\Downloads\\Seasonal Love - Ali Gatie.m4a")
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_herz=16000,
                language_code="en-US"
            )

            responce=client.recognize(config=config,audio=audio)
            for result in responce.results:
                print("trancript: {}.". format(result.alternative[0].trancript))

        else:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            recognizer.recognize_google = recognizer.recognize_sphinx 
            audio_file = "path/to/your/audio.wav"  

            with sr.AudioFile(audio_file) as source:
                print("Listening to the audio file...")
                audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_sphinx(audio_data)
                print("Recognized text: ", text)
            except sr.UnknownValueError:
                print("Pocketsphinx could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Pocketsphinx service; {e}")

    def text_to_speech(self):
        super().__init__(self)
        recognize = sr.Recognizer()
        engine=pyttsx3.init()
        engine.say()
        engine.runAndWait()
        while(1):    
            try:
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio2 = r.listen(source2)
                    MyText = r.recognize_google(audio2)
                    MyText = MyText.lower()

                    print(&quot;Did you say &quot;,MyText)
                    SpeakText(MyText)
                    
            except sr.RequestError as e:
                print(&quot;Could not request results; {0}&quot;.format(e))
                
            except sr.UnknownValueError:
                print(&quot;unknown error occurred&quot;)

    def image_extracter(self):
        image_path=input("enter image path to your image:  ")
        if True:
            text = pytesseract.image_to_string('image_path')
            speech_to_text(text)


if __name__=="__main__":
    Deaf_healper()






        

