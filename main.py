from tkinter import *
from tkinter.ttk import Progressbar
import sys
import os

# Function to exit the window
def exit_window():
    sys.exit()

# Function to open the login window
def top():
    root.withdraw()
    os.system("python login.py")
    root.destroy()

# Function to update the progress bar smoothly
def load():
    global progress_value
    if progress_value < 100:
        # Increment progress (faster than original)
        progress_value += 1  # Increase this value to make it faster
        
        # Update progress bar
        progress['value'] = progress_value
        txt = f'Loading System... {progress_value}%'
        progress_label.config(text=txt)
        
        # Schedule next update with shorter delay for smoother animation
        progress_label.after(20, load)  # Reduced from 1000ms to 20ms
    else:
        top()

# Initialize Tkinter
root = Tk()
root.attributes('-fullscreen', True)  # Make it truly fullscreen
root.config(background='#ffffff')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load image
image_path = os.path.join('images', 'logo.png')
try:
    image = PhotoImage(file=image_path)
    # Scale image proportionally to fit screen
    image = image.subsample(max(1, int(image.width()/(screen_width*0.6))))
except Exception as e:
    print(f"Failed to load image: {e}")
    image = None

# Create widgets with responsive positioning
welcome_label = Label(root, 
                     text='WELCOME TO POULTRY MANAGEMENT SYSTEM', 
                     bg='#ffffff', 
                     font=("Arial", int(screen_height/30), "bold"), 
                     fg='black')
welcome_label.pack(pady=int(screen_height*0.05))

if image:
    logo_label = Label(root, image=image, bg='#ffffff')
    logo_label.image = image
    logo_label.pack(pady=int(screen_height*0.05))

progress_label = Label(root, 
                      text="Loading System... 0%", 
                      font=('Arial', int(screen_height/45)), 
                      fg='black', 
                      bg='#ffffff')
progress_label.pack(pady=int(screen_height*0.05))

# Create a longer, thinner progress bar that spans most of the screen width
progress = Progressbar(root, 
                      orient=HORIZONTAL, 
                      length=int(screen_width*0.8), 
                      mode='determinate')
progress.pack(pady=int(screen_height*0.02))

# Modern exit button in top-right corner
exit_btn = Button(root, 
                 text='✕', 
                 bg='#ffffff', 
                 command=exit_window, 
                 bd=0, 
                 font=("Arial", int(screen_height/30)), 
                 activebackground='red', 
                 fg='black')
exit_btn.place(x=screen_width-60, y=10, width=50, height=50)

# Initialize progress counter
progress_value = 0

# Start loading process immediately
root.after(100, load)  # Short initial delay

# Run the application
root.mainloop()