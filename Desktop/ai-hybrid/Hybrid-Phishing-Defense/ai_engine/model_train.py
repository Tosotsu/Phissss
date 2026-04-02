import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, MaxPooling1D, LSTM, Dense, Concatenate, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ===========================
# 1. Configuration
# ===========================
# Ensure dataset_phishing.csv is in the same folder!
DATA_PATH = 'dataset_phishing.csv' 
MODEL_SAVE_PATH = 'phishing_model.h5'
TOKENIZER_SAVE_PATH = 'tokenizer.pkl'
SCALER_SAVE_PATH = 'scaler.pkl'

# Architecture Constants (MUST match Backend)
MAX_URL_LEN = 200       
VOCAB_SIZE = 5000       # Increased for better accuracy
EMBEDDING_DIM = 50
BATCH_SIZE = 32
EPOCHS = 20

def train_professional_model():
    if not os.path.exists(DATA_PATH):
        print(f"❌ ERROR: {DATA_PATH} not found!")
        print("Please download the dataset and place it in the 'ai_engine' folder.")
        return

    print("📊 Loading and processing data...")
    df = pd.read_csv(DATA_PATH)
    
    # --- A. Preprocess Labels ---
    # Convert 'legitimate'/'phishing' text to 0/1
    le = LabelEncoder()
    df['target'] = le.fit_transform(df['status']) 
    y = df['target'].values
    print(f"Classes found: {le.classes_}") # Should be ['legitimate' 'phishing']

    # --- B. Preprocess URL Text (Deep Learning Branch) ---
    url_data = df['url'].astype(str).values
    
    # Train Tokenizer on REAL URLs
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, char_level=True, oov_token='<OOV>')
    tokenizer.fit_on_texts(url_data)
    
    sequences = tokenizer.texts_to_sequences(url_data)
    X_urls = pad_sequences(sequences, maxlen=MAX_URL_LEN, padding='post', truncating='post')
    
    # --- C. Preprocess 89 Features (Statistical Branch) ---
    # Drop non-numeric columns to isolate the 89 features
    feature_cols = df.drop(['url', 'status', 'target'], axis=1)
    
    # Normalize features (Crucial for Neural Networks)
    scaler = StandardScaler()
    X_features = scaler.fit_transform(feature_cols.values)
    
    print(f"Training on {len(df)} samples...")
    print(f"Features Shape: {X_features.shape}") # Should be (11430, 89)

    # --- D. Save the Processors for Backend ---
    # The backend NEEDS these exact processors to understand new data
    with open(TOKENIZER_SAVE_PATH, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open(SCALER_SAVE_PATH, 'wb') as handle:
        pickle.dump(scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("✅ Tokenizer and Scaler saved.")

    # --- E. Split Data ---
    X_url_train, X_url_test, X_feat_train, X_feat_test, y_train, y_test = train_test_split(
        X_urls, X_features, y, test_size=0.2, random_state=42
    )

    # --- F. Build the Hybrid Architecture ---
    
    # Branch 1: CNN-LSTM for Text
    url_input = Input(shape=(MAX_URL_LEN,), name='url_input')
    x1 = Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM)(url_input)
    x1 = Conv1D(filters=64, kernel_size=3, activation='relu')(x1)
    x1 = MaxPooling1D(pool_size=2)(x1)
    x1 = LSTM(64, return_sequences=False)(x1)
    
    # Branch 2: Dense Network for Features
    feature_input = Input(shape=(X_features.shape[1],), name='feature_input')
    x2 = Dense(128, activation='relu')(feature_input)
    x2 = Dropout(0.3)(x2)
    x2 = Dense(64, activation='relu')(x2)
    
    # Fusion
    merged = Concatenate()([x1, x2])
    z = Dense(64, activation='relu')(merged)
    z = Dropout(0.5)(z)
    output = Dense(1, activation='sigmoid', name='output')(z)
    
    model = Model(inputs=[url_input, feature_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # --- G. Train ---
    print("🚀 Starting Professional Training...")
    
    # Stop training if it stops improving (prevents Overfitting)
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    
    history = model.fit(
        [X_url_train, X_feat_train], y_train,
        validation_data=([X_url_test, X_feat_test], y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stop]
    )
    
    # --- H. Save Model ---
    loss, accuracy = model.evaluate([X_url_test, X_feat_test], y_test)
    print(f"\n🏆 Final Test Accuracy: {accuracy*100:.2f}%")
    
    model.save(MODEL_SAVE_PATH)
    print(f"✅ Professional Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_professional_model()