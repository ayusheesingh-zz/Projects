from Crypto.Cipher import AES
import binascii
import base64

# set 1 challenge 1
## converting hex to base64
def hex_to_64(hex_string):
    # convert hex to binary
    raw_bytes = binascii.unhexlify(hex_string)
    # convert binary to base64
    return base64.b64encode(raw_bytes)

# set 1 challenge 2
## xor two strings
def fixed_xor(s1, s2):
    # converts s1 from hex to bytes
    s1_bytes = bytes.fromhex(s1)
    s2_bytes = bytes.fromhex(s2)
    # xor element by element
    result = bytes([a ^ b for a, b in zip(s1_bytes, s2_bytes)])
    return result.hex()

# set 1 challenge 3
## find what char string has been xor'd with and decrypt the message
def single_xor(s1, key):
    output = b''
    for b in s1:
        output += bytes([b ^ key])
    return output

# find english score using character frequencies
def get_english_score(s1):
    char_freqs = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }

    total = 0
    for elem in s1.lower():
        total += char_freqs.get(chr(elem), 0)

    return total
    
def single_xor_main(s1):
    # convert to bytes if not already
    if (type(s1) != bytes):
        to_encrypt = bytes.fromhex(s1)
    else:
        to_encrypt = s1

    best_message = ""
    best_score = 0
    best_key = ""
    
    for key in range(256):
        message = single_xor(to_encrypt, key)
        score = get_english_score(message)
        if score > best_score:
            best_score = score
            best_message = message
            best_key = chr(key)
    return best_score, best_key, best_message

# set 1 challenge 4
## find the string that's been encrypted by single-char xor
def detect_single_char_xor():
    ciphers = []
    with open ("4.txt") as f:
        for line in f.readlines():
            ciphers.append(bytes.fromhex(line.strip()))

    best_score = 0
    best_key = ""
    best_message = ""
    encrypted_string = ""
    for cipher in ciphers:
        curr_score, curr_key, curr_message = single_xor_main(cipher)
        if curr_score > best_score:
            best_score = curr_score
            best_key = curr_key
            best_message = curr_message
            encrypted_string = cipher
    return best_key, best_message, encrypted_string

# set 1 challenge 5
## encrypt message using repeating-key xor
def repeating_key_xor(plaintext, key):
    ciphertext = b""

    i = 0
    for elem in plaintext:
        ciphertext += bytes([elem ^ key[i]])
        # wraparound index to reuse key elems
        if (i + 1) == len(key):
            i = 0
        else:
            i += 1
    return ciphertext.hex()
    
# set 1 challenge 7
## decrypt message encrypted in AES-128 in ECB mode
def aes():
    key = b"YELLOW SUBMARINE"
    with open ("7.txt") as f:
        ciphertext = base64.b64decode(f.read())
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

# set 1 challenge 8
## counts the number of repetitions in given ciphertext
def count_repetitions(ciphertext):
    block_chunks = []
    for i in range(0, len(ciphertext), 16):
        block_chunks.append(ciphertext[i:i+16])
    num_repetitions = len(block_chunks) - len(set(block_chunks))
    return num_repetitions

## detects which ciphertext has been encrypted by seeing which one has most repetitions
def detect_ecb():
    ciphertext = []
    for line in open("8.txt"):
        ciphertext.append(bytes.fromhex(line.strip()))

    highest_repetitions = 0
    encrypted_message = ""
    for cipher in ciphertext:
        curr_repetitions = count_repetitions(cipher)
        if curr_repetitions > highest_repetitions:
            encrypted_message = cipher
            highest_repetitions = curr_repetitions
    return encrypted_message, highest_repetitions

# print(hex_to_64("1c0111001f010100061a024b53535009181c"))
# print(fixed_xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965"))
# print(single_xor_main("1c0111001f010100061a024b53535009181c"))
# print(detect_single_char_xor())
# print(repeating_key_xor(b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal", b"ICE"))
# print(hammingDistance(b"this is a test", b"wokka wokka!!!"))
# print(calculate_hamming_distance(b"this is a test", b"wokka wokka!!!"))
# print(break_repeating_key_xor())
# print(aes())
# print(detect_ecb())