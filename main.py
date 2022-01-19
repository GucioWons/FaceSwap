import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2

root = tk.Tk()

type = None
img = None
gray = None
face_cascade = cv2.CascadeClassifier('face_detector.xml')
imgswap = cv2.imread('assets/mickey.jpg')


def refresh(self):
    self.destroy()
    self.__init__()
    rootSetUp()


def rootSetUp():
    canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
    canvas.pack()

    frame = tk.Frame(root, bg='white')
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    tk.Button(root, text="Select Photo", padx=10, pady=5, fg='white', bg="#263D42", command=showPhotos).pack()
    tk.Button(root, text="Swap", padx=10, pady=5, fg='white', bg="#263D42", command=swapFace).pack()

    bottom = tk.Frame(root)
    bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    #Wybieranie typu pliku
    if type == ".PNG":
        tk.Button(root, text='.PNG', padx=10, pady=5, fg='white', bg="yellow").pack(in_=bottom, side=tk.LEFT)
    else:
        tk.Button(root, text='.PNG', padx=10, pady=5, fg='white', bg="#263D42",
                  command=lambda *args: settype(".PNG")).pack(in_=bottom, side=tk.LEFT)
    if type == ".JPG":
        tk.Button(root, text='.JPG', padx=10, pady=5, fg='white', bg="yellow").pack(in_=bottom, side=tk.LEFT)
    else:
        tk.Button(root, text='.JPG', padx=10, pady=5, fg='white', bg="#263D42",
                  command=lambda *args: settype(".JPG")).pack(in_=bottom, side=tk.LEFT)
    #Wpisywanie nazwy pliku
    entry1 = tk.Entry(root, width=20)
    entry1.pack(in_=bottom, side=tk.LEFT)
    tk.Button(root, text='SAVE', padx=10, pady=5, fg='white', bg="#263D42",
              command=lambda *args: save(entry1.get())).pack(in_=bottom, side=tk.LEFT)
    #Jeśli plik został wczytany, wyświetl
    if img is not None:
        b, g, r = cv2.split(img)
        imgDisplay = cv2.merge((r, g, b))
        im = Image.fromarray(imgDisplay)
        imgtk = ImageTk.PhotoImage(image=im)
        label = tk.Label(frame, image=imgtk)
        label.pack()

    root.mainloop()

#zmiana typu pliku
def settype(settype):
    global type
    type = settype
    refresh(root)

#wyświetlenie zdjęć
def showPhotos():
    filename = filedialog.askopenfilename(initialdir='/assets/', title="Select photo", filetypes=[
        ("image", ".png"),
        ("image", ".jpg"),
    ])
    global img
    img = cv2.imread(filename, -1)
    cv2.imshow("Wojtek", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    refresh(root)

#zamiana twarzy
def swapFace():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if faces is not None:
        for (x, y, w, h) in faces:
            resized = cv2.resize(imgswap, (w, h))
            img[y:y + h, x:x + w] = resized
        cv2.imshow("Wojtek", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    refresh(root)

#zapisywanie
def save(title):
    if type == ".PNG":
        cv2.imwrite("%s.PNG" % title, img)
    elif type == ".JPG":
        cv2.imwrite("%s.JPG" % title, img)


rootSetUp()
