import customtkinter as ctk
from tkinter import filedialog
import os
import shutil

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python File Organizer")
        self.geometry("500x300")

        self.label = ctk.CTkLabel(self, text="File Organizer Tool", font=("Roboto", 24))
        self.label.pack(pady=20)

        self.btn_select = ctk.CTkButton(self, text="Select Folder to Organize", command=self.select_and_organize)
        self.btn_select.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready", text_color="gray")
        self.status_label.pack(pady=10)

    def select_and_organize(self):
        folder_path = filedialog.askdirectory()
        
        if folder_path:
            self.status_label.configure(text="Organizing...", text_color="yellow")
            self.update()
            
            self.organize(folder_path)
            
            self.status_label.configure(text="✅ Done! Folder organized.", text_color="green")
        else:
            self.status_label.configure(text="No folder selected", text_color="red")

    def organize(self, path):
        file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
            'Videos': ['.mp4', '.mkv', '.mov', '.avi'],
            'Archives': ['.zip', '.rar', '.7z', '.tar.gz'],
            'Scripts': ['.py', '.sh', '.js', '.html', '.css']
        }
        
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                extension = os.path.splitext(filename)[1].lower()
                for folder, extensions in file_types.items():
                    if extension in extensions:
                        dest_folder = os.path.join(path, folder)
                        if not os.path.exists(dest_folder):
                            os.makedirs(dest_folder)
                        shutil.move(filepath, os.path.join(dest_folder, filename))
                        break

if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()