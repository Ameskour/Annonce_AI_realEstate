from flask import Flask, render_template, request, jsonify
import openai
from questions import questions  # import the questions dictionary

# Set up your OpenAI API credentials
openai.api_key = 'OPENAI_API_KEY'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user input, previous answers, and current state from the request
    user_input = request.json.get('user_input', '')
    previous_answers = request.json.get('previous_answers', {})
    current_state = request.json.get('current_state', 'description')

    previous_answers[current_state] = user_input  # Save user's response

    # Determine the next state based on the current state and user input
    if current_state == "description": 
        current_state = "Tonalite_de_l_annonce"
        
    elif current_state == "Tonalite_de_l_annonce":
        current_state = "Longueur_de_lannonce"
        
    elif current_state == "Longueur_de_lannonce":
        ad_prompt = previous_answers
        ad_message = create_advertisement(ad_prompt)
        return jsonify({'question': "" + ad_message, 'previous_answers': previous_answers})

    else:
        return None 
    
    return jsonify({'question': questions[current_state]['question'], 
                    'previous_answers': previous_answers, 
                    'next_state': current_state})

def create_advertisement(ad_prompt):
    # Create a string by joining the non-empty values from the prompt
    # By iterating over the items in the ad_prompt dictionary, we maintain the order of the responses as they are received
    ad_prompt_string = ', '.join([f"{key.capitalize()}: {value}" for key, value in ad_prompt.items() if value.strip()])
    try:
        # Generate an advertisement using the OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a real estate agent creating an advertisement for a property , generate the ad in French with {ad_prompt['Tonalite_de_l_annonce']} tone and length of {ad_prompt['Longueur_de_lannonce']}. Write a compelling description using only the characteristiques in the user's description that highlights the unique features and selling points of the property."},
                {"role": "user", "content": ad_prompt_string}
            ]
        )

    except openai.error.RateLimitError:
        print("Rate limit exceeded. Please wait before making more requests.")
        return "Rate limit exceeded. Please wait before making more requests."

    message = response.choices[0].message['content'].strip()
    return message

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
