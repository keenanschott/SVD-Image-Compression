# necessary imports
import sys
import numpy as np
from PIL import ImageTk, Image
import tkinter as tk
from tkinter.filedialog import askopenfilename

energies = np.empty(0, dtype=float) # declare energies array, will store RGB energies

def close():
    window.destroy()
    sys.exit(0)

def get_svc(color_matrix):
    return len(np.linalg.svd(color_matrix, full_matrices = False)[1]) # how many singular values there are for the given image

def svd_approx(color_matrix, k):
    u, s, vt = np.linalg.svd(color_matrix, full_matrices = False) # SVD
    calculate_energy(s, k, np.linalg.matrix_rank(color_matrix)) # calculating energies as we go
    s = np.diag(s)
    approx = u[:,:k] @ s[0:k,:k] @ vt[:k,:] # the SVD approximation given k singular values
    return approx

def calculate_energy(s, k, rank):
    global energies
    energies = np.append(energies, round((sum(np.square(s[:k])) / sum(np.square(s[:rank]))) * 100, 2))  # energy calculation

tk.Tk().withdraw()
filename = askopenfilename(filetypes=(("PNG Files", "*.png"),)) # let user pick file

image = Image.open(filename)
npdata = np.array(image, dtype=int) # image data
image.close()

width = len(npdata[0])
height = len(npdata)
shape = (height, width)
shape_rgb = (height, width, 3) # final image shape

new_image = np.zeros(shape_rgb, dtype=int)
red = np.zeros(shape, dtype=int)
green = np.zeros(shape, dtype=int)
blue = np.zeros(shape, dtype=int)

for i in range(len(npdata)):
    for j in range(len(npdata[i])):
        red[i][j] = npdata[i][j][0]
        green[i][j] = npdata[i][j][1]
        blue[i][j] = npdata[i][j][2]

singular_value_count = get_svc(red)

# input loop
print(f"Please provide a valid integer input for the quantity of singular values between 1 and {singular_value_count}.")
while True:
    singular_value_choice = input("Quantity: ")
    try:
        singular_value_choice = int(singular_value_choice)
    except:
        print("That's not an integer; try again.")
        continue
    if singular_value_choice >= 1 and singular_value_choice <= singular_value_count:
        break
    else:
        print("That's not within the given range for singular values; try again.")

uncompressed_size = width * height
compressed_size = (height * singular_value_choice) + singular_value_choice + (singular_value_choice * width)

red_approx = svd_approx(red, singular_value_choice) # approximations
green_approx = svd_approx(green, singular_value_choice)
blue_approx = svd_approx(blue, singular_value_choice)

# write to new image
for i in range(height):
    for j in range(width):
        new_image[i][j][0] = int(red_approx[i][j])
        new_image[i][j][1] = int(green_approx[i][j])
        new_image[i][j][2] = int(blue_approx[i][j])

final_image = Image.new(mode = "RGB", size = shape[::-1])
pixel = final_image.load()

y = 0
for i in range(len(new_image)): 
    x = 0
    for rgb in new_image[i]:
        pixel[x, y] = tuple(rgb)
        x += 1
    y += 1

# write to GUI
window = tk.Tk()
window.resizable(False, False)
window.attributes("-topmost", True)
window.lift()
window.title("SVD Image Compression")
window.protocol("WM_DELETE_WINDOW", close)

# size window
window_width = image.width 
window_height = (image.height // 2) + 50
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# text
text = tk.Label(window, text=f"Compression Ratio: {uncompressed_size} / {compressed_size} = {round(uncompressed_size / compressed_size, 2)}\nR Energy: {energies[0]}%, G Energy: {energies[1]}%, B Energy: {energies[2]}%", font=("Helvetica", 16))
text.pack(side=tk.BOTTOM, expand=True)

# original image
img = Image.open(filename)
img = img.resize((window_width // 2, window_height - 50)) 
label = ImageTk.PhotoImage(image = img, master=window)  
tk.Label(window, image=label).pack(side=tk.RIGHT, expand=True)

# new image
final_image = final_image.resize((window_width // 2, window_height - 50))
label2 = ImageTk.PhotoImage(image = final_image, master=window)     
tk.Label(window, image=label2).pack(side=tk.LEFT, expand=True)

# run until closure
window.mainloop()