#Chris Chueh

import pygame
from tkinter import *
from tkinter import messagebox


class DoublyLinkedListNode:
    def __init__(self, title, artist, file, album, myNext, myPrevious):
        #Construct a new Linked List Node
        self.title = title
        self.artist = artist
        self.file = file
        self.album = album
        self.next = myNext
        self.previous = myPrevious
        return
        

class DoublyLinkedList:
    def __init__(self):
        #Construct a new LinkedList. The first node and last node are the same. Size is 0        self.firstNode = LinkedListNode(None, None)
        self.firstNode = DoublyLinkedListNode(None, None, None, None, None, None)
        self.lastNode = self.firstNode
        self.size = 0
        return

    def addToFront(self, title, artist, file, album):
        #Add a node to the list
        node = DoublyLinkedListNode(title, artist, file, album, None, None)
        node.title = title;
        node.artist = artist;
        node.file = file;
        node.album = album;
        if self.firstNode.title == None:
            self.firstNode = node
            self.lastNode = node
        else:
            self.firstNode.previous = node
            node.next = self.firstNode
            self.firstNode = node

        self.size += 1
        
    def addToRear(self, title, artist, file, album):
        #Add a node to the list
        node = DoublyLinkedListNode(title, artist, file, album, None, None)
        node.title = title;
        node.artist = artist;
        node.file = file;
        node.album = album;
        if self.firstNode.title == None:
            self.firstNode = node
            self.lastNode = node
        else:
            self.lastNode.next = node
            node.previous = self.lastNode
            self.lastNode = node

        self.size += 1

        return

    def removeFromFront(self):
        #Remove a node from the front of the list

        if self.size == 0:
            frontData = None
        else:
            currentNode = self.firstNode
            frontData = currentNode.title

            # This is the case where we have only one node in the list
            if currentNode.next == None:
                self.firstNode = DoublyLinkedListNode(None, None, None, None, None, None)
                self.lastNode = self.firstNode
                self.size = self.size - 1
            else:

                # Here there are more than one nodes in the list
                nextNode = currentNode.next
                nextNode.previous = None
                self.firstNode = nextNode
                self.size = self.size - 1

        return frontData

    def removeFromRear(self):
        #Remove a node from the rear of the list

        if self.size == 0:
            rearData = None
        else:
            currentNode = self.lastNode
            rearData = currentNode.title

            # This is the case where we have only one node in the list
            if currentNode.previous == None:
                self.firstNode = DoublyLinkedListNode(None, None, None, None, None, None)
                self.lastNode = self.firstNode
                self.size = self.size - 1
            else:

                # Here there are more than one nodes in the list
                previousNode = currentNode.previous
                previousNode.next = None
                self.lastNode = previousNode
                self.size = self.size - 1

        return rearData 

# Plays the loaded music.
def playsong():
    pygame.mixer.music.play()

# Pauses the loaded music, or plays the music if paused.
def pausesong():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

# Stops the loaded music. If the user plays it again, it starts from the beginning.
def stopsong():
    pygame.mixer.music.stop()

# Loads the next song in the Doubly Linked List.
def nextsong():
    global currentsong
    if currentsong.next != None:
        currentsong = currentsong.next
    else:
        currentsong = songslist.firstNode
    update()
    
# Loads the previous song in the Doubly Linked List.
def previoussong():
    global currentsong
    if currentsong.previous != None:
        currentsong = currentsong.previous
    else:
        currentsong = songslist.lastNode
    update()

# Sets up entry boxes for adding a new song to the database.    
def addsong():
    a.delete(0, END)
    b.delete(0, END)
    c.delete(0, END)
    d.delete(0, END)
    frame.grid(row = 2, column = 1)
    
# Adds a song based on what the user entered.
def addfinal():
    global a, b, c, d
    songslist.addToRear(a.get(), b.get(), c.get(), d.get())
    frame.grid_forget()

# Removes the current song from the database.    
def deletesong():
    global currentsong
    if currentsong == songslist.firstNode:
        songslist.removeFromFront()
        currentsong = songslist.firstNode
    elif currentsong == songslist.lastNode:
        songslist.removeFromRear()
        currentsong = songslist.lastNode
    else:
        currentsong = currentsong.next
        currentsong.previous.previous.next = currentsong
        currentsong.previous = currentsong.previous.previous
    update()


# Clears search entry box for user input.    
def search():
    searchtext.delete(0, END)
    frame2.grid(row = 3, column = 1)

# Looks for information based on user input.    
def find():
    count = 0
    global currentsong
    temp = currentsong
    textresults.insert(END, 'Results: \n\n')
    stext = searchtext.get()
    for i in range(songslist.size):
        if stext.lower() in currentsong.title.lower() or stext.lower() in currentsong.artist.lower() or stext.lower() in currentsong.album.lower():
            string = 'Title: ' + currentsong.title + '\nAlbum: ' + currentsong.album + 'Artist: ' + currentsong.artist + '\n\n'
            textresults.insert(END, string)
            count += 1
        if currentsong == songslist.lastNode:
            currentsong = songslist.firstNode
        else:
            currentsong = currentsong.next
    frame2.grid_forget()
    if count > 0:
        frame3.grid(row = 4, column = 1)
        
    else:
        messagebox.showinfo('Sorry!', 'No results were found!')
        textresults.delete(1.0, END)
    currentsong = temp
    update()

# Removes search results from user view.
def donewithsearch():
    frame3.grid_forget()
    textresults.delete(1.0, END)
    return

