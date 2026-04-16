import sys
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFileDialog, QTextEdit, QLabel, 
                             QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import pandas as pd
from docx import Document

class OCRWorker(QThread):
    result_ready = pyqtSignal(dict)
    progress = pyqtSignal(int, str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            full_text = ""
            excel_data = []
            self.progress.emit(20, "جاري معالجة الملف...")
            
            if self.file_path.lower().endswith('.pdf'):
                images = convert_from_path(self.file_path)
            else:
                images = [Image.open(self.file_path)]

            for i, img in enumerate(images):
                page_text = pytesseract.image_to_string(img, lang='ara+eng+deu')
                full_text += f"\n--- صفحة {i+1} ---\n{page_text}"
                
                # استخراج الأسئلة للإكسيل
                lines = page_text.split('\n')
                for line in lines:
                    if line.strip() and re.match(r'^\d+', line.strip()):
                        excel_data.append({"السؤال": line.strip(), "الصفحة": i+1})
                
                self.progress.emit(50, f"تمت قراءة صفحة {i+1}")

            self.progress.emit(100, "اكتمل الاستخراج")
            self.result_ready.emit({"text": full_text, "data": excel_data})
        except Exception as e:
            self.result_ready.emit({"error": str(e)})

class ProfessionalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.extracted_text = ""
        self.extracted_data = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("نظام استخراج وتنظيم البيانات الذكي")
        self.resize(1000, 700)
        self.setStyleSheet("QMainWindow { background-color: #1a1a1a; } QTextEdit { background-color: #2b2b2b; color: white; border-radius: 5px; padding: 10px; font-size: 12pt; } QPushButton { background-color: #3d3d3d; color: white; border-radius: 5px; padding: 8px; font-weight: bold; } QPushButton:hover { background-color: #505050; }")

        layout = QVBoxLayout()
        
        # الأزرار العلوية
        top_bar = QHBoxLayout()
        self.btn_load = QPushButton("تحميل ملف (صورة/PDF)")
        self.btn_word = QPushButton("تصدير إلى Word")
        self.btn_excel = QPushButton("تصدير إلى Excel")
        self.btn_excel.setStyleSheet("background-color: #217346;") # لون الإكسيل الأخضر
        
        top_bar.addWidget(self.btn_load)
        top_bar.addWidget(self.btn_word)
        top_bar.addWidget(self.btn_excel)
        
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("الحالة: جاهز")
        self.status_label.setStyleSheet("color: #aaa;")
        
        self.display = QTextEdit()
        
        layout.addLayout(top_bar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.btn_load.clicked.connect(self.start_ocr)
        self.btn_word.clicked.connect(self.save_word)
        self.btn_excel.clicked.connect(self.save_excel)

    def start_ocr(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف", "", "Images (*.png *.jpg *.pdf)")
        if file_path:
            self.worker = OCRWorker(file_path)
            self.worker.progress.connect(self.update_progress)
            self.worker.result_ready.connect(self.finish_ocr)
            self.worker.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(f"الحالة: {msg}")

    def finish_ocr(self, results):
        if "error" in results:
            QMessageBox.critical(self, "خطأ", results["error"])
        else:
            self.extracted_text = results["text"]
            self.extracted_data = results["data"]
            self.display.setText(self.extracted_text)

    def save_word(self):
        if not self.extracted_text: return
        path, _ = QFileDialog.getSaveFileName(self, "حفظ Word", "النتيجة.docx", "Word Files (*.docx)")
        if path:
            doc = Document()
            doc.add_paragraph(self.extracted_text)
            doc.save(path)
            QMessageBox.information(self, "نجاح", "تم حفظ ملف Word")

    def save_excel(self):
        if not self.extracted_data:
            QMessageBox.warning(self, "تنبيه", "لا توجد بيانات منظمة للتصدير!")
            return
        path, _ = QFileDialog.getSaveFileName(self, "حفظ Excel", "الأسئلة.xlsx", "Excel Files (*.xlsx)")
        if path:
            df = pd.DataFrame(self.extracted_data)
            df.to_excel(path, index=False)
            QMessageBox.information(self, "نجاح", "تم حفظ ملف Excel")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfessionalApp()
    window.show()
    sys.exit(app.exec())