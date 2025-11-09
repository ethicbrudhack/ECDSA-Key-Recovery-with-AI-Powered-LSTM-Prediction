import ecdsa
import numpy as np
import random
import json
from sympy import mod_inverse
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 🔹 Konfiguracja ECDSA
n = ecdsa.SECP256k1.order
G = ecdsa.SECP256k1.generator

# 🔹 Wczytujemy dane historyczne `k`
historical_k = []

# 🔹 Lista transakcji (przykładowe podpisy low-s)
transactions = [
    {"r": 0x632e34fc9ef7829c3da931caf40baa643e85f85b950dd54c8c1b1dde49e47c0b,
     "s": 0x2ffa9209f934de2fdaf21d55571e42a0da47665c9ab10a86c97dacc62a9b01bd,
     "z": 0xbeb21d89f2ebdc645094135d999aa79d386711a6a5f0289eba893c5515a4856f},

    {"r": 0x8ca2698b53fffcf9d064b1ca1313ff08e08e47d3bbb97a4f9d54dd0e3164af9a,
     "s": 0x65913d2b007ebedf451e0068b368a33ff0fdb9725370a8cecc34e2e8449f143c,
     "z": 0xbeb21d89f2ebdc645094135d999aa79d386711a6a5f0289eba893c5515a4856f},

    {"r": 0xefe66ff0cc452d2dc373db4cf2fa848944e32dbfac6c46542d2ed03a22cbb081,
     "s": 0x1726f4b1dc28ca118aea9d6a4fc7f9345c6cb071b7cbd95b22456c45539cb5fa,
     "z": 0xbeb21d89f2ebdc645094135d999aa79d386711a6a5f0289eba893c5515a4856f},

    {"r": 0x1e68b7d13178cd65061c2bb57623efb2f99be1577465a2ec0532f697113e4e34,
     "s": 0x16779876223604f100c9e444feea939aa828928dd2a67ca4a2ac1afe1edfa310,
     "z": 0xbeb21d89f2ebdc645094135d999aa79d386711a6a5f0289eba893c5515a4856f}
]

# 🔹 AI: Model LSTM do przewidywania `k`
def train_lstm_model(k_values):
    if len(k_values) < 5:
        return None  

    X_train = np.array(k_values[:-1]).reshape(-1, 5, 1)
    y_train = np.array(k_values[1:])

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(5, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=10, verbose=0)

    return model

def predict_k_lstm(model, k_values):
    X_input = np.array(k_values[-5:]).reshape(1, 5, 1)
    return int(model.predict(X_input)[0][0]) % n

# 🔹 Odzyskiwanie `d` z `low-s`
def recover_d_from_low_s(tx1, tx2, n):
    r1, s1, z1 = tx1["r"], tx1["s"], tx1["z"]
    r2, s2, z2 = tx2["r"], tx2["s"], tx2["z"]

    # Jeśli z1 == z2, klucz prywatny nie może być odzyskany
    if z1 == z2:
        print("❌ Nie można odzyskać `d` - wartości `z` są identyczne!")
        return None

    # Korekcja `low-s`
    if s1 > n // 2:
        s1 = n - s1
    if s2 > n // 2:
        s2 = n - s2

    try:
        # Sprawdzamy, czy s1 - s2 ≠ 0
        delta_s = (s1 - s2) % n
        if delta_s == 0:
            print("❌ Nie można odzyskać `d` - `s1 - s2 = 0`!")
            return None

        d = ((z1 - z2) * mod_inverse(delta_s, n)) % n
        print(f"🎯 Znaleziono klucz prywatny! d = {hex(d)}")
        return d

    except ValueError:
        print("❌ Nie udało się odzyskać `d` - błąd `mod_inverse`")
        return None

# 🔹 Inteligentne dopasowanie `k`
def recover_k(d, tx):
    r, s, z = tx["r"], tx["s"], tx["z"]

    # Korekcja `low-s`
    if s > n // 2:
        s = n - s

    # Model AI do przewidywania `k`
    lstm_model = train_lstm_model(historical_k)

    # Przewidywanie `k`
    if lstm_model:
        k_pred = predict_k_lstm(lstm_model, historical_k)
    else:
        k_pred = random.randint(1, n - 1)  # Awaryjne losowanie

    # Szukamy `k`, które pasuje do `r`
    for _ in range(1000):  # Inteligentne iteracje
        R = k_pred * G
        if R.x() % n == r:
            print(f"🔑 Znaleziono `k`! k = {k_pred}")
            return k_pred
        k_pred = (k_pred + 1) % n  

    print("❌ Nie znaleziono `k`")
    return None

# 🔹 Zapisywanie wyników do pliku
def save_results(d, k_values):
    result_data = {
        "d": d,
        "k_values": k_values
    }
    with open("recovered_keys.txt", "w") as f:
        json.dump(result_data, f, indent=4)
    print("✅ Wyniki zapisane w recovered_keys.txt")

# 🔹 Uruchamianie procesu
d = recover_d_from_low_s(transactions[0], transactions[1], n)

if d:
    recovered_ks = []
    for tx in transactions:
        k_found = recover_k(d, tx)
        if k_found:
            recovered_ks.append(k_found)

    save_results(d, recovered_ks)