from PIL import Image, ImageTk
import customtkinter as ctk

window = ctk.CTk()
window.title('RFID System')
window.geometry('900x600')
window.resizable(False, False)
ctk.set_appearance_mode('light')
window_frame = ctk.CTkFrame(window, fg_color = '#ff7e75', corner_radius = 0, border_color = 'black', border_width = 2)
window_frame.pack(expand = True, fill = 'both')

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width = 200, height = 600, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.place(anchor = 'nw', relx = 0, rely = 0)
        profile_icon = ctk.CTkImage(light_image = Image.open("profile.png"), size = (70,70))
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.15)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Booking History & \nSupport', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.35)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approval Request & \nOutgoing Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.5)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'My Analytics', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.63)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Logout', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.93)
        self.content_frame = ctk.CTkFrame(window_frame, width = 650, height = 550, border_color = 'black', border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.content_frame.place(anchor = 'center', relx = 0.61, rely = 0.5)

sidebar = Sidebar(window_frame)

#ctk.CTkButton(sidebar.content_frame).place(anchor = 'center', relx = 0.5, rely = 0.5)

window.mainloop()
