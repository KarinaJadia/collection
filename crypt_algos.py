def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
    
def write_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(data)

def text_to_binary(text):
    return ''.join(f"{ord(c):08b}" for c in text)

def binary_to_text(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def encrypt_binary(binary_str, key):
    # XOR with k1
    # Left shift by k2 bits (modulo 8)
    # XOR with k3
    # Right shift by k4 bits (modulo 8)
    # k1, k2, k3, k4 = key
    k1, k2, k3, k4 = key
    encrypted = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) < 8:
            byte = byte.ljust(8, '0')
        b = int(byte, 2)

        b ^= k1
        b = ((b << k2) | (b >> (8 - k2))) & 0xFF
        b ^= k3
        b = ((b >> k4) | (b << (8 - k4))) & 0xFF

        encrypted += f"{b:08b}"
    return encrypted

def decrypt_binary(encrypted_binary, key):
    k1, k2, k3, k4 = key
    decrypted = ""
    for i in range(0, len(encrypted_binary), 8):
        byte = encrypted_binary[i:i+8]
        if len(byte) < 8:
            byte = byte.ljust(8, '0')
        b = int(byte, 2)

        b = ((b << k4) | (b >> (8 - k4))) & 0xFF
        b ^= k3
        b = ((b >> k2) | (b << (8 - k2))) & 0xFF
        b ^= k1

        decrypted += f"{b:08b}"
    return decrypted

if __name__ == "__main__":
    key = tuple([int(i) for i in input('key: ')])
    original_text = read_file(input('enter file name: '))
    binary_data = text_to_binary(original_text)
    encrypted_binary = encrypt_binary(binary_data, key)
    write_file("encrypted.txt", encrypted_binary)

    encrypted_from_file = read_file("encrypted.txt")
    decrypted_binary = decrypt_binary(encrypted_from_file, key)
    decrypted_text = binary_to_text(decrypted_binary)
    write_file("decrypted.txt", decrypted_text)
    print(decrypted_text)