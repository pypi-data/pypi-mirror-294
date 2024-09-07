import os
import time


current_dir = os.path.dirname(__file__)
version_file_path = os.path.join(current_dir, '_VERSION')

with open(version_file_path, 'r') as f:
    __version__ = f.read().strip()


def run_simulation(*args):
    """
    Run a simulation with BioCompose

    Args:
        - args: Positional arguments
            - 1 argument(**smoldyn simulation only**): smoldyn simulation configuration in which time parameters (dt, duration) are already defined.
            - 3 arguments(**smoldyn simulation only**): smoldyn configuration file, smoldyn simulation duration, smoldyn simulation dt
            - 5 arguments(**sbml simulation only**): sbml filepath, simulation start, simulation end, simulation steps, simulator

    """
    from bio_compose.runner import SimulationRunner, SimulationResult

    # set up submission
    runner = SimulationRunner()
    in_file = args[0]
    n_args = len(args)
    submission = None

    if n_args == 1:
        submission = runner.run_smoldyn_simulation(smoldyn_configuration_filepath=in_file)
    elif n_args == 3:
        dur = args[1]
        dt = args[2]
        submission = runner.run_smoldyn_simulation(smoldyn_configuration_filepath=in_file, duration=dur, dt=dt)
    elif n_args == 5:
        start = args[1]
        end = args[2]
        steps = args[3]
        simulator = args[4]
        submission = runner.run_utc_simulation(sbml_filepath=in_file, start=start, end=end, steps=steps, simulator=simulator)

    # fetch results
    job_id = submission.get('job_id')
    output = None
    if job_id is not None:
        while True:
            simulation_result = runner.get_output(job_id=job_id)
            status = simulation_result['content']['status']
            if not 'COMPLETED' in status:
                time.sleep(1)
            else:
                output = simulation_result
                break

    return SimulationResult(data=output)


def verify(*args, **kwargs):
    """
    Verify and compare the outputs of simulators for a given entrypoint file of either sbml or omex.

    Args:
        - **args**: positional arguments passed to the verification.
            - 1 argument(`str`): submit an sbml or omex verification with no time params.
            - 2 arguments(`str`, `list[str]`): omex filepath, simulators to include in the verification.
            - 4 arguments(`str`, `int`, `int`, `int`): sbml filepath, start, stop, steps.
            - 5 arguments(`str`, `int`, `int`, `int`, `list[str]`): sbml filepath, start, stop, steps, simulators.
        - **kwargs**: keyword arguments passed to the verification.

    Returns:
        Verification result instance. See documentation for more details.
    """
    from bio_compose.verifier import Verifier, VerificationResult

    verifier = Verifier()
    simulators = kwargs.get('simulators')
    run_sbml = False
    for arg in args:
        if isinstance(arg, int):
            run_sbml = True
    submission = None
    if run_sbml:
        submission = verifier.verify_sbml(*args, **kwargs)
    else:
        submission = verifier.verify_omex(*args, **kwargs)
    job_id = submission.get('job_id')
    output = None
    if job_id is not None:
        while True:
            verification_result = verifier.get_output(job_id=job_id)
            status = verification_result['content']['status']
            if not 'COMPLETED' in status:
                time.sleep(1)
            else:
                output = verification_result
                break

    return VerificationResult(data=output)
