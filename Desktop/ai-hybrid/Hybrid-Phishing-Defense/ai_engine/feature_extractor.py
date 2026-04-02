import re
import requests
import numpy as np
import tldextract
from urllib.parse import urlparse

class FeatureExtractor:
    def __init__(self, url):
        self.url = url
        self.domain_info = tldextract.extract(url)
        self.parsed_url = urlparse(url)
        
    def extract_features(self):
        # 1. Initialize a vector of 87 zeros (Standard dataset size)
        # We use a dictionary first to map specific names if we knew them
        # But here we will follow the Standard Kaggle Dataset Order roughly.
        
        features = []

        # --- Group A: Lengths (Usually the first columns) ---
        features.append(len(self.url))                  # length_url
        features.append(len(self.parsed_url.netloc))    # length_hostname
        
        # --- Group B: Binary Flags ---
        try:
            ip_check = 1 if self.parsed_url.netloc and self.parsed_url.netloc[0].isdigit() else 0
        except: ip_check = 0
        features.append(ip_check)                       # ip
        
        # --- Group C: Character Counts (The bulk of the features) ---
        # The standard dataset has them in this specific sequence usually:
        chars_to_count = ['.', '-', '@', '?', '&', '|', '=', '_', '~', '%', '/', '*', ':', ',', ';', '$', ' ']
        for char in chars_to_count:
            features.append(self.url.count(char))

        # --- Group D: Special Tokens ---
        features.append(self.url.lower().count('www'))  # nb_www
        features.append(self.url.lower().count('com'))  # nb_com
        features.append(self.url.count('//'))           # nb_dslash
        
        # --- Group E: Ratios ---
        http_in_path = 1 if 'http' in self.parsed_url.path else 0
        features.append(http_in_path)
        
        https_token = 1 if self.parsed_url.scheme == 'https' else 0
        features.append(https_token)
        
        digits = sum(c.isdigit() for c in self.url)
        ratio = digits / len(self.url) if len(self.url) > 0 else 0
        features.append(ratio)
        
        # --- Group F: Padding ---
        # We have calculated about ~25 features. The model expects 87.
        # We fill the rest with "0" (representing 'unknown' for complex features like PageRank)
        
        current_len = len(features)
        target_len = 87
        
        if current_len < target_len:
            features += [0] * (target_len - current_len)
        elif current_len > target_len:
            features = features[:target_len]
            
        return features

def extract_features(url):
    extractor = FeatureExtractor(url)
    return extractor.extract_features()