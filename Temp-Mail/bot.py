# Telegram Bot for Smart TempMail API
# Copyright @ISmartCoder
# Updates Channel https://t.me/abirxdhackz

import os
import asyncio
import aiohttp
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TempMailBot:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.api_url = os.getenv('API_URL', 'http://localhost:8000')
        self.user_sessions = {}
        
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable is required")
    
    async def make_api_request(self, endpoint: str) -> dict:
        """Make HTTP request to TempMail API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}{endpoint}") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"API request failed with status {response.status}"}
        except Exception as e:
            logger.error(f"API request error: {str(e)}")
            return {"error": f"Connection error: {str(e)}"}
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🌟 *Welcome to Smart TempMail Bot* 🌟

Hello {user.first_name}! 👋

I can help you generate and manage temporary email addresses instantly! 

*Available Commands:*
📧 /gen - Generate regular temporary email
⏱️ /tenmin - Generate 10-minute email  
🎓 /edu - Generate .edu email
📬 /check - Check messages for your emails
❓ /help - Show this help message

*Quick Actions:*
        """
        
        keyboard = [
            [InlineKeyboardButton("📧 Generate Email", callback_data="gen_regular")],
            [InlineKeyboardButton("⏱️ 10-Min Email", callback_data="gen_10min")],
            [InlineKeyboardButton("🎓 Edu Email", callback_data="gen_edu")],
            [InlineKeyboardButton("📬 Check Messages", callback_data="check_messages")],
            [InlineKeyboardButton("🔗 Visit API", url=f"{self.api_url}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🔹 *Smart TempMail Bot Help* 🔹

*Commands:*
• `/start` - Show welcome message
• `/gen` - Generate regular temporary email
• `/tenmin` - Generate 10-minute email (expires in 10 min)
• `/edu` - Generate educational (.edu) email
• `/check` - Check messages for your active emails
• `/help` - Show this help

*How to use:*
1️⃣ Generate an email using any command
2️⃣ Use the email for your needs
3️⃣ Check messages using /check or buttons
4️⃣ Copy emails and tokens easily

*Features:*
✅ Multiple email types
✅ Instant generation
✅ Message checking
✅ Auto-expiration for 10-min emails
✅ Easy copy/paste

*Developer:* @ISmartCoder
*Updates:* @WeSmartDevelopers
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def generate_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE, email_type: str = "regular"):
        """Generate temporary email"""
        user_id = update.effective_user.id
        loading_msg = await update.message.reply_text("🔄 Generating your temporary email...")
        
        # Determine API endpoint
        endpoints = {
            "regular": "/api/gen",
            "10min": "/api/10min/gen", 
            "edu": "/api/edu/gen"
        }
        
        endpoint = endpoints.get(email_type, "/api/gen")
        result = await self.make_api_request(endpoint)
        
        await loading_msg.delete()
        
        if "error" in result:
            await update.message.reply_text(f"❌ Error: {result['error']}")
            return
        
        # Store user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        
        email_key = "edu_mail" if email_type == "edu" else "temp_mail"
        email = result.get(email_key)
        token = result.get("access_token")
        
        self.user_sessions[user_id][email] = {
            "token": token,
            "type": email_type,
            "created_at": datetime.now()
        }
        
        # Format response message
        email_icon = "🎓" if email_type == "edu" else "⏱️" if email_type == "10min" else "📧"
        expiry_info = f"\n⏰ *Expires:* {result.get('expires_at', 'N/A')}" if email_type == "10min" else ""
        
        response_text = f"""
{email_icon} *Temporary Email Generated!*

📬 *Email:* `{email}`
🔑 *Token:* `{token}`
⚡ *Generated in:* {result.get('time_taken', 'N/A')}
👨‍💻 *API by:* {result.get('api_owner', '@ISmartCoder')}{expiry_info}

*Tap to copy email or token* ☝️
        """
        
        keyboard = [
            [InlineKeyboardButton("📬 Check Messages", callback_data=f"check_{email}")],
            [InlineKeyboardButton("🔄 Generate New", callback_data=f"gen_{email_type}")],
            [InlineKeyboardButton("📋 Copy Email", callback_data=f"copy_{email}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def check_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE, email: str = None):
        """Check messages for emails"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions or not self.user_sessions[user_id]:
            await update.message.reply_text(
                "❌ No active emails found. Generate an email first using /gen, /tenmin, or /edu"
            )
            return
        
        if email and email not in self.user_sessions[user_id]:
            await update.message.reply_text("❌ Email not found in your active sessions.")
            return
        
        # If no specific email, show all emails
        if not email:
            emails_text = "📬 *Your Active Emails:*\n\n"
            keyboard = []
            
            for user_email, session_data in self.user_sessions[user_id].items():
                email_type = session_data.get('type', 'regular')
                email_icon = "🎓" if email_type == "edu" else "⏱️" if email_type == "10min" else "📧"
                created = session_data.get('created_at')
                created_str = created.strftime("%H:%M") if created else "Unknown"
                
                emails_text += f"{email_icon} `{user_email}`\n📅 Created: {created_str}\n\n"
                keyboard.append([InlineKeyboardButton(f"📬 Check {user_email[:20]}...", callback_data=f"check_{user_email}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(emails_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            return
        
        # Check specific email
        session_data = self.user_sessions[user_id][email]
        token = session_data['token']
        email_type = session_data.get('type', 'regular')
        
        loading_msg = await update.message.reply_text("🔍 Checking messages...")
        
        # Determine check endpoint
        check_endpoints = {
            "regular": f"/api/chk?token={token}",
            "10min": f"/api/10min/chk?token={token}",
            "edu": f"/api/edu/chk?token={token}"
        }
        
        endpoint = check_endpoints.get(email_type, f"/api/chk?token={token}")
        result = await self.make_api_request(endpoint)
        
        await loading_msg.delete()
        
        if "error" in result:
            await update.message.reply_text(f"❌ Error checking messages: {result['error']}")
            return
        
        messages = result.get('messages', [])
        email_from_result = result.get('mailbox') or result.get('edu_mail', email)
        
        if not messages:
            response_text = f"""
📭 *No messages found*

📬 *Email:* `{email_from_result}`
🔍 *Checked at:* {datetime.now().strftime('%H:%M:%S')}

Messages will appear here when received.
            """
        else:
            response_text = f"📬 *Messages for:* `{email_from_result}`\n\n"
            
            for i, msg in enumerate(messages[:5], 1):  # Show max 5 messages
                sender = msg.get('from') or msg.get('From', 'Unknown')
                subject = msg.get('subject') or msg.get('Subject', 'No Subject')
                date = msg.get('receivedAt') or msg.get('Date', 'Unknown')
                body = msg.get('body') or msg.get('Message', 'No content')
                
                # Truncate long content
                if len(body) > 100:
                    body = body[:97] + "..."
                
                response_text += f"""
📨 *Message {i}:*
👤 *From:* {sender}
📝 *Subject:* {subject}
📅 *Date:* {date}
💬 *Content:* {body}

────────────────
                """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"check_{email}")],
            [InlineKeyboardButton("📧 Generate New", callback_data="gen_regular")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("gen_"):
            email_type = data.replace("gen_", "")
            await self.generate_email(query, context, email_type)
        
        elif data.startswith("check_"):
            if data == "check_messages":
                await self.check_messages(query, context)
            else:
                email = data.replace("check_", "")
                await self.check_messages(query, context, email)
        
        elif data.startswith("copy_"):
            email = data.replace("copy_", "")
            await query.edit_message_text(
                f"📋 *Email copied!*\n\n`{email}`\n\nTap the email above to copy it.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def gen_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gen command"""
        await self.generate_email(update, context, "regular")
    
    async def tenmin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tenmin command"""
        await self.generate_email(update, context, "10min")
    
    async def edu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /edu command"""
        await self.generate_email(update, context, "edu")
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command"""
        await self.check_messages(update, context)
    
    def run_bot(self):
        """Start the bot"""
        application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("gen", self.gen_command))
        application.add_handler(CommandHandler("tenmin", self.tenmin_command))
        application.add_handler(CommandHandler("edu", self.edu_command))
        application.add_handler(CommandHandler("check", self.check_command))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        logger.info("Smart TempMail Bot starting...")
        logger.info(f"API URL: {self.api_url}")
        
        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        # Start keep-alive server if enabled
        if os.getenv('ENABLE_KEEP_ALIVE', 'false').lower() == 'true':
            try:
                from keep_alive import keep_alive
                keep_alive()
                logger.info("Keep-alive server started")
            except ImportError:
                logger.warning("keep_alive module not found, skipping keep-alive server")
            except Exception as e:
                logger.warning(f"Failed to start keep-alive server: {e}")
        
        # Start the bot
        bot = TempMailBot()
        bot.run_bot()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print("Please set BOT_TOKEN environment variable with your Telegram bot token")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"Error starting bot: {e}")