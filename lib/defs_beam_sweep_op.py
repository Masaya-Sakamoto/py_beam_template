import subprocess
import time
from datetime import datetime
from pytypes.type_beam import beam_sweeping_t

def oai_xapp_beam_management_handler(txBeamId:int, rxBeamId:int, program_path:str) -> bool:
    """
    
    This function just calls the oai_xapp_beam_management() function from the OAI xApp.
    returns True if the function executes successfully, otherwise returns False.
    Usage: ./oaibox_xapp_beam_management --txBeamId <int> --rxBeamId <int>
    """
    # oai_xapp_beam_management() takes txBeamId and rxBeamId as arguments
    command = [program_path, "--txBeamId", str(txBeamId), "--rxBeamId", str(rxBeamId)]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Command not found")
        return False

def sequence_ops(beam_sweep_tables: list[beam_sweeping_t], program_path:str) -> bool:
    """
    beam_sweep_table: beam sweep sequenceテーブル {"id", "theta", "phi"}
    oai_xapp_beam_management_handlerをbeam_sweep_tableに基づいて実行する.
    """
    for beam in beam_sweep_tables:
        txBeamId = beam["id"]
        rxBeamId = beam["id"]
        print(f"Executing beam management for BeamId: {txBeamId}, Theta: {beam['theta']}, Phi: {beam['phi']} at {datetime.now()}")
        if not oai_xapp_beam_management_handler(txBeamId, rxBeamId, program_path):
            return False
        time.sleep(beam['duration'])
    return True