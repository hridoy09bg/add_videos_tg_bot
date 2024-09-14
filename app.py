import json
from flask import Flask, request, jsonify, render_template

# File path to the JSON file
json_file = 'videos.json'

# Initialize Flask app
app = Flask(__name__)

# Helper function to load data from the JSON file
def load_data():
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If the file is empty or not found, return an empty structure
        return {"videos": []}

# Helper function to save data to the JSON file
def save_data(data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Route to display the HTML form
@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/add_video', methods=['POST'])
def add_video():
    # Get the data from the form
    name = request.form.get('name')
    videourl = request.form.get('videourl')
    category = request.form.get('category')
    
    # Validate the input
    if not name or not videourl or not category:
        return "All fields are required.", 400

    # Create a new video entry
    new_video = {
        "name": name,
        "videourl": videourl,
        "category": category
    }
    
    # Load the current video data
    data = load_data()

    # Add the new video to the list
    data['videos'].append(new_video)

    # Save the updated data
    save_data(data)

    return f"Video '{name}' added successfully."

# Route to get all videos in JSON format
@app.route('/videos', methods=['GET'])
def get_videos():
    data = load_data()
    return jsonify(data)

# Main block to run the app
if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
