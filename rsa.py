import streamlit as st
import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def xgcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0

    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y


def chooseE(totient):
    while True:
        e = random.randrange(2, totient)
        if gcd(e, totient) == 1:
            return e


def chooseKeys():
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    fo = open('primes-to-100k.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    gcd, x, y = xgcd(e, totient)

    if x < 0:
        d = x + totient
    else:
        d = x

    f_public = open('public_keys.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()


def chooseE(totient):
    while True:
        e = random.randrange(2, totient)
        if gcd(e, totient) == 1:
            return e

def chooseKeys():
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    fo = open('primes-to-100k.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    gcd, x, y = xgcd(e, totient)

    if x < 0:
        d = x + totient
    else:
        d = x

    f_public = open('public_keys.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()

    return n, e, d


def encrypt(message, file_name='public_keys.txt', block_size=2):
    try:
        fo = open(file_name, 'r')
    except FileNotFoundError:
        st.write('Le fichier n\'a pas été trouvé.')
        return None

    n = int(fo.readline())
    e = int(fo.readline())
    fo.close()

    encrypted_blocks = []
    ciphertext = -1

    if len(message) > 0:
        ciphertext = ord(message[0])

    for i in range(1, len(message)):
        if i % block_size == 0:
            encrypted_blocks.append(ciphertext)
            ciphertext = 0
        ciphertext = ciphertext * 1000 + ord(message[i])

    encrypted_blocks.append(ciphertext)

    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str((encrypted_blocks[i] ** e) % n)

    encrypted_message = " ".join(encrypted_blocks)

    return encrypted_message


def decrypt(blocks, block_size=2):
    fo = open('private_keys.txt', 'r')
    n = int(fo.readline())
    d = int(fo.readline())
    fo.close()

    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    for i in range(len(int_blocks)):
        int_blocks[i] = (int_blocks[i] ** d) % n

        tmp = ""
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000
        message += tmp

    return message


st.title("Programme RSA")

option = st.sidebar.radio("Choisissez une option",
                          ("Générer les clés RSA", "Crypter un message", "Décrypter un message"))

if option == "Générer les clés RSA":
    if st.button("Générer les clés"):
        chooseKeys()
        st.write("Clés générées avec succès.")
        n, e, d = chooseKeys()
        st.write("Clés générées avec succès.")
        st.write("Clé publique (n, e):")
        st.write(f"n: {n}")
        st.write(f"e: {e}")
        st.write("Clé privée (n, d):")
        st.write(f"n: {n}")
        st.write(f"d: {d}")

elif option == "Crypter un message":
    message = st.text_input("Entrez le message à crypter")
    own_keys = st.checkbox("Utiliser vos propres clés")

    if own_keys:
        if st.button("Crypter"):
            encrypted_message = encrypt(message)
            if encrypted_message:
                st.write("Message chiffré :")
                st.code(encrypted_message)
    else:
        public_key_file = st.file_uploader("Sélectionner le fichier de clé publique")
        if public_key_file is not None and st.button("Crypter"):
            public_key_content = public_key_file.read().decode("utf-8")
            encrypted_message = encrypt(message, public_key_content)
            if encrypted_message:
                st.write("Message chiffré :")
                st.code(encrypted_message)

elif option == "Décrypter un message":
    ciphertext = st.text_input("Entrez le message chiffré")
    if st.button("Décrypter"):
        decrypted_message = decrypt(ciphertext)
        st.write("Message décrypté :")
        st.code(decrypted_message)
