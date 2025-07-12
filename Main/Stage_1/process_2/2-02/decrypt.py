def caesar_cipher_decode(target_txt):
    print('Trying Caesar cipher decoding with all 26 shifts: \n')

    for shift in range(26):
        decoded_txt = ''
        for char in target_txt:
            if 'a' <= char <='z':
                                # 구하려는 값    # 초기값     #밀린 자릿수
                decoded_txt += chr((ord(char) - ord('a')-shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded_txt += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded_txt += char  # non-alphabet characters remain unchanged
            print(f'Shift {shift:2}: {decoded_txt}')
