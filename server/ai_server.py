import io
import torch
import clip
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

# Assign the network engine device dynamically based on runtime availability
device = "cuda" if torch.cuda.is_available() else "cpu"
model = None
preprocess = None

def load_model():
    """Loads the CLIP model into memory once when the server starts."""
    global model, preprocess
    print(f"[Server] Loading CLIP model (ViT-B/32) onto device: {device}...")
    
    # Load the specific ViT-B/32 model requested by your mentor
    model, preprocess = clip.load("ViT-B/32", device=device)
    model.eval()  # Configure the model context explicitly for inference evaluation
    print("[Server] Model loaded successfully and ready for incoming traffic.")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint that receives an image and candidate text labels,
    runs CLIP inference, and returns the highest matching label.
    """
    # Guard clause: Ensure the multi-part request payload contains an image file
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    # Guard clause: Ensure labels exist to map visual data against
    labels_raw = request.form.get("labels", "")
    if not labels_raw:
        return jsonify({"error": "No labels provided"}), 400
    
    # Standardize string inputs to eliminate white-space variances
    labels = [label.strip() for label in labels_raw.split(",")]

    try:
        image_file = request.files['image']
        image_bytes = image_file.read()
        
        # Verify binary stream image wrapper integrity before processing tensors
        img_stream = io.BytesIO(image_bytes)
        image = Image.open(img_stream)
        image.verify()  
        
        # Reset byte pointer position to zero after structural verification pass
        img_stream.seek(0)
        image = Image.open(img_stream).convert("RGB")

        # Standardize structural shapes via CLIP preprocessor pipeline
        image_input = preprocess(image).unsqueeze(0).to(device)
        text_inputs = clip.tokenize(labels).to(device)

        # Execute evaluation loop isolated from computational gradient tracking
        with torch.no_grad():
            logits_per_image, _ = model(image_input, text_inputs)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

        # Process prediction vector results
        best_match_idx = probs.argmax()
        prediction = labels[best_match_idx]
        confidence = float(probs[best_match_idx])

        return jsonify({
            "status": "success",
            "prediction": prediction,
            "confidence": confidence
        })

    except Exception as e:
        # Stream down structural error details back to the client environment for logging
        return jsonify({"error": f"Inference failed: {str(e)}"}), 500

if __name__ == "__main__":
    # Ensure dependencies load completely before launching interface handlers
    load_model()
    # Bind server internally to port 5000 
    app.run(host="0.0.0.0", port=5000, debug=False)
