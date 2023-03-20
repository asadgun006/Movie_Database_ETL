import tkinter as tk
import pymongo
from PIL import ImageTk, Image
from RangeSlider.RangeSlider import RangeSliderH as rs
from RangeSlider.RangeSlider import RangeSliderH as rs2


client = pymongo.MongoClient("mongodb+srv://agundra001:Final_Project_1@pythonproject.v3r1sg2.mongodb.net/?retryWrites=true&w=majority")
disneyAndMarvelDatabase = client['DisneyAndMarvelDatabase']
disney_collection = disneyAndMarvelDatabase['disney_movies']
marvel_collection = disneyAndMarvelDatabase['marvel_movies']

window = tk.Tk()
#

# HEIGHT = 400
# WIDTH = 800
# canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
# canvas.pack()

frame = tk.Frame(window)
frame.place(relheight=1, relwidth=1)
image = ImageTk.PhotoImage(Image.open("Disney-Marvel-logo.jpg"))
imageWidth = image.width()
imageHeight = image.height()
window.geometry(f"{imageWidth}x{imageHeight}")

imageLabel = tk.Label(frame, image=image)

imageLabel.place(relwidth=1, relheight=1)
bgColor = "#ffffff"
mainLabel = tk.Label(frame, text="Welcome to Movie World", font=("Chiller", 22), bg=bgColor)
mainLabel.place(relx=0.5, y=0, anchor="n")
secondLabel = tk.Label(frame, text="A searchable database for Marvel Cinematic Universe movies/tv shows and Disney movies",
                       font=("Chiller", 18), bg=bgColor)
secondLabel.place(relx=0.5, y=30, anchor="n")
messageLabel = tk.Label(frame, text="You can filter by Year and IMDb rating", bg=bgColor,font=("Chiller", 15))
messageLabel.place(relx=0.5, y=60, anchor="n")

disneyCheckBoxVar = tk.IntVar()
disneyCheckBox = tk.Checkbutton(frame, text="Disney", bg="#ffffff", fg="#000000", font=("Chiller", 16), variable=disneyCheckBoxVar, onvalue=1, offvalue=0)
disneyCheckBox.place(relx=0.3, y=100, anchor="n")

marvelCheckBoxVar = tk.IntVar()
marvelCheckBox = tk.Checkbutton(frame, text="Marvel", bg="#ffffff", fg="#ED1D24", font=("Chiller", 16), variable=marvelCheckBoxVar, onvalue=1, offvalue=0)
marvelCheckBox.place(relx=0.7, y=100, anchor="n")

filterLabel = tk.Label(frame, text="Filter", bg="#ffffff", font=("Chiller", 18))
filterLabel.place(relx=0.5, y=150, anchor="n")

yearCheckBoxVar = tk.IntVar()
yearCheckBox = tk.Checkbutton(frame, text="By Year", bg="#ffffff", fg="#000000", font=("Chiller", 15), variable=yearCheckBoxVar, onvalue=1, offvalue=0)
yearCheckBox.place(relx=0.3, y=250, anchor="n")

ratingCheckBoxVar = tk.IntVar()
ratingCheckBox = tk.Checkbutton(frame, text="By IMDb", bg="#ffffff", fg="#ED1D24", font=("Chiller", 15), variable=ratingCheckBoxVar, onvalue=1, offvalue=0)
ratingCheckBox.place(relx=0.7, y=250, anchor="n")

hVarOne = tk.DoubleVar()
hVarTwo = tk.DoubleVar()
sliderOne = rs(frame, [hVarOne, hVarTwo], line_s_color="#000000", min_val=1937, max_val=2022, padX=24, font_size=8, digit_precision='.0f', Height=50)
sliderOne.place(relx=0.28, y=290, anchor="n")

vVarOne = tk.DoubleVar()
vVarTwo = tk.DoubleVar()
sliderTwo = rs(frame, [vVarOne, vVarTwo], line_s_color="#000000", min_val=0, max_val=10, padX=12, font_size=8, digit_precision='.0f', Height=50,Width=280)
sliderTwo.place(relx=0.8, y=290, anchor="n")

