import subprocess
from sys import exit
from getpass import getpass

def run_softmodem(host:str, bin_path:str) -> subprocess.Popen|None:
    privileged_password = getpass()
    privileged_password if privileged_password else ""
    command = ['sudo', '-S', bin_path, '...some_args']
    try:
        # proc = subprocess.Popen(command, input=privileged_password, check=True, text=True)
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.stdin is not None:
            try:
                proc.stdin.write(privileged_password)
                proc.stdin.close()
            except Exception as e:
                print(f"Error occurred while writing to stdin: {e}")
        else:
            proc.kill()  # stdinがNoneの場合はプロセスを終了
            raise RuntimeError("Process was not initialized properly")
        return proc
    except FileNotFoundError:
        print(f"エラー: コマンド '{command[0]}' が見つかりません。")
        exit(1)
        return None

def kill_softmodem(proc: subprocess.Popen|None) -> None:
    if proc is None:
        return
    if proc.poll() is None:
        # 1. 穏便な終了を試みる
        proc.terminate()
        try:
            # 2. 終了するのを最大10秒間待つ
            return_code = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            # 3. terminateで終了しなかった場合、強制終了する
            print("サブプロセスが終了しませんでした。強制終了します。")
            proc.kill()
            return_code = proc.wait() # 強制終了後、待機してリソースを解放
            print(f"サブプロセスを強制終了しました。リターンコード: {return_code}")
    else:
        pass  # 既に終了している場合は何もしない