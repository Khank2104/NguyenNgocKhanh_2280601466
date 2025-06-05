from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayFairCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

caesar_cipher = CaesarCipher()
playfair_cipher = PlayFairCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
transposition_cipher = TranspositionCipher()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return render_template('caesar.html', encrypted_text=encrypted_text)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return render_template('caesar.html', decrypted_text=decrypted_text)

@app.route('/playfair')
def playfair_page():
    return render_template('playfair.html')

@app.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    plain_text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, matrix)
    return render_template('playfair.html', encrypted_text=encrypted_text)

@app.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    cipher_text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, matrix)
    return render_template('playfair.html', decrypted_text=decrypted_text)
@app.route("/vigenere")
def vigenere_page():
    return render_template("vigenere.html")

@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt_route():
    text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]
    encrypted_text = vigenere_cipher.vigenere_encrypt(text, key)
    return render_template("vigenere.html", encrypted_text=encrypted_text)

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt_route():
    text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]
    decrypted_text = vigenere_cipher.vigenere_decrypt(text, key)
    return render_template("vigenere.html", decrypted_text=decrypted_text)

@app.route('/railfence')
def railfence_page():
    return render_template('railfence.html')

@app.route('/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    plain_text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return render_template('railfence.html', encrypted_text=encrypted_text)

@app.route('/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    cipher_text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return render_template('railfence.html', decrypted_text=decrypted_text)

@app.route('/transposition')
def transposition_page():
    return render_template('transposition.html')

@app.route('/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    plain_text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return render_template('transposition.html', encrypted_text=encrypted_text)

@app.route('/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    cipher_text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return render_template('transposition.html', decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
