````markdown
# 🚀 Telegram Cyber Quiz Bot

**Automate your group’s brainpower with periodic, sharp cybersecurity quizzes — delivered straight into your Telegram topic threads every 6 hours.**

---

## 🛠️ Overview

This bot injects interactive, timed quiz challenges into your Telegram groups, crafted for pentesters, infosec enthusiasts, and hacking pros. It turns your chat into a continuous learning arena with polls that test real-world cyber knowledge — all loaded from an easy-to-manage question bank.

- 🔥 Sends **quiz polls** with multiple-choice questions  
- 🕒 Fires off a new challenge **every 6 hours**  
- ✅ Automatically marks the **correct answer** and provides detailed **explanations**  
- 🎯 Targets specific **topic threads** in supergroups (via `message_thread_id`)  
- 🎮 Manual `/test` command to instantly drop a quiz on demand

---

## ⚙️ Setup & Configuration

Before you unleash the bot, tune these parameters inside the script (`q.py`):

```python
BOT_TOKEN = "<your-telegram-bot-token>"
CHAT_ID = <your-telegram-group-chat-id>
TOPIC_ID = <target-topic-thread-id>  # where quizzes will land
QUIZ_FILE = "questions.txt"          # plaintext quiz question repository
````

> Make sure your bot has admin rights to post polls in the group and access to the target topic thread.

---

## 🔍 Question File Format

Your quiz question bank (`questions.txt`) uses a simple markdown-inspired format:

```
[ Poll : What is the primary tool for network traffic analysis? ]
* Wireshark
- Nmap
- Metasploit
- Burp Suite
> Explanation:
Wireshark is the go-to packet analyzer used by security pros worldwide to capture and inspect network traffic.
```

* Use `*` to tag the **correct answer**
* Use `-` for **other choices**
* `> Explanation:` section is **optional but recommended** for post-quiz learning
* Separate quizzes by **one blank line**

---

## 🚀 How to Run

1. Install the required library:

```bash
pip install python-telegram-bot --upgrade
```

2. Run the bot:

```bash
python quiz.py
```

3. The bot will quietly work in the background, posting quizzes every **6 hours** into your defined group topic.
4. Need to test the bot or drop a spontaneous quiz? Send `/test` command in the group.

---

## 🎯 Why Use This Bot?

* Keep your community **engaged and learning** without manual effort
* Perfect for **security teams**, **CTF groups**, or **infosec classrooms**
* Lightweight and easy to customize with your own question sets
* Built with Python and the trusted **python-telegram-bot** library for robust, async performance

---

## 👨‍💻 Author

**INDRA** — Security aficionado and bot whisperer.
Feel free to fork, tweak, and hack your own version.

---

## 📜 License

This project is open-source under the **MIT License**.
Use it, break it, fix it, but always share your code.

---

*Powered by curiosity and the quest for knowledge. Stay sharp, stay safe.*

```

If you want, I can also generate a slick example `questions.txt` file for you!
```
