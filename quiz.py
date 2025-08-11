import logging
import random
import os
from telegram import Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==== CONFIG ====
BOT_TOKEN = "<YOUR_BOT_TOKEN>"
CHAT_ID = <YOUR_CHAT_ID>  # Replace with your group chat ID
TOPIC_ID = <YOUR_TOPIC_ID>  # Topic ID where quizzes will be sent
QUIZ_FILE = "questions.txt"  # Path to quiz questions file
SENT_FILE = "sent_questions.txt"  # File to store sent questions
# ================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sent_questions():
    """Load list of already sent questions from file."""
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_question(question_text):
    """Save sent question to file."""
    with open(SENT_FILE, "a", encoding="utf-8") as f:
        f.write(question_text + "\n")

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

    sent_questions = load_sent_questions()

    # Filter out already sent questions
    available_questions = [q for q in questions if q["question"] not in sent_questions]

    if not available_questions:
        logger.info("All questions sent. Resetting list...")
        open(SENT_FILE, "w").close()  # Clear file
        available_questions = questions

    question = random.choice(available_questions)

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

    save_sent_question(question['question'])
    logger.info(f"Sent quiz: {question['question']}")

async def send_daily_quiz(context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context.bot, CHAT_ID, TOPIC_ID)

async def test_command(update, context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context.bot, CHAT_ID, TOPIC_ID)
    await context.bot.send_message(
        chat_id=CHAT_ID,
        message_thread_id=TOPIC_ID,
        text="Test quiz sent. Please answer to see the explanation."
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("test", test_command))

    # Schedule quiz every 6 hours
    job_queue = app.job_queue
    job_queue.run_repeating(send_daily_quiz, interval=6*60*60, first=10)

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
