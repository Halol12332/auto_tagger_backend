from flask import Flask, request, jsonify
from flask_cors import CORS
from processor import process_image

app = Flask(__name__)
# Security: Restricted to Next.js default port during dev
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://project-d2coy.vercel.app"]
    }
})
@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    image_bytes = file.read()
    
    try:
        data, encoded_image = process_image(image_bytes)
        
        if data is None:
            return jsonify({"error": "No recognizable objects found"}), 404

        return jsonify({
            "title": f"Japanese-style {data['label']}".title(),
            "category": data['label'],
            "all_categories": data['all_labels'],
            "confidence": round(data['confidence'], 2),
            # CHANGE THIS LINE from jpeg to png:
            "image_data": f"data:image/png;base64,{encoded_image}" 
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# @app.route('/')
# def health_check():
#     return "Backend is running!", 200

@app.route('/', methods=['GET'])
def health_check():
    return "Tsunagu AI Backend is Live!", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
