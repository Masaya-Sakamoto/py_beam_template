from pytypes.type_beam import sweep_program_t, beam_t, beam_sweeping_t

def def_lin_beam_sweeping(origin: dict[str, int], beams: list[dict[str, int]]) -> list[dict[str, int]]:
    """
    Generate a list of basic linear beams with sweeping angles.

    """
    print(f"type(origin)={type(origin)}, type(beams)={type(beams)}")
    return [origin,] + beams + beams[-1::-1]  # Reverse the last beam to create a sweeping effect

def def_basic_lin_beam_sweeping(origin: dict[str, int], beams_list: list[list[dict[str, int]]]) -> list[dict[str, int]]:
    result:list[dict[str, int]] = []
    for beams in beams_list:
        result.extend(def_lin_beam_sweeping(origin, beams))
    return result

def __search_beam(beam_table:list[beam_t], beam_id:int) -> tuple[beam_t|None, int|None]:
    selected_beam = None
    selected_idx = None
    for _i, _beam in enumerate(beam_table):
        if _beam['id'] == beam_id:
            selected_beam = _beam
            selected_idx = _i
            break
    return selected_beam, selected_idx

def write_const_program(const_index:int, reduction:bool, duration:int) -> sweep_program_t:
    return {
            'start_id': const_index,
            'end_id': const_index,
            'step': -1,
            'method': 0,
            'iters': -1,
            'reduction': reduction,
            'duration': duration
    }

def write_lin_sweep_program(start_index:int, end_index:int, step:int, reduction:bool, duration:int) -> sweep_program_t:
    # Generate the linear sweep program
    return {
            'start_id': start_index,
            'end_id': end_index,
            'step': step,
            'method': 1,
            'iters': 1,
            'reduction': reduction,
            'duration': duration
    }

def write_random_sweep_program(start_index:int, end_index:int, step:int, reduction:bool, duration:int, iterations:int) -> sweep_program_t:
    return {
        'start_id': start_index,
        'end_id': end_index,
        'step': step,
        'method': 2,
        'iters': iterations,
        'reduction': reduction,
        'duration': duration
    }

def def_beam_sweeping(beam_table:list[beam_t], sweep_program_lst:list[sweep_program_t], origin_id:int=1) -> list[beam_sweeping_t]:
    """
    input: 
        [
            {"id": 1, "theta": 0, "phi": 0},
            {"id": 1, "theta": 1, "phi": 0}, 
            ...
        ],  -- beam table
        [
            # initial state -- method #0
            {'start_id':  1, 'end_id':  1, 'step': -1, 'method': 0, 'iters': -1, 'reduction': 0, 'duration': 10}

            # motion stop -- method #0 -- 1
            {'start_id':  1, 'end_id':  1, 'step': -1, 'method': 0, 'iters':  1, 'reduction': 1, 'duration': 10},
            # Example: Reciprocating motion -- method #1 -- 2..26..2
            {'start_id':  2, 'end_id': 26, 'step':  1, 'method': 1, 'iters':  1, 'reduction': 0, 'duration': 10},
            {'start_id': 26, 'end_id':  2, 'step':  1, 'method': 1, 'iters':  1, 'reduction': 1, 'duration': 10},
            # motion stop -- method #0 -- 1
            {'start_id':  1, 'end_id':  1, 'step': -1, 'method': 0, 'iters':  1, 'reduction': 1, 'duration': 10},
            # Resuming reciprocating motion -- method#1 -- 27..52..27
            {'start_id': 27, 'end_id': 52, 'step':  1, 'method': 1, 'iters':  1, 'reduction': 1, 'duration': 10},
            {'start_id': 52, 'end_id': 27, 'step':  1, 'method': 1, 'iters':  1, 'reduction': 1, 'duration': 10},
            # motion stop -- method #0 -- 1
            {'start_id':  1, 'end_id':  1, 'step': -1, 'method': 0, 'iters':  1, 'reduction': 1, 'duration': 10},

            # Example: Random motion -- method #2 -- random([1:52]) x3
            {'start_id':  1, 'end_id': 52, 'step': -1, 'method': 2, 'iters':  3, 'reduction': 0, 'duration':  5},

            # termination -- method #0
            {'start_id':  1, 'end_id':  1, 'step': -1, 'method': 0, 'iters': -1, 'reduction': 0, 'duration': 10}
        ],  -- sweep_program_lst

    output:
        [
            {"id": 1, "theta": 0, "phi": 0, "duration": 10},
            {"id": 1, "theta": 1, "phi": 0, "duration": 10},
            ...
        ]
    """
    beam_sweeping = []
    for program in sweep_program_lst:
        start_id = program['start_id']
        end_id = program['end_id']
        step = program['step']
        method = program['method']
        iters = program['iters']
        reduction = program['reduction']
        duration = program['duration']

        # Initial state or stop
        if method == 0:
            # skip if reduction is True
            if (
                reduction and \
                len(beam_sweeping) > 0 and \
                beam_sweeping[-1]['id'] == start_id
            ):
                continue
            selected_beam, _idx = __search_beam(beam_table, start_id)
            if selected_beam is None:
                raise ValueError(f"Beam ID {start_id} not found in beam table.")
            beam_sweeping.append({
                'id': origin_id,
                'theta': selected_beam['theta'],
                'phi': selected_beam['phi'],
                'duration': duration
            })

        #  Sequential motion
        elif method == 1:  
            for _ in range(iters):
                step_vector = (end_id - start_id) // abs(end_id - start_id) * step
                for beam_id in range(start_id, end_id + step_vector, step_vector):
                    # skip if reduction is True
                    if (
                        reduction and \
                        len(beam_sweeping) > 0 and \
                        beam_sweeping[-1]['id'] == beam_id
                    ):
                        continue
                    selected_beam, _idx = __search_beam(beam_table, beam_id)
                    if selected_beam is None:
                        raise ValueError(f"Beam ID {beam_id} not found in beam table.")
                    beam_sweeping.append({
                        'id': selected_beam['id'],
                        'theta': selected_beam['theta'],
                        'phi': selected_beam['phi'],
                        'duration': duration
                    })

        # Random motion     
        elif method == 2:
            import random
            for _ in range(iters):
                # Get the start and end beams
                _garbage, start_idx = __search_beam(beam_table, start_id)
                _garbage, end_idx = __search_beam(beam_table, end_id)
                if start_idx is None:
                    raise ValueError(f"Beam ID {start_id} not found in beam table.")
                if end_idx is None:
                    raise ValueError(f"Beam ID {end_id} not found in beam table.")
                # Adjust end index
                if end_idx == len(beam_table) - 1:
                    end_idx = None  # No end index, use the whole table
                else:
                    end_idx += 1
                src_table = beam_table[start_idx:end_idx]
                random_seq = random.sample(src_table, len(src_table))
                for random_beam in random_seq:
                    beam_sweeping.append({
                        'id': random_beam['id'],
                        'theta': random_beam['theta'],
                        'phi': random_beam['phi'],
                        'duration': duration
                    })

    return beam_sweeping