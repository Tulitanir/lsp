import cv2
import random

def text_to_binary(text):
    byte_array = text.encode("utf-8")

    binary_text = "".join(format(byte, "08b") for byte in byte_array)
    return binary_text

def binary_to_text(binary_text):
    byte_array = bytearray(int(binary_text[i:i+8], 2) for i in range(0, len(binary_text), 8))
    decoded_text = byte_array.decode("utf-8")
    
    return decoded_text

def encode_lsb(image_path, output_path, secret_text, seed=404):
    random.seed(seed)

    img = cv2.imread(image_path)

    image_size = img.shape[0] * img.shape[1] * img.shape[2] // 2
    text_binary = text_to_binary(secret_text)
    message_length = len(text_binary)

    if message_length + 16 > image_size:  # Учитываем 16 бит для хранения длины сообщения
        raise ValueError("Секретное сообщение слишком велико для данного контейнера (изображения)")

    secret_text = format(message_length, "016b") + text_binary
    pixels = random.sample(range(image_size), message_length + 16)

    for i, pixel_index in enumerate(pixels):
        row = pixel_index // (img.shape[1] * img.shape[2])
        col = (pixel_index % (img.shape[1] * img.shape[2])) // img.shape[2]
        channel = pixel_index % img.shape[2]
        img[row][col][channel] = img[row][col][channel] & 254 | int(secret_text[i])

    cv2.imwrite(output_path, img)

    print("Текст успешно закодирован в изображение")

def decode_lsb(image_path, seed=404):
    random.seed(seed)

    img = cv2.imread(image_path)
    image_size = img.shape[0] * img.shape[1] * img.shape[2] // 2

    pixels = random.sample(range(image_size), 16)

    binary_length = ""
    for pixel_index in pixels:
        row = pixel_index // (img.shape[1] * img.shape[2])
        col = (pixel_index % (img.shape[1] * img.shape[2])) // img.shape[2]
        channel = pixel_index % img.shape[2]
        binary_length += str(img[row][col][channel] & 1)

    message_length = int(binary_length, 2)

    binary_text = ""
    random.seed(seed)
    pixels = random.sample(range(image_size), message_length + 16)

    for i, pixel_index in enumerate(pixels):
        if i < 16:
            continue

        row = pixel_index // (img.shape[1] * img.shape[2])
        col = (pixel_index % (img.shape[1] * img.shape[2])) // img.shape[2]
        channel = pixel_index % img.shape[2]
        binary_text += str(img[row][col][channel] & 1)
    return binary_to_text(binary_text)

encode_lsb("test/images.jpg", "test/output.png",
        """
大胆不敵にハイカラ革命
磊々落々らいらいらくらく反戦国家
日の丸印の二輪車転がし
悪霊退散　ICBM

環状線を走り抜けて
東奔西走なんのその
少年少女戦国無双
浮世の随まにまに

千本桜　夜ニ紛レ
君ノ声モ届カナイヨ
此処は宴　鋼の檻
その断頭台で見下ろして
三千世界　常世之闇とこよのやみ
嘆ク唄モ聞コエナイヨ
青藍せいらんの空　遥か彼方
その光線銃で打ち抜いて

百戦錬磨の見た目は将校
いったりきたりの花魁おいらん道中
アイツもコイツも皆で集まれ
聖者の行進　わんっ　つー　さん　しっ

禅定門ぜんじょうもんを潜り抜けて
安楽浄土厄払い
きっと終幕さいごは大団円
拍手の合間に

千本桜　夜ニ紛レ
君ノ声モ届カナイヨ
此処は宴　鋼の檻
その断頭台で見下ろして
三千世界　常世之闇とこよのやみ
嘆ク唄モ聞コエナイヨ
希望の丘　遥か彼方
その閃光弾を打ち上げろ

環状線を走り抜けて
東奔西走なんのその
少年少女戦国無双
浮世の随まにまに

千本桜　夜ニ紛レ
君ノ声モ届カナイヨ
此処は宴　鋼の檻
その断頭台を飛び降りて

千本桜　夜ニ紛レ
君が歌い僕は踊る
此処は宴　鋼の檻
さあ光線銃を撃ちまくれ
        """
)
print(decode_lsb("test/output.png"))