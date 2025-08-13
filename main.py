from lib.make_beam_csvfile import create_beam_table_csv, create_beam_table
from lib.defs_beams import def_lin_beams
from lib.defs_beam_sweeping import def_basic_lin_beamsweeping
from lib.defs_beamsweep_op import sequence_ops
import subprocess
from getpass import getpass
import sys
import shutil

HOME_DIR = '/home/user'
OAI_DIR = 'openairinterface5g'
EXECUTABLES_DIR = 'cmake_targets/ran_build/build'
SOFTMODEM_BIN = 'nr-softmodem'
FLEXRIC_DIR = 'openair2/E2AP/flexric'
FLEXRIC_BUILD_DIR = 'build'
XAPP_BEAMMANAGEMENT_BIN = 'xapp_beam_management'
xapp_beam_management_bin_path = f'{HOME_DIR}/{OAI_DIR}/{FLEXRIC_DIR}/{FLEXRIC_BUILD_DIR}/examples/xApp/oaibox/{XAPP_BEAMMANAGEMENT_BIN}'
local_beamtable_csv_location = './CustomBatchBeams.csv'
du_beam_csv_location = f'{HOME_DIR}/{OAI_DIR}/radio/USRP/setup/'

def run_softmodem() -> subprocess.Popen|None:
    privil_password = (getpass() + '\n').encode()
    command = ['sudo', f'{HOME_DIR}/{OAI_DIR}/{EXECUTABLES_DIR}/{SOFTMODEM_BIN}', '...some_args']
    try:
        proc = subprocess.Popen(command, input=privil_password, check=True)
        return proc
    except FileNotFoundError:
        print(f"エラー: コマンド '{command[0]}' が見つかりません。")
        sys.exit(1)
        return None

def kill_softmodem(proc: subprocess.Popen):
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

def main():
    """
    1. beam_listsを作成 list[list[dict[str, int]]]
    2. beam_listsからbs_seqを作成
    3. beam_listsからbeam_tableを作成 list[list[dict[str,str]]]
    4. beam_tableからcsvを作成
    5. csvを再配置
    6. softmodem起動
    7. beamsweepingを実行
    """
    # 1. beam_listsを作成
    origin = {"id": 1, "theta": 0, "phi":45}
    theta_min = 1
    theta_max = 25
    theta_step = 1
    beams_size = (theta_max - theta_min) // theta_step + 1
    beams_lists = [
        def_lin_beams(id_start=2, theta_start=1, theta_end=25, phi_const=0, include_end=True, step=1),
        def_lin_beams(id_start=beams_size+2, theta_start=1, theta_end=25, phi_const=180, include_end=True, step=1),
    ]
    
    # 2. beam_listsからbs_seqを作成
    beam_seq_table = def_basic_lin_beamsweeping(origin, beams_lists)

    # 3. beam_listsからbeam_tableを作成
    beam_table = create_beam_table([origin,] + beams_lists)

    # 4. beam_tableからcsvを作成
    create_beam_table_csv(beam_table, local_beamtable_csv_location)

    # 5. csvを再配置
    shutil.copy(local_beamtable_csv_location, du_beam_csv_location)

    # 6. softmodem起動
    proc = run_softmodem()

    # 7. beamsweepingを実行
    while True:
        try:
            input ("Press Enter to start beam sweeping or Ctrl+C to exit...")
            sequence_ops(beam_seq_table, xapp_beam_management_bin_path, interval=5)
        except KeyboardInterrupt:
            print("中断されました。")
            kill_softmodem(proc)
            break

if __name__ == "__main__":
    main()
