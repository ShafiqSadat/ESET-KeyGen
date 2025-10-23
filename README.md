# Educational License Key Generator  

This repository contains a simple educational script (`main.py`) that demonstrates how to generate a random alphanumeric key and send it to a Telegram chat via the Telegram Bot API. It does **not** interact with ESET products and is **not** intended to generate or activate any commercial software licenses. The project is intended solely for learning purposes.  

## Disclaimer  

This tool is provided for educational purposes only. It does not generate real license keys for any software. Use of this script is at your own risk. The authors and contributors are not responsible for any misuse or damage caused by this project.  

## Usage  

1. Clone this repository or download the source files.  
2. Install dependencies from `requirements.txt` using `pip install -r requirements.txt`.  
3. Set the following environment variables before running the script:  
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token.  
   - `TELEGRAM_CHAT_ID`: The chat ID where you want to receive the generated key.  
4. Run the script:  
   ```bash  
   python3 main.py  
   ```  
   The script will generate a random uppercase alphanumeric string and send it to the specified Telegram chat. If the environment variables are not set, the script will prompt you to set them.  

## How it works  

The script uses Python's `random` and `string` modules to generate a 20-character uppercase alphanumeric string. It then uses the Telegram Bot API (via `requests`) to send a message containing the generated key to the chat ID you specify. For more details, see `main.py`.  

## Contributing  

Contributions to improve the educational value of this project are welcome. Please ensure that any changes adhere to legal and ethical guidelines.  

## License  

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
