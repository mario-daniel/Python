import customtkinter as ctk
from PIL import Image

window = ctk.CTk()
ctk.set_appearance_mode('light')

frame = ctk.CTkFrame(window, width = 500, height = 600)
frame.pack()
profile_icon = ctk.CTkImage(light_image = Image.open("profile.png"), size = (50,50))
ctk.CTkButton(frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20)).pack()
window.mainloop()
