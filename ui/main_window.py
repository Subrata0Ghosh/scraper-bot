from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTextEdit, QLabel, QFileDialog, QHBoxLayout, QListWidget, QListWidgetItem
)
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
from scraper.etsy_scraper import scrape_data
import pandas as pd
import requests

class ScraperThread(QThread):
    finished = Signal(list)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        data = scrape_data(self.url)
        self.finished.emit(data)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper Bot")
        self.setGeometry(300, 100, 1000, 600)

        self.scraped_data = []  # To store scraped results

        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        # URL Input and Buttons
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL here...")
        self.scrape_button = QPushButton("Start Scraping")
        self.scrape_button.clicked.connect(self.start_scraping)
        self.save_button = QPushButton("Save to CSV")
        self.save_button.clicked.connect(self.save_to_csv)
        self.save_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel("Target URL:"))
        button_layout.addWidget(self.url_input)
        button_layout.addWidget(self.scrape_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        # Main split view: list on left, preview on right
        self.split_layout = QHBoxLayout()
        main_layout.addLayout(self.split_layout)

        # Left side: List of products
        self.product_list = QListWidget()
        self.product_list.itemClicked.connect(self.show_preview)
        self.split_layout.addWidget(self.product_list, 40)  # 40% width

        # Right side: Product preview
        self.preview_widget = QWidget()
        preview_layout = QVBoxLayout()
        self.preview_widget.setLayout(preview_layout)

        self.preview_image = QLabel("Image Preview Here")
        self.preview_image.setFixedSize(300, 300)
        self.preview_image.setScaledContents(True)

        self.preview_details = QTextEdit()
        self.preview_details.setReadOnly(True)

        preview_layout.addWidget(self.preview_image)
        preview_layout.addWidget(self.preview_details)

        self.split_layout.addWidget(self.preview_widget, 60)  # 60% width


        

    def start_scraping(self):
        url = self.url_input.text().strip()
        if url:
            self.product_list.clear()
            self.preview_image.clear()
            self.preview_details.clear()
            self.product_list.addItem("Scraping started...")
            
            self.thread = ScraperThread(url)
            self.thread.finished.connect(self.scraping_finished)
            self.thread.start()
        else:
            self.product_list.addItem("Please enter a valid URL!")

    def scraping_finished(self, data):
        self.product_list.clear()  # <<< Clear loading text
        self.scraped_data = data
        if data:
            for item in data:
                list_item = QListWidgetItem(item['title'])
                list_item.setData(1000, item)  # Store full product info inside the item
                self.product_list.addItem(list_item)
            self.save_button.setEnabled(True)
        else:
            self.product_list.addItem("No data scraped or an error occurred.")

    def show_preview(self, list_item):
        product = list_item.data(1000)
        if not product:
            return

        # Show product details
        details_text = f"Title: {product['title']}\nPrice: {product['price']}\nAvailability: {product['availability']}\nURL: {product['product_url']}"
        self.preview_details.setPlainText(details_text)

        # Show product image
        image_url = product.get('image_url')
        if image_url:
            try:
                response = requests.get(image_url)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.preview_image.setPixmap(pixmap)
            except Exception as e:
                self.preview_image.setText("Failed to load image")
        else:
            self.preview_image.setText("No image available")

    def save_to_csv(self):
        if not self.scraped_data:
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                df = pd.DataFrame(self.scraped_data)
                df.to_csv(path, index=False)
                self.preview_details.append(f"\nData saved to {path}")
            except Exception as e:
                self.preview_details.append(f"\nFailed to save file: {str(e)}")
