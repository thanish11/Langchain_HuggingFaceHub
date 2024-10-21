from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import webbrowser
from threading import Timer
from models import OvarianCancerChatbot  # Assuming you have this class implemented

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use session

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8080/")

@app.route('/')
def home():
    session.clear()  # Clear session when going back to the home page
    return render_template('home.html')

# Chat route to handle user input and chatbot interaction
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    bot = OvarianCancerChatbot()

    if 'chat_history' not in session:
        session['chat_history'] = []  # Initialize chat history

    if request.method == 'POST':
        user_input = request.form.get('query', '').strip().lower()  # Extract user query
        session['chat_history'].append(f"You: {user_input}")

        # Store biomarkers in session
        if 'ca125' not in session:
            ca125 = request.form.get('CA125', None)
            if ca125:
                try:
                    session['ca125'] = float(ca125)  # Accept float
                except ValueError:
                    session['chat_history'].append("Bot: Please enter a valid float value for CA125.")
                    return render_template('chat.html', chat_history=session['chat_history'])

        if 'he4' not in session:
            he4 = request.form.get('HE4', None)
            if he4:
                try:
                    session['he4'] = float(he4)  # Accept float
                except ValueError:
                    session['chat_history'].append("Bot: Please enter a valid float value for HE4.")
                    return render_template('chat.html', chat_history=session['chat_history'])

        if 'menopause_status' not in session:
            menopause_status = request.form.get('menopause_status', '').strip().lower()
            if menopause_status not in ["premenopause", "postmenopause"]:
                session['chat_history'].append("Bot: Invalid menopause status. Please provide 'premenopause' or 'postmenopause'.")
                return render_template('chat.html', chat_history=session['chat_history'])
            session['menopause_status'] = menopause_status

        # If biomarkers are all collected, calculate the ROMA score
        if 'ca125' in session and 'he4' in session and 'menopause_status' in session:
            try:
                roma_score = bot.calculate_roma_score(session['ca125'], session['he4'], session['menopause_status'])
                roma_message = f"Your ROMA score is {roma_score:.2f}%."
                if roma_score >= 7.4:
                    roma_message += " High risk of ovarian cancer. Please consult a specialist."
                else:
                    roma_message += " Low risk, but regular monitoring is recommended."
                session['chat_history'].append(f"Bot: {roma_message}")
            except ValueError:
                session['chat_history'].append('Bot: Invalid input for CA125 or HE4.')

        # Respond to general user queries
        response = ""
        if "hospital" in user_input:
            response = bot.query_pdf(bot.hospital_store, user_input)
        elif "diet" in user_input:
            response = bot.query_pdf(bot.diet_store, user_input)
        elif "ovarian" in user_input:
            response = bot.query_pdf(bot.common_store, user_input)
        else:
            response = bot.answer_general_query(user_input)

        session['chat_history'].append(f"Bot: {response}")
        return render_template('chat.html', chat_history=session['chat_history'])

    return render_template('chat.html', chat_history=session['chat_history'])

# Route to end chat
@app.route('/end_chat')
def end_chat():
    session.clear()  # Clear session to reset the chat
    return redirect(url_for('home'))

# Main function to run the Flask app
if __name__ == '__main__':
    Timer(1, open_browser).start()  
    app.run(host='0.0.0.0', port=8080, debug=True)
