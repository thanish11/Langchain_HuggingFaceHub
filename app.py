from flask import Flask, render_template, request, jsonify
import webbrowser
from threading import Timer
from models import OvarianCancerChatbot  # Assuming you have this class implemented

app = Flask(__name__)

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8080/")

@app.route('/')
def home():
    return render_template('home.html')

# Chat route to handle user input and chatbot interaction
@app.route('/chat', methods=['GET','POST'])
def chat():
    bot = OvarianCancerChatbot()
    
    if request.method == 'POST':
        user_input = request.form.get('query', '').strip().lower()  # Extract user query
        menopause_status = request.form.get('menopause_status', '').strip().lower()
        ca125 = request.form.get('CA125', None)
        he4 = request.form.get('HE4', None)

        # Validate user input
        if not user_input:
            return render_template('chat.html', response="Please provide a valid query.")

        # Validate menopause status
        if menopause_status not in ["premenopause", "postmenopause"]:
            return render_template('chat.html', response="Invalid menopause status. Please provide 'premenopause' or 'postmenopause'.")

        # Validate biomarker levels
        if ca125 is None or he4 is None:
            return render_template('chat.html', response='Please provide CA125 and HE4 levels.')

        # Calculate the ROMA score
        try:
            roma_score = bot.calculate_roma_score(float(ca125), float(he4), menopause_status)
            response_message = f"Your ROMA score is {roma_score:.2f}%."
            
            if roma_score >= 7.4:
                response_message += " High risk of ovarian cancer. Please consult a specialist."
            else:
                response_message += " Low risk, but regular monitoring is recommended."
        except ValueError:
            return render_template('chat.html', response='Invalid input. Please provide numerical values for CA125 and HE4.')

        # Respond to user queries
        response = ""
        if "hospital" in user_input:
            response = bot.query_pdf(bot.hospital_store, user_input)
        elif "diet" in user_input:
            response = bot.query_pdf(bot.diet_store, user_input)
        elif "ovarian" in user_input:
            response = bot.query_pdf(bot.common_store, user_input)
        else:
            response = bot.answer_general_query(user_input)

        return render_template('chat.html', response=response, romascore=response_message)

    return render_template('chat.html')

# Main function to run the Flask app
if __name__ == '__main__':
    Timer(1, open_browser).start()  
    app.run(host='0.0.0.0', port=8080, debug=True)

