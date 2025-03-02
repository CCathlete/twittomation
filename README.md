# **Twittomation**  

## **Project Overview**  
Twittomation is a Python-based automation tool that interacts with Twitter using the Tweepy library. It enables actions like fetching tweets and liking them programmatically.  

## **Installation & Setup**  

### **Prerequisites**  
- Python 3.8+ or PyPy 3.9+  
- A Twitter Developer account with API access  

### **Clone the Repository**  
```sh
git clone https://github.com/CCathlete/twittomation.git
cd twittomation
```

### **Choose Your Setup Method**  
You can set up Twittomation in three different ways:

1. **Using `venv` and `requirements.txt`** (Recommended for most users)  
2. **Using Conda and `environment.yml`**  
3. **Running a Standalone Executable** (No setup needed)  

---

### **Option 1: Create a Virtual Environment (venv, CPython)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### **Option 2: Create a Conda Environment (pypy)**
```sh
conda env create -f twittomation-conda-env.yml
conda activate twittomation
```

---

### **Option 3: Run the Standalone Executable**
If you have downloaded the prebuilt executable or created one yourself, you can run it directly:

```sh
./dist/main  # On Windows: dist\main.exe
```
⚠ **Ensure that the `.env` file is in the root directory (same location as `requirements.txt`).**  

---

### **Set Up Environment Variables**  
Create a `.env` file in the **project root** with the following content:  

```ini
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_TWEET_ID=1234567890123456789  # Replace with an actual tweet ID
```

## **Usage**  

### **Run the Main Function**  
#### **If Using venv or Conda**
```sh
python -m src.presentation.main
```

#### **If Using the Standalone Executable**
```sh
./dist/main  # On Windows: dist\main.exe
```

### **Example Output**  
```
[INFO] Fetching tweet with ID 1234567890123456789...
[INFO] Liking the tweet...
[INFO] Tweet liked successfully!
```

## **Building an Executable with PyInstaller**  

To bundle the project into an executable, use **PyInstaller**:  
```sh
pyinstaller --onefile --name main src/presentation/main.py
```
This creates a standalone binary inside the `dist/` folder.  

**Note:** The `.env` file should remain in the root directory.

## **Configuration**  

### **Environment Variables**  
| Variable | Description |
|----------|------------|
| `TWITTER_CONSUMER_KEY` | API key from Twitter Developer Portal |
| `TWITTER_CONSUMER_SECRET` | API secret key |
| `TWITTER_ACCESS_TOKEN` | Access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Access token secret |
| `TWITTER_TWEET_ID` | ID of the tweet to like |
