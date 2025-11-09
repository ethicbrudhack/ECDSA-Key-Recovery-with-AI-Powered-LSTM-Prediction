# 🔐 ECDSA Key Recovery with AI-Powered LSTM Prediction

This Python project demonstrates **ECDSA private key recovery** using **low-s signatures** and a touch of **AI-based prediction** for nonce (`k`) estimation.  
It combines **elliptic curve cryptography (SECP256k1)**, **numerical analysis**, and **deep learning (LSTM)** for an experimental approach to analyzing and recovering cryptographic keys.

---

## 🚀 Features

- Recovers the **ECDSA private key (`d`)** from pairs of low-signed transactions.
- Uses a **TensorFlow LSTM model** to predict likely `k` values (nonces).
- Supports **automatic correction of low-s signatures**.
- Saves recovered keys and results to a JSON-formatted output file.
- Demonstrates **AI-assisted cryptanalysis** in a safe, educational context.

---

## ⚙️ Requirements

Install the necessary Python dependencies using `pip`:

```bash
pip install ecdsa numpy sympy tensorflow
(Optional but recommended for managing dependencies)
Create a virtual environment first:

python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate        # On Windows

🧠 How It Works

Load Transactions
The script contains example ECDSA transactions, each with r, s, and z components.

Recover Private Key (d)
Using two transactions with the same message hash but different signatures,
it computes d by exploiting the mathematical relationship between r, s, and z.

Predict Nonce (k) with LSTM
The AI model (LSTM) is trained on historical k values (if available).
It predicts new candidates for k to accelerate the search process.

Validate Nonce
It checks whether the predicted k correctly regenerates the observed r value.

Save Results
The recovered keys (d and k values) are saved to recovered_keys.txt in JSON format.

🧩 File Structure
📂 ecdsa_ai_recovery/
 ├── main.py               # The main script (this file)
 ├── recovered_keys.txt    # Output file with recovered values
 ├── requirements.txt      # Dependencies (optional)
 └── README.md             # Documentation (this file)

▶️ How to Run

Run the script directly:

python main.py


Example output:

❌ Nie można odzyskać `d` - wartości `z` są identyczne!
🎯 Znaleziono klucz prywatny! d = 0x123abc...
🔑 Znaleziono `k`! k = 847239123...
✅ Wyniki zapisane w recovered_keys.txt

⚠️ Disclaimer

This project is intended solely for educational and research purposes.
Do not use this code for unauthorized access, exploitation, or recovery of private keys
belonging to others. Misuse may be illegal and unethical.

🧑‍💻 Author

AI-Enhanced ECDSA Recovery Example
Created for cryptography enthusiasts exploring intersections between machine learning and blockchain security.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
