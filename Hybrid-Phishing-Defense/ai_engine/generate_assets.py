import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate
from tensorflow.keras.initializers import Constant
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.preprocessing.text import Tokenizer

def create_smart_dummy_assets():
    print("🛠️ Generating Smart AI Assets...")
    
    # --- 1. Create a "Safe-Biased" Model ---
    # We use random weights, but we force the final decision (Bias) to be negative.
    # This ensures the model defaults to "Safe" unless it sees something very specific.
    
    url_input = Input(shape=(200,), name='url_input') 
    feature_input = Input(shape=(89,), name='feature_input') 
    
    # Use small random weights so inputs don't explode
    x1 = Dense(8, kernel_initializer='glorot_uniform')(url_input)
    x2 = Dense(8, kernel_initializer='glorot_uniform')(feature_input)
    
    merged = Concatenate()([x1, x2])
    
    # KEY FIX: bias_initializer=Constant(-5.0)
    # This pushes the sigmoid output towards 0 (Safe) by default.
    output = Dense(1, activation='sigmoid', bias_initializer=Constant(-5.0), name='output')(merged)
    
    model = Model(inputs=[url_input, feature_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    
    model.save('phishing_model.h5')
    print("✅ Model saved (Biased for Safety).")

    # --- 2. Create a Tokenizer ---
    tokenizer = Tokenizer(num_words=1000, char_level=True, oov_token='<OOV>')
    # Fit on some dummy text to initialize the internal map
    tokenizer.fit_on_texts(['https://www.google.com', 'http://phishing-site.net/login'])
    with open('tokenizer.pkl', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("✅ Tokenizer saved.")

    # --- 3. Create a Realistic Scaler ---
    scaler = StandardScaler()
    # KEY FIX: Fit on RANDOM numbers (0-100) instead of Zeros.
    # This prevents the "Exploding Input" bug when real URL lengths are fed in.
    dummy_data = np.random.rand(50, 89) * 100 
    scaler.fit(dummy_data)
    
    with open('scaler.pkl', 'wb') as handle:
        pickle.dump(scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("✅ Scaler saved (Realistic Range).")

if __name__ == "__main__":
    create_smart_dummy_assets()