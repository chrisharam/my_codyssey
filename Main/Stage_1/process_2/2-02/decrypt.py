# decrypt.py

PASSWORD_FILE = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-01/password.txt"
RESULT_FILE = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-02/result.txt"

def caesar_cipher_decode(target_txt):
    """모든 시프트로 해독 결과 출력"""
    print('Trying Caesar cipher decoding with all 26 shifts:\n')
    for shift in range(26):
        decoded_txt = ''
        for char in target_txt:
            if 'a' <= char <= 'z':
                decoded_txt += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded_txt += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded_txt += char
        print(f'Shift {shift:2}: {decoded_txt}')

def main():
    # password.txt 파일 읽기
    try:
        with open(PASSWORD_FILE, "r") as f:
            cipher_text = f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] Cannot find {PASSWORD_FILE}")
        return

    # Caesar cipher 해독 시도 및 출력
    caesar_cipher_decode(cipher_text)

    # 사용자 입력: 몇 번째 자리수로 암호를 해독했는지
    while True:
        shift_input = input("\nEnter the shift number that gives the correct decoding: ")
        try:
            shift_num = int(shift_input)
            if 0 <= shift_num <= 25:
                break
            else:
                print("[ERROR] Shift number must be between 0 and 25.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")

    # 선택한 shift로 최종 결과 생성
    result_txt = ''
    for char in cipher_text:
        if 'a' <= char <= 'z':
            result_txt += chr((ord(char) - ord('a') - shift_num) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            result_txt += chr((ord(char) - ord('A') - shift_num) % 26 + ord('A'))
        else:
            result_txt += char

    # result.txt에 저장
    with open(RESULT_FILE, "w") as f:
        f.write(result_txt)

    print(f"[SUCCESS] Decoded text saved to {RESULT_FILE}")
    print(f"Shift used: {shift_num}")
    print(f"Decoded text: {result_txt}")

if __name__ == "__main__":
    main()
