# Scraper Bot

**Scraper Bot** is a simple desktop application built with **Python** and **PySide6** that scrapes product data (like title, price, availability, image) from a given Etsy URL and saves it into a CSV file.  
It features a graphical interface with live preview of scraped products.

---

## ✨ Features
- Enter any Etsy URL to scrape product listings.
- View scraped products in a side panel with images.
- Preview product details and larger image.
- Save scraped data as a CSV file.
- Simple and lightweight GUI (PySide6 based).
- Loading indicator while scraping.

---

## 🛠 Technologies Used
- Python 3
- PySide6 (Qt for Python)
- pandas (for CSV saving)
- requests (for downloading images)
- BeautifulSoup / lxml (inside scraper module - assumed)

---

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Subrata0Ghosh/scraper-bot.git
cd scraper-bot
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

*(You may need to create a `requirements.txt` file listing: `PySide6`, `pandas`, `requests`, `beautifulsoup4`, etc.)*

---

## 🚀 Usage

1. Run the application:

```bash
python app.py
```

2. Paste an Etsy URL into the input field.
3. Click **Start Scraping**.
4. Browse products on the left panel.
5. Click **Save to CSV** to export results.

---

## 📂 Project Structure

```text
scraper-bot/
├── app.py                # Main GUI application
├── scraper/
│   └── etsy_scraper.py    # Etsy scraping logic
├── README.md              # Project description
└── requirements.txt       # Python package dependencies
```

---

## 🧩 To-Do
- Add support for pagination.
- Add more website scrapers (Amazon, eBay, etc.)
- Error handling improvements.

---

## 📝 License

This project is licensed under the MIT License - feel free to use, modify, and distribute it!

