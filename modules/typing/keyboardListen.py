import keyboard # used to detect key pressed
from sys import exit as sysExit

# Get keys to not write like MAJ or CTRL from static/keysToIgnore.txt
with open("static/keysToIgnore.txt", "r", encoding="utf8") as file :
    keysToIgnore = [line.strip() for line in file.readlines()] # line.strip() remove '\n' in the line
    del keysToIgnore[0] # Delete first line of keysToIgnore.txt (the commentary)
text = "" # All the char who have pressed by user

def on_key_press(event) :
    '''Event when a key has been pressed, event is an object who have useful info like the name of the key pressed'''
    global keysToIgnore
    global text # We used global variable for use python in-build multi-thread conflit resolver
                # Utilisation d'un variable de niveau global pour ne pas s'embêter
                # avec les conflits de surcharge sur l'écriture de la variable,
                # littéralement, on fait ça pour que si il y a un pb c'est à cause,
                # de python est pas nous ^^.
    char = "" # To escape none called error with keys to ignore
    # Re-writing of char who have pressed for the comfort
    if event.name == "space" :
        char = " "
    elif event.name == "enter" :
        char = "\n"
    elif event.name == "backspace" :
        text = text[:-1]
    # keys to ignore :
    elif event.name in keysToIgnore :
        pass
    else :
        char = event.name
    # Push char in global text
    text += char

def startListening(returnObject=None) :
    '''This is execute when the file is call'''
    listenKeyboard = True # Set to false to kill the listen
    # Setup event for listen keyboard
    keyboard.on_press(on_key_press) # Get async scan for key who was pressed    
    # Output the text
    while listenKeyboard == True :
        old_text = text
        while old_text == text :
            # Await for a change
            # If we want to stop the process in this loop :
            if returnObject.killScript == True :
                sysExit()
        #print(text+"\n") # Print the change in a terminal
        if returnObject != None :
            returnObject.set_var(text)
        if returnObject.killScript == True :
            sysExit()
