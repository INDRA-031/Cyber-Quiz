import logging
import random
from telegram import Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==== CONFIG ====
BOT_TOKEN = "<your-telegram-bot-token>"
CHAT_ID = <your-telegram-group-chat-id>  # Replace with your group chat ID
TOPIC_ID = <target-topic-thread-id>  # Topic ID where quizzes will be sent
QUIZ_FILE = "questions.txt"  # Path to quiz questions file
# ================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_questions():
    questions = []
    try:
        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip().split("\n\n")
            for block in content:
                lines = block.strip().split("\n")
                if not lines or len(lines) < 3:
                    continue
                question_text = lines[0].replace("[ Poll : ", "").replace("]", "").strip()
                options = []
                correct_index = None
                explanation = ""
                for idx, line in enumerate(lines[1:]):
                    if line.startswith("*"):
                        options.append(line[2:].strip())
                        correct_index = idx
                    elif line.startswith("-"):
                        options.append(line[2:].strip())
                    elif line.startswith("> Explanation:"):
                        explanation = "\n".join(lines[idx+2:]).strip()
                        break
                if question_text and options and correct_index is not None:
                    questions.append({
                        "question": question_text,
                        "options": options,
                        "correct_index": correct_index,
                        "explanation": explanation
                    })
    except Exception as e:
        logger.error(f"Error loading questions: {e}")
    return questions

async def send_quiz(bot, chat_id, topic_id):
    questions = load_questions()
    if not questions:
        logger.error("No questions found!")
        return
    question = random.choice(questions)
    await bot.send_poll(
        chat_id=chat_id,
        message_thread_id=topic_id,
        question=question['question'],
        options=question['options'],
        type=Poll.QUIZ,
        correct_option_id=question['correct_index'],
        explanation=question['explanation'],
        explanation_parse_mode='HTML',
        is_anonymous=False
    )
    logger.info(f"Sent quiz: {question['question']}")

async def send_daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context.bot, CHAT_ID, TOPIC_ID)

async def test_command(update, context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context.bot, CHAT_ID, TOPIC_ID)
    await context.bot.send_message(chat_id=CHAT_ID, message_thread_id=TOPIC_ID,
                                   text="Test quiz sent. Please answer to see the explanation.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("test", test_command))

    # Schedule quiz every 6 hours (6*60*60 seconds)
    job_queue = app.job_queue
    job_queue.run_repeating(send_daily_quiz, interval=6*60*60, first=10)

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