getDataButton = tk.Button(frame, text="Show me movies", font=("Chiller", 16), bg="#ffffff")
getDataButton.bind('<Button>', lambda e: newWindow())
getDataButton.place(relx=0.5, rely=1, anchor="s")

def newWindow():

    anotherWindow = tk.Toplevel(window)
    anotherWindow.title('Movie Information')
    anotherWindow.geometry("800x400")
    label = tk.Label(anotherWindow, bg='#80b3ff', text="Your Requested Movies Are Below:", font=("Castellar", 14))
    label.pack(fill="x")
    scrollbarh = tk.Scrollbar(anotherWindow, orient="horizontal")
    scrollbarh.pack(side="bottom", fill="x")
    scrollbarv = tk.Scrollbar(anotherWindow, orient="vertical")
    scrollbarv.pack(side="right", fill="y")
    textWindow = tk.Text(anotherWindow, bg='#cce0ff', yscrollcommand=scrollbarv.set, xscrollcommand=scrollbarh.set, wrap="none", font=("Bahnschrift Light", 14))
    textWindow.pack(expand=True, fill='both')
    # myFile = open("marvel_data_refreshed.json", encoding="utf-8")
    # marvel_file = json.load(myFile)
    # for name in marvel_file:
    #     for key, value in name.items():
    #         textWindow.insert(tk.END, f"{key}: {value}\n")
    #     textWindow.insert(tk.END, "\n")
    if disneyCheckBoxVar.get() & marvelCheckBoxVar.get():
        joinedList = []
        if yearCheckBoxVar.get() & ratingCheckBoxVar.get():
            for name in disney_collection.find({"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                                                "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}},
                                               {'_id': 0}):
                joinedList.append(name)
            for name in marvel_collection.find({"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                                                "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}},
                                               {'_id': 0}):
                joinedList.append(name)
            for name in joinedList:
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif yearCheckBoxVar.get():
            for name in disney_collection.find(
                    {"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]}}, {'_id': 0}):
                joinedList.append(name)
            for name in marvel_collection.find(
                    {"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                     "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                joinedList.append(name)
            for name in joinedList:
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif ratingCheckBoxVar.get():
            for name in disney_collection.find({"IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                joinedList.append(name)
            for name in marvel_collection.find(
                    {"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                     "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                joinedList.append(name)
            for name in joinedList:
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        else:
            textWindow.insert(tk.INSERT, "Please select a filter!")

    elif disneyCheckBoxVar.get():
        if yearCheckBoxVar.get() & ratingCheckBoxVar.get():
            for name in disney_collection.find({"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                                                "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}},
                                               {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif yearCheckBoxVar.get():
            for name in disney_collection.find({"Release Year": {"$gte": sliderOne.getValues()[0],
                                                                 "$lte": sliderOne.getValues()[1]}}, {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif ratingCheckBoxVar.get():
            for name in disney_collection.find({"IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        else:
            textWindow.insert(tk.INSERT, "Please select a filter!")

    elif marvelCheckBoxVar.get():
        if yearCheckBoxVar.get() & ratingCheckBoxVar.get():
            for name in marvel_collection.find(
                    {"Release Year": {"$gte": sliderOne.getValues()[0], "$lte": sliderOne.getValues()[1]},
                     "IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif yearCheckBoxVar.get():
            for name in marvel_collection.find({"Release Year": {"$gte": sliderOne.getValues()[0],
                                                                 "$lte": sliderOne.getValues()[1]}}, {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        elif ratingCheckBoxVar.get():
            for name in marvel_collection.find(
                    {"IMDb": {"$gte": sliderTwo.getValues()[0], "$lte": sliderTwo.getValues()[1]}}, {'_id': 0}):
                for key, value in name.items():
                    if type(value) is list:
                        value = ", ".join(value)
                    textWindow.insert(tk.INSERT, f"{key}: {value}\n")
                textWindow.insert(tk.INSERT, "\n")
        else:
            textWindow.insert(tk.INSERT, "Please select a filter!")
    else:
        textWindow.insert(tk.INSERT, "No movies to display! Please select a database!")

    textWindow.config(state="disabled")
    scrollbarh.config(command=textWindow.xview)
    scrollbarv.config(command=textWindow.yview)



window.wm_resizable(width=False, height=False)
window.mainloop()

