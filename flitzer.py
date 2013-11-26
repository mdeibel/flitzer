#!/usr/bin/env python
#The above line specifies to the Unix that the file is a python script 

# Alison Polton-Simon and Max Deibel
# Final Project, CS 73
# Dartmouth College

#Import Necessary Libraries
import nltk
import random
import Tkinter as tk
from PIL import ImageTk, Image
import telnetlib
import smtplib
from email.mime.text import MIMEText

class application:
    
    #Initialize the flitz interface 
    def __init__(self,window):
        #Create and anchor background image
        self.bg = ImageTk.PhotoImage(file= "Red_Heart2.gif") 
        w = self.bg.width() 
        h = self.bg.height() 
        canvas = tk.Canvas(width = w, height = h, bg = 'red')
        canvas.pack(expand = tk.YES, fill = tk.BOTH)
        bg = canvas.create_image(0,0,image=self.bg, anchor="nw")    
        
        #Create title for program
        self.title = tk.Label(window, text="Welcome to the flitzer!")
        flitz_title = canvas.create_window(w/2, h/2 - 120, window = self.title)
       
       	#Create line for name entering
        self.recip_entrybox = tk.Entry(window, cursor = "heart")
        recip_entrywindow = canvas.create_window(w/2, h/2-70, window = self.recip_entrybox)
        self.recip_entrybox.insert(0,"Enter name here")
        
        #Create output area
        self.flitz_area = tk.Text(window, cursor = "heart", width = 50, height = 6)
        flitz_window = canvas.create_window(w/2, h/2+10, window = self.flitz_area)
        
        #Flitz generate button
        self.flitz_generate_button = tk.Button(window, text="Flitz", command=self.make_flitz, cursor = "heart")
       	flitz_button_window = canvas.create_window(w/2, h/2+90, window = self.flitz_generate_button)
       	
       	#Send message button
       	self.flitz_send_button = tk.Button(window, text="Send", command = lambda: self.send_screen(window, canvas), cursor = "heart")
       	send_button = canvas.create_window(w/2, h/2+170, window = self.flitz_send_button)
       	
       	#Flitzier checkbox
       	self.extra = tk.IntVar()
       	self.flitz_checkbox = tk.Checkbutton(window, text="More flitzy", variable = self.extra, cursor = "heart")
       	extra_flitz_window = canvas.create_window(w/2, h/2+130, window = self.flitz_checkbox)
    
    #Function to reset window after flitz is sent   
    def reset(self,window, canvas):
    	 w = self.bg.width() 
    	 h = self.bg.height()        
       
       #Recreate line for name entering
    	 self.recip_entrybox.delete(0,tk.END)
    	 self.recip_entrybox.insert(0,"Enter name here")
    	 
    	 #Reset output area
    	 self.flitz_area.delete(1.0,tk.END)
    	 
    	 #Send message
    	 self.flitz_send_button = tk.Button(window, text="Send", command = lambda: self.send_screen(window, canvas), cursor = "heart")
    	 send_button = canvas.create_window(w/2, h/2+170, window = self.flitz_send_button)
    	 
    	 #Recreate flitzier checkbox
    	 self.extra = tk.IntVar()
    	 self.flitz_checkbox = tk.Checkbutton(window, text="More flitzy", variable = self.extra, cursor = "heart")
    	 extra_flitz_window = canvas.create_window(w/2, h/2+130, window = self.flitz_checkbox)
    	 
    	 #Recreate flitz button
    	 self.flitz_generate_button = tk.Button(window, text="Flitz", command=self.make_flitz, cursor = "heart")
    	 flitz_button_window = canvas.create_window(w/2, h/2+90, window = self.flitz_generate_button)
    	 
    	 #Destroy unneeded entry boxes and buttons
    	 self.senderentrybox.destroy()
    	 self.flitz_mail.destroy()

    
    #Function to process input and generate message
    def make_flitz(self):
    
    	#Allow for name-less/non-custom messages
    	if (len(self.recip_entrybox.get().strip()) == 0 
    		or self.recip_entrybox.get().strip() == 'Enter name here'):
    		new_flitz = flitz("", self.extra.get())
    	#Generate flitz
    	else:
    		new_flitz = flitz(self.recip_entrybox.get(), self.extra.get())  	
    	#Display generated flitz
    	self.flitz_area.delete(1.0,tk.END)
    	self.flitz_area.insert(tk.END, new_flitz)
    
    #Function for actually sending flitzes	
    def blitz_flitz(self, window, canvas):
    	#Set message parameters
    	msg = MIMEText(self.flitz_area.get(1.0, tk.END))
    	msg['Subject'] = 'hi ;-)' 
    	msg['To'] = self.recip_entrybox.get()
    	#Send message over SMTP
    	s = smtplib.SMTP('mailhub3.dartmouth.edu')
    	s.sendmail(self.senderentrybox.get(), ["asps@dartmouth.edu", "mnd@dartmouth.edu", msg['To'], self.senderentrybox.get()], msg.as_string())
    	#Quit mailhub and reset user interface to send another flitz
    	s.quit()
    	self.reset(window, canvas)
    	
    #Function to display message-sending interface	
    def send_screen(self, window, canvas):
    	#Delete unneeded components	
    	w = self.bg.width() 
    	h = self.bg.height() 
    	self.flitz_checkbox.destroy()
    	self.flitz_generate_button.destroy()
    	
    	#Update entry points
    	self.recip_entrybox.delete(0,tk.END)
    	self.recip_entrybox.insert(0,"Enter recipient email here")
    	
    	#Add spot to include sender email
    	self.senderentrybox = tk.Entry(window, cursor = "heart")
    	sender_window = canvas.create_window(w/2, h/2+110, window = self.senderentrybox)
    	self.senderentrybox.insert(0,"Enter sender email here")
    	
    	#Add actually send        	
    	self.flitz_mail = tk.Button(window, text="Mail me ;)", command = lambda: self.blitz_flitz(window, canvas), cursor = "heart")
    	send_button = canvas.create_window(w/2, h/2+170, window = self.flitz_mail)

