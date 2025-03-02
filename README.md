
# **Twittomation**  

## **Project Overview**  
Twittomation is a Python-based automation tool that interacts with Twitter using the Tweepy library. It enables actions like fetching tweets and liking them programmatically.  

## **Installation & Setup**  

### **Prerequisites**  
- Python 3.8+  
- A Twitter Developer account with API access  

### **Clone the Repository**  
```sh
git clone https://github.com/CCathlete/twittomation.git
cd twittomation
```

### **Create a Virtual Environment**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **Set Up Environment Variables**  
Create a `.env` file in the project root with the following content:  

```ini
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_TWEET_ID=1234567890123456789  # Replace with an actual tweet ID
```

## **Usage**  

### **Run the Main Function**  
```sh
python -m src.presentation.main
```

### **Example Output**  
```
[INFO] Fetching tweet with ID 1234567890123456789...
[INFO] Liking the tweet...
[INFO] Tweet liked successfully!
```

## **Configuration**  

### **Environment Variables**  
| Variable | Description |
|----------|------------|
| `TWITTER_CONSUMER_KEY` | API key from Twitter Developer Portal |
| `TWITTER_CONSUMER_SECRET` | API secret key |
| `TWITTER_ACCESS_TOKEN` | Access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Access token secret |
| `TWITTER_TWEET_ID` | ID of the tweet to like |
