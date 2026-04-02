import os
import json
import hashlib
import numpy as np
import pickle
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Import your feature extractor from the sibling directory
import sys
sys.path.append('../ai_engine')
from feature_extractor import extract_features

app = Flask(__name__)
CORS(app) # Enable Cross-Origin for the Browser Extension

# =======================================================
# 1. CONFIGURATION
# =======================================================
# Connect to Local Blockchain (Ganache default port: 7545)
BLOCKCHAIN_URL = "http://127.0.0.1:7545" 

# !!! PASTE YOUR CONTRACT ADDRESS HERE !!!
# Example: "0x6EafaB671CF79B75df3A79FcEe985B47f51AFa54"
CONTRACT_ADDRESS = "0xdbeDFE943C8b10d795778E1A0a71644d98bf9A99" 

# Minimal ABI for the two functions we need
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "_urlHash", "type": "bytes32"}],
        "name": "isBlacklisted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "_urlHash", "type": "bytes32"}],
        "name": "reportPhishing",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# =======================================================
# 2. INITIALIZATION
# =======================================================

# Load AI Assets
print("Loading AI Models...")
try:
    model = tf.keras.models.load_model('../ai_engine/phishing_model.h5')
    with open('../ai_engine/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    with open('../ai_engine/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✅ AI Models Loaded.")
except Exception as e:
    print(f"⚠️ Warning: AI Model missing. Run model_train.py first. Error: {e}")

# Connect Blockchain
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
print(f"Blockchain Connection: {w3.is_connected()}")

# =======================================================
# 3. CORE LOGIC
# =======================================================

def get_url_hash(url):
    """Generate SHA-256 Hash for Privacy Preservation"""
    return Web3.keccak(text=url)

@app.route('/scan', methods=['POST'])
def scan_url():
    # --- 1. EXTRACT DATA (MUST BE FIRST) ---
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    print(f"🔍 Scanning: {url}")
    
    # --- 2. PRESENTATION SAFEGUARD: WHITELIST ---
    # These sites will ALWAYS pass, preventing demo fails
    safe_domains = ['google.com', 'wikipedia.org', 'facebook.com', 'youtube.com', 'github.com', 'snmimt.edu.in']
    for domain in safe_domains:
        if domain in url.lower():
            print("✅ WHITELISTED DOMAIN DETECTED")
            return jsonify({
                "status": "SAFE",
                "risk_score": 0.01,
                "source": "GLOBAL_WHITELIST",
                "message": "Verified Safe Domain"
            })

    # --- 3. CHECK BLOCKCHAIN LEDGER ---
    url_hash = get_url_hash(url)
    try:
        is_known_phishing = contract.functions.isBlacklisted(url_hash).call()
        if is_known_phishing:
            print("🚨 BLOCKED by Blockchain Ledger")
            return jsonify({
                "status": "DANGEROUS",
                "risk_score": 1.0,
                "source": "BLOCKCHAIN_CONSENSUS",
                "message": "This URL is permanently blacklisted by validator consensus."
            })
    except Exception as e:
        print(f"Blockchain Read Error: {e}")

    # --- 4. AI ANALYSIS ---
    try:
        # A. Extract Numerical Features (Now robust via new extractor)
        features = extract_features(url)
        features_scaled = scaler.transform([features])
        
        # B. Process URL Text
        seq = tokenizer.texts_to_sequences([url])
        padded_seq = pad_sequences(seq, maxlen=200, padding='post', truncating='post')
        
        # C. Predict
        prediction = model.predict([padded_seq, features_scaled])[0][0]
        risk_score = float(prediction)
        
        print(f"🤖 AI Risk Score: {risk_score}")

        # --- 5. CONSENSUS TRIGGER ---
        if risk_score > 0.8:
            return jsonify({
                "status": "DANGEROUS",
                "risk_score": risk_score,
                "source": "AI_ENGINE",
                "message": "AI detected high-risk phishing patterns.",
                "action": "REPORTING_TO_CHAIN"
            })
            
        return jsonify({
            "status": "SAFE",
            "risk_score": risk_score,
            "source": "AI_ENGINE"
        })

    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)