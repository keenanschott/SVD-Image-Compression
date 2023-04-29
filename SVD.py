import sys
import numpy as np
from PIL import ImageTk, Image
import tkinter as tk
from tkinter.filedialog import askopenfilename

energies = np.empty(0, dtype=float) # declare energies array, will store RGB energies here

# shut down program
def close():
    window.destroy()
    sys.exit(0)

# get singular value count
def get_svc(color_matrix):
    return len(np.linalg.svd(color_matrix, full_matrices = False)[1]) 

# SVD approximation for each color matrix
def svd_approx(color_matrix, k):
    u, s, vt = np.linalg.svd(color_matrix, full_matrices = False) # SVD
    calculate_energy(s, k, np.linalg.matrix_rank(color_matrix)) # calculate energies as we go
    s = np.diag(s)
    approx = u[:,:k] @ s[0:k,:k] @ vt[:k,:] # the SVD approximation given k singular values
    return approx

# calculate energies
def calculate_energy(s, k, rank):
    global energies
    energies = np.append(energies, round((sum(np.square(s[:k])) / sum(np.square(s[:rank]))) * 100, 2))  # energy calculation

# let user pick PNG file
tk.Tk().withdraw()
filename = askopenfilename(filetypes=(("PNG Files", "*.png"),))

# read image
image = Image.open(filename)
npdata = np.array(image, dtype=int) 
image.close()

# declare variables
width = len(npdata[0])
height = len(npdata)
shape = (height, width)
shape_rgb = (height, width, 3) # final image shape, '3' corresponds to RGB entry

# declare matrices
new_image = np.zeros(shape_rgb, dtype=int)
red = np.zeros(shape, dtype=int)
green = np.zeros(shape, dtype=int)
blue = np.zeros(shape, dtype=int)

# split RGB values into separate matrices
for i in range(len(npdata)):
    for j in range(len(npdata[i])):
        red[i][j] = npdata[i][j][0]
        green[i][j] = npdata[i][j][1]
        blue[i][j] = npdata[i][j][2]

# get singular value count
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

# calculate compression ratio
uncompressed_size = width * height
compressed_size = (height * singular_value_choice) + singular_value_choice + (singular_value_choice * width)

# get approximations
red_approx = svd_approx(red, singular_value_choice) 
green_approx = svd_approx(green, singular_value_choice)
blue_approx = svd_approx(blue, singular_value_choice)

# write to new image
for i in range(height):
    for j in range(width):
        new_image[i][j][0] = int(red_approx[i][j])
        new_image[i][j][1] = int(green_approx[i][j])
        new_image[i][j][2] = int(blue_approx[i][j])

# create final image
final_image = Image.new(mode = "RGB", size = shape[::-1])
pixel = final_image.load()
y = 0
for i in range(len(new_image)): 
    x = 0
    for rgb in new_image[i]:
        pixel[x, y] = tuple(rgb) # write to pixel
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
original_img = Image.open(filename)
original_img = original_img.resize((window_width // 2, window_height - 50)) 
label = ImageTk.PhotoImage(image = original_img, master=window)  
tk.Label(window, image=label).pack(side=tk.RIGHT, expand=True)

# final image
final_image = final_image.resize((window_width // 2, window_height - 50))
label2 = ImageTk.PhotoImage(image = final_image, master=window)     
tk.Label(window, image=label2).pack(side=tk.LEFT, expand=True)

# run until closure
window.mainloop()