# Updates title, artist, and album to the current song.    
def update():
    global currentsong
    if currentsong.title != None and currentsong.title != '':
        pygame.mixer.music.load("songs/" + currentsong.file)
        titlelabel['text'] = currentsong.title
        artistlabel['text'] = currentsong.artist
        albumlabel['text'] = currentsong.album
    else:
        titlelabel['text'] = ''
        artistlabel['text'] = ''
        albumlabel['text'] = ''

# Imports songs from the database to the list, and initializes the music player.        
paused = False
songlist = open('songlist.txt', 'r')
songs = songlist.readlines()
songslist = DoublyLinkedList()
for i in range(len(songs)):
    songgroup = (songs[i].split(','))
    songslist.addToRear(songgroup[0], songgroup[1], songgroup[2], songgroup[3])   
currentsong = songslist.firstNode
pygame.mixer.init()
pygame.mixer.music.load("songs/Astronaut.mp3")

# Initializes the GUI.
root =Tk()
frame1 = Frame(root, bg = 'blue')
frame1.grid(row = 1, column = 1)
root.title('Pytunes')


# Creates labels for the current song information.
Label(frame1, text = 'Title:', height = 2, fg = 'white', bg = 'blue').grid(row = 1, column = 1)
titlelabel = Label(frame1, text = currentsong.title, height = 2, width = 20, fg = 'white', bg = 'blue')
titlelabel.grid(row = 1, column = 2, columnspan = 2)
Label(frame1, text = 'Artist:', height = 2, fg = 'white', bg = 'blue').grid(row = 2, column = 1)
artistlabel = Label(frame1, text = currentsong.artist, height = 2, width = 20, fg = 'white', bg = 'blue')
artistlabel.grid(row = 2, column = 2, columnspan = 2)
Label(frame1, text = 'Album:', height = 2, fg = 'white', bg = 'blue').grid(row = 3, column = 1)
albumlabel = Label(frame1, text = currentsong.album, height = 2, width = 20, fg = 'white', bg = 'blue')
albumlabel.grid(row = 3, column = 2, columnspan = 2)

# Creates buttons for user manipulation of the current song.
Button(frame1, text='Play', command = playsong, width = 15, fg = 'white', bg = 'blue').grid(row = 4, column = 1, sticky = W)
Button(frame1, text='||', command = pausesong, height = 3, width = 20, fg = 'white', bg = 'blue').grid(row = 4, column = 2, columnspan = 2, rowspan = 2)
Button(frame1, text='Stop', command = stopsong, width = 15, fg = 'white', bg = 'blue').grid(row = 4, column = 4, sticky = E)
Button(frame1, text='>>', command = nextsong, width = 15, fg = 'white', bg = 'blue').grid(row = 5, column = 4, sticky = E)
Button(frame1, text='<<', command = previoussong, width = 15, fg = 'white', bg = 'blue').grid(row = 5, column = 1, sticky = W)

# Creates buttons to allow users to edit songs in the database.
Button(frame1, text='Add', command = addsong, width = 15, fg = 'white', bg = 'blue').grid(row = 6, column = 1, sticky = W)
Button(frame1, text='Delete', command = deletesong, width = 15, fg = 'white', bg = 'blue').grid(row = 6, column = 4,  sticky = E)

# Creates buttons for finding songs.
Button(frame1, text='Search', command = search, width = 20, fg = 'white', bg = 'blue').grid(row = 6, column = 2, columnspan = 2)


# Creates entries for adding songs.
frame = Frame(root, bg = 'blue')
Label(frame, text = 'Song Title:', fg = 'white', bg = 'blue').grid(row = 1, column = 1)
a =Entry(frame, fg = 'white', bg = 'blue', width = 50)
a.grid(row = 1, column = 2)
Label(frame, text = 'Song Artist:', fg = 'white', bg = 'blue').grid(row = 2, column = 1)
b = Entry(frame, fg = 'white', bg = 'blue', width = 50)
b.grid(row = 2, column = 2)
Label(frame, text = 'Song File:', fg = 'white', bg = 'blue').grid(row = 3, column = 1)
c = Entry(frame, fg = 'white', bg = 'blue', width = 50)
c.grid(row = 3, column = 2)
Label(frame, text = 'Song Album:', fg = 'white', bg = 'blue').grid(row = 4, column = 1)
d = Entry(frame, fg = 'white', bg = 'blue', width = 50)
d.grid(row = 4, column = 2)
Button(frame, text = 'Done', command = addfinal, fg = 'white', bg = 'blue').grid(row = 5, column = 1, columnspan = 2)

# Creates entries for searching for songs.
frame2 = Frame(root, bg = 'white')
searchtext = Entry(frame2, fg = 'white', bg = 'blue', width = 54)
searchtext.grid(row = 1, column = 1)
Button(frame2, text = 'Go', command = find, fg = 'white', bg = 'blue', width = 6).grid(row = 1, column = 2)

# Creates search results.
frame3 = Frame(root, bg = 'white')
yscrollbar = Scrollbar(frame3)
yscrollbar.grid(row = 0, column = 1, sticky = N+S)
textresults = Text(frame3, height = 5, width = 44, wrap = WORD, fg = 'white', bg = 'blue', yscrollcommand=yscrollbar.set)
textresults.grid(row = 0, column = 0, sticky = N+S+E+W)
yscrollbar.config(command = textresults.yview)
Button(frame3, text = 'Ok', command = donewithsearch, fg = 'white', bg = 'blue').grid(row = 2, column = 1)

# Loops the GUI.
root.mainloop()

