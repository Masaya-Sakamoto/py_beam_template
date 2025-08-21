from lib.make_beam_file import create_beam_table_csv, create_beam_table_csv_data
from lib.defs_beams import def_lin_beams, def_basic_fibonacci_beams
from lib.defs_beam_sweeping import def_lin_beam_sweeping
from lib.defs_beam_sweep_op import sequence_ops
from tools.arg_parser import arg_parser
import subprocess
from getpass import getpass
import sys
import shutil
from typing import Any

# HOME_DIR = '/home/user'
# OAI_DIR = 'openairinterface5g'
# EXECUTABLES_DIR = 'cmake_targets/ran_build/build'
# SOFTMODEM_BIN = 'nr-softmodem'
# FLEXRIC_DIR = 'openair2/E2AP/flexric'
# FLEXRIC_BUILD_DIR = 'build'
# XAPP_BEAMMANAGEMENT_BIN = 'oaibox_xapp_beam_management'
# xapp_beam_management_bin_path = f'{HOME_DIR}/{OAI_DIR}/{FLEXRIC_DIR}/{FLEXRIC_BUILD_DIR}/examples/xApp/oaibox/{XAPP_BEAMMANAGEMENT_BIN}'
# local_beam_table_csv_location = './CustomBatchBeams.csv'
# du_beam_csv_location = f'{HOME_DIR}/{OAI_DIR}/radio/USRP/setup/'
# beam_switch_interval = 20

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
        sys.exit(1)
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



def main(args):
    """
    1. beam_listsを作成 list[list[dict[str, int]]]
    2. beam_listsからbs_seqを作成
    3. beam_listsからbeam_tableを作成 list[list[dict[str,str]]]
    4. beam_tableからcsvを作成
    5. csvを再配置
    6. softmodem起動
    7. beam-sweepingを実行
    """
    beams_lists = []
    if args['beam_pattern'] == "linear":
        # 1. beam_listsを作成
        origin = {"id": 1, "theta": 0, "phi":0}
        theta_min = args['theta_min']
        theta_max = args['theta_max']
        theta_step = args['theta_step']
        pattern_rotation = args['pattern_rotation']
        beams_size = (theta_max - theta_min) // theta_step + 1
        beams_lists.append(def_lin_beams(
            id_start=2,
            theta_start=theta_min,
            theta_end=theta_max,
            pattern_rotation=pattern_rotation,
            include_end=True,
            step=theta_step))
        beams_lists.append(def_lin_beams(
            id_start=beams_size+2,
            theta_start=theta_min,
            theta_end=theta_max,
            pattern_rotation=(pattern_rotation+180)%360,
            include_end=True,
            step=theta_step))

        # 2. beam_listsからbs_seqを作成
        
        # 3. beam_listsからbeam_tableを作成
        beam_table = create_beam_table_csv_data([origin,] + beams_lists[0] + beams_lists[1])
    elif args['beam_pattern'] == "fibonacci":
        beams_lists.append(def_basic_fibonacci_beams(
            N = 64,
            delta=0.0,
            theta_max=args['theta_max'],
            pattern_rotation=args['pattern_rotation'],
        ))
        beam_table = create_beam_table_csv_data(beams_lists[0])

    else:
        raise ValueError(f"Unsupported beam pattern: {args['beam_pattern']}")
    
    if args['beam_pattern'] == "linear":
        # beam_seq_table = def_basic_lin_beams_weeping(origin, beams_lists)
        # beam_seq_tables = [def_lin_beam_sweeping(origin, beams) for beams in beams_lists]
        # TODO: beam_seq_tablesと実行部分をidで参照するように変更する
        

    

    # 4. beam_tableからcsvを作成
    create_beam_table_csv(beam_table, local_beam_table_csv_location)

    # 5. csvを再配置
    shutil.copy(local_beam_table_csv_location, du_beam_csv_location)

    # 6. softmodem起動
    proc = run_softmodem()

    # 7. beam-sweepingを実行
    while True:
        try:
            input ("Press Enter to start beam sweeping or Ctrl+C to exit...")
            sequence_ops(beam_seq_tables, args["xapp_beam_management_bin_path"], interval=args['beam_switch_interval'])
        except KeyboardInterrupt:
            print("中断されました。")
            kill_softmodem(proc)
            break

if __name__ == "__main__":
    args = arg_parser()
    main(args)
