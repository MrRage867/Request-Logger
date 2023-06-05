import threading
import telebot
import socket
import random
import string
import time

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

live_hashes = []
ongoing_logs = []

def socket_server(sock):
    try:
        data = sock.recv(4096).decode("utf-8")
        data = data.replace("\r", "")
        for live_hash in live_hashes:
            if live_hash.lower() in data.lower():
                with open(f"RequestLogs/{live_hash}.log", "a") as add:
                    add.write(f"{data}\n")
                sock.send(str.encode("HTTP/1.1 200 OK\n\n" + data))
                sock.close()
        sock.send(str.encode("HTTP/1.1 200 OK\n\n200 OK"))
        sock.close()
    except:
        sock.close()

def socket_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", 80))
    except:
       print("Failed to start the socket server")
    server.listen(999999)

    while True:
        try:
            sock, addr = server.accept()
        except:
            continue
        try:
            threading.Thread(target=socket_server, args=(sock,)).start()
        except:
            continue

def generate_hash():
    characters = string.ascii_letters + string.digits
    random_hash = ''.join(random.choice(characters) for _ in range(10))
    return random_hash

def handle_log(message, seconds, log_hash, previous):
    live_hashes.append(log_hash)
    ongoing_logs.append(str(message.chat.id))
    time.sleep(int(seconds))
    live_hashes.remove(log_hash)
    ongoing_logs.remove(str(message.chat.id))
    try:
        file = open(f"RequestLogs/{log_hash}.log", "rb")
        num_requests = len(open(f"RequestLogs/{log_hash}.log").read().split("\n\n"))
        bot.edit_message_text(
            text=f"Requests Received: *{num_requests}*",
            chat_id=message.chat.id,
            message_id=previous.message_id,
            parse_mode="MarkdownV2"
        )
        bot.send_document(message.chat.id, file)
    except:
        bot.edit_message_text("No requests received.", message.chat.id, previous.message_id)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "Use /log to start logging. Made by @MrRage :)")

@bot.message_handler(commands=['log'])
def log(message):
    data = message.text.split(" ")
    try:
        seconds = data[1]
        if str(message.chat.id) in ongoing_logs:
            bot.send_message(message.chat.id, "It appears that a logger is currently in progress.")
        elif int(seconds) > 299:
            bot.send_message(message.chat.id, "No more than 300 seconds allowed.")
        else:
            log_hash = generate_hash()
            confirmation = bot.send_message(
                message.chat.id,
                f"Logging on `http://127.0.0.1/{log_hash}` for {seconds} seconds...",
                parse_mode="MarkDownV2"
            )
            handle_log(message, seconds, log_hash, confirmation)
    except:
        bot.send_message(message.chat.id, "Usage: /log [Seconds]")

def main():
    threading.Thread(target=socket_listener).start()
    while True:
        try:
            bot.polling(none_stop=True, timeout=20)
        except:
            bot.stop_polling()
            time.sleep(3)

if __name__ == '__main__':    
    main()
