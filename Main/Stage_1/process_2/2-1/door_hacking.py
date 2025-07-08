import time
import string
import zipfile
import itertools

def unlock_zip():
    start_time = time.time()
    attempts = 0
    pass_found = False

    candidate = string.ascii_lowercase + string.digits
    zip_path = '/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey-1/Main/Stage_1/process_2/1-1/emergency_storage_key.zip'

    try:
        locked_file = zipfile.ZipFile(zip_path)
    except FileNotFoundError:
        print("Can't find the zipped file.")
        return
    except zipfile.BadZipFile:
        print("Wrong zip file structure.")
        return

    print("Start decryption")
    print("Start time:", time.strftime('%Y-%m-%d %H:%M:%S'))

    for pwd_tuple in itertools.product(candidate, repeat=6):
        pwd = ''.join(pwd_tuple)
        attempts += 1

        try:
            locked_file.extractall(pwd=bytes(pwd, 'utf-8'))
            print('Successful decryption.')
            print('Password:', pwd)
            print('Total attempts:', attempts)
            process_time = time.time() - start_time
            print('Time taken to complete the task: {:.2f} seconds'.format(process_time))

            with open('/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey-1/Main/Stage_1/process_2/2-1/password.txt', 'w') as f:
                f.write(pwd)
            pass_found = True
            break
        except RuntimeError:
            #When trying to decrypt pwd and fail, it passes.
            pass
        except Exception as e:
            msg = str(e)
            if ('Error -3 while decompressing data' in msg) or ('Bad CRC-32' in msg):
                #ignore wrong pwd
                pass
            else:
                print(f"Unexpected error occurred: {e}")
                break

        if attempts % 1000 == 0:
            process_time = time.time() - start_time
            print(f"Attempts: {attempts}, Processing time: {process_time:.2f} seconds")

    if not pass_found:
        print("❌ Password not found.")

if __name__ == '__main__':
    unlock_zip()
