# 🎵 Web Scrapping / Song Downloader

A Python-based web scraper that downloads Tamil movie songs (ZIP format) by year from example.com.

---

## 🚀 Features

* 📅 Download songs by **year range**
* 🎧 Supports **320kbps & 128kbps**
* 🔄 Automatic pagination (fetches all movies)
* ⏭ Skips already downloaded files (resume support)
* 📁 Organized output: `downloads/{year}/`
* 📊 Download progress indicator

---

## 📦 Project Structure

```
MP3-Song-Downloader-masstamilan/
│
├── masstamilan_downloader.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
│
├── config/
│   └── config.example.yaml
│
├── logs/
│   └── .gitkeep
│
├── downloads/
│   └── .gitkeep
│
└── scripts/
    └── run.sh
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MARIOREDFOX/MP3-Song-Downloader-masstamilan-.git
cd MP3-Song-Downloader-masstamilan
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the script:

```bash
python masstamilan_downloader.py
```

Or using the helper script:

```bash
bash scripts/run.sh
```

---

## 🔧 Configuration

Update the configuration directly inside the script:

```python
YEAR_FROM    = 2000
YEAR_TO      = 2026
QUALITY      = "320"   # "320" or "128"
DOWNLOAD_DIR = "./downloads"
DELAY        = 3
```

---

## 📁 Output Example

```
downloads/
├── 2000/
│   ├── Movie1_320kbps.zip
│   ├── Movie2_320kbps.zip
│
├── 2001/
│   └── Movie3_320kbps.zip
```

---

## 🧠 How It Works

1. Scrapes movies by year
2. Visits each movie page
3. Extracts ZIP download link
4. Downloads file with progress tracking
5. Skips if already exists

---

## ⚠️ Disclaimer

* This project is intended for **educational purposes only**
* Do not misuse or violate any website's **terms of service**
* Respect copyright laws and content ownership

---

## 🛠 Requirements

* Python 3.8+
* Libraries:

  * `cloudscraper`
  * `beautifulsoup4`

---

## 👨‍💻 Author

**Marie Infantraj**

---

## ⭐ Support

If you find this project useful:

* ⭐ Star the repo
* 🍴 Fork it
* 🛠 Contribute improvements

---