# Generates a random sentence using ngrams
# Modified from code in the NLTK
def generateSentence(totalSentences, bigramModel, trigramModel, context=()):
	text = list(context)
	numSentences = 0 # Current number of sentences generated
	currModel = trigramModel # Initially generate from trigrams
	
	# Loop until we've generated the right number of sentences
	while (numSentences < totalSentences):
		''' 
		***We attempted some sort of bigram/trigram interpolation, but it resulted
				in noticeably less coherent sentences (likely due to our relatively 
				small corpus). We've included the relavant code here***
		pickGram = random.randint(1,100)
		# 5% chance to switch to bigram
		if (currModel == trigramModel):
			if (pickGram >= 95):
				currModel = bigramModel
		# 95% chance to switch back to trigram
		elif (currModel == bigramModel):
			if (pickGram <= 95):
				currModel = trigramModel
		'''
		# Generate next work based on current ngram model
		next = currModel._generate_one(text)
		currModel = trigramModel # Make sure our default is trigram
		
		# See if we ended a sentence
		if (next == '.' or next == '!' or next == '?' or next == '...'):
			numSentences += 1
			currModel = bigramModel # Use bigram model for the next word if at 
															# sentence end (so we don't follow along any one
															# flitz in our corpus for too long)			
		# Add word to text
		text.append(next)
	
	# Return generated sentence(s)
	return text
	
# Function to "glue" the sentence back together.
# Removes whitespace appropriately.
def fixPunctuation(sentenceList, extra):
	sentence = "" # We will concatenate onto this
	insertSpace = False # Keeps track of whether or not to add a space first
	
	# Iterate through the list, concatenating entries appropriately
	for word in sentenceList:  
		if ((word.isalnum() or word[0] == ":" or word[0] == ";") and insertSpace):
			sentence += " " + word
		elif ((word.isalnum() or word[0] == ":" or word[0] == ";") and not insertSpace):
			sentence += word
			insertSpace = True
		elif (word == "'"): # Apostrophe, so we don't want spaces
			sentence += word
			insertSpace = False
		elif (word == "-"): # Dash, so we want space on both sides
			sentence += " " + word
			if (not insertSpace):
				insertSpace = True
		else: # End of sentence or comma, so we want no space
			# Occasionally replace end of sentence with ';)' if extra was checked
			wink = random.randint(1,4)
			if (wink == 1 and word != ',' and extra == 1):
				sentence += " ;)"
			else:
				sentence += word
			insertSpace = True # Next word should be seperated from this punctuation
	
	return sentence
	
# Function to make the flitz more "flitzy"
# Currently adds extra letters to ends of some words
def flitzify(sentenceList):
	index = 0
	newSentenceList = list()

	# Iterate through, flitzify some words
	for word in sentenceList:  
		addLetters = random.randint(1,5) # Will determine if we add extra letters
		if (word[-1] == 'y'): # Only add extra letters if the word ends in 'y'
			if (addLetters == 1):
				sentenceList[index] = word + word[-1] + word[-1] + word[-1]
		else:
			sentenceList[index] = word
		index += 1
		
#Flitz function
def flitz(name, extra):	
	# Get flitzes into a tokenized list
	flitzes = open('flitzes.txt','rU')
	raw = flitzes.read() # Convert text file to string
	raw = raw.lower() # Lowercase all characters
	tokens = nltk.wordpunct_tokenize(raw) # Split string into buckets of words
																				# and punctuation
	
	# Create bigram and trigram models, using the NLTK toolkit
	bigramModel = nltk.NgramModel(2, tokens)
	trigramModel = nltk.NgramModel(3, tokens)
	
	# Decide on which starting context to use.
	# By using end punctuation as a starting context, we can start at a random
	# start of sentence in our corpus.
	option = random.randint(1,4)
	if (option == 1):
		startContext = "."
	elif (option == 2):
		startContext = "!"
	elif (option == 3):
		startContext = "?"
	else:
		startContext = "..."
	
	# Generate sentence in list form
	sentenceList = generateSentence(3, bigramModel, trigramModel, startContext)
	
	# Iterate to find where words start, then strip punctuation on left side.
	# The left side is padded with 1-3 punctuation characters due to how we enter
	# a starting context.
	i = 0
	while (not sentenceList[i].isalnum()):
		i += 1
	sentenceList = sentenceList[i:]
	
	#Personalize flitz
	sentenceList.insert(0, 'hey')
	sentenceList.insert(1, name)
	sentenceList.insert(2,';)')
	
	# Flitzify
	if (extra == 1):
		flitzify(sentenceList)
	
	# Concatenate properly
	sentence = fixPunctuation(sentenceList, extra)
	
	return sentence

root=tk.Tk()
myapp = application(root)
root.mainloop()
