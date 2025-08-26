# from lib.defs_beams import def_lin_beams
# from lib.defs_beam_sweeping import def_basic_lin_beamsweeping
# from lib.defs_beam_sweep_op import sequence_ops

# retcode = 0
# def init_testcase(testcase_retcode:int):
#     global retcode
#     retcode = testcase_retcode

# def mock_oaibox_xapp_beam_management_handler(txBeamId:int, rxBeamId:int, program_path:str) -> bool:
#     return retcode == 0

# def test_sequence_ops(mocker):
#     program_path = "/path/to/oai_xapp_beam_management" # dummy

#     # beam sweep sequenceを定義
#     origin = {"id": 1, "theta": 0, "phi": 0}
#     beam_sweep_tables = [
#         [
#             origin,
#             {"id": 2, "theta": 10, "phi": 0},
#             origin
#         ]
#     ]

#     # mock initialize: subprocess.run, sleep
#     mocker.patch('time.sleep')
#     mocker.patch('lib.defs_beamsweep_op.oai_xapp_beam_management_handler', new=mock_oaibox_xapp_beam_management_handler)

#     init_testcase(0) # Mock successful execution
#     assert sequence_ops(beam_sweep_tables, program_path) == True
#     init_testcase(1) # Mock failed execution
#     assert sequence_ops(beam_sweep_tables, program_path) == False