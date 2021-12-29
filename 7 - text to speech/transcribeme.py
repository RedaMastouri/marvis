from gtts import gTTS
import os


#from a file:
fh = open('test.txt', 'r')
myText = fh.read().replace('\n', " ")

# from the keyboard
# myText = input("Type something you want Jarvis to know about (He will try to recognize your style by reading what you will type!! Be careful he is watching you): ")

Language = 'en'

output = gTTS(text=myText, lang=Language, slow=False)

output.save("output.mp3")

# to close the file
fh.close()

os.system("Start output.mp3")