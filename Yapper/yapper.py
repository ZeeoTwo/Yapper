import speech_recognition as sr

recognizer = sr.Recognizer()


while True:
	
	try:
		with sr.Microphone() as source:
			recognizer.adjust_for_ambient_noise(source, duration=0.2)
			audio = recognizer.listen(source);
			text = recognizer.recognize_google(audio, language="pl-PL")
			text.lower();
			print(f"You said: " + text) # + text.encode('utf-8').decode('utf-8')
	except sr.UnknownValueError:
		print("Google Web Speech API could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Web Speech API; {0}".format(e))
	
	continue