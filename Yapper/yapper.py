import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
	print("Say something:")
	audio = recognizer.listen(source)

while True:
	
	try:
		text = recognizer.recognize_google(audio, language="pl-PL")
		print(f"You said: " + text) # + text.encode('utf-8').decode('utf-8')
	except sr.UnknownValueError:
		print("Google Web Speech API could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Web Speech API; {0}".format(e))
	
	continue