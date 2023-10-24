def main():
    print("Starting simplecell")

    import bluepyopt.ephys as ephys

    print("Setting up simple cell model")

    morph = ephys.morphologies.NrnFileMorphology('pyrunner/simple.swc')

    somatic_loc = ephys.locations.NrnSeclistLocation(
        'somatic', seclist_name='somatic')

    hh_mech = ephys.mechanisms.NrnMODMechanism(
        name='hh',
        suffix='hh',
        locations=[somatic_loc])

    hh_mech = ephys.mechanisms.NrnMODMechanism(
        name='hh',
        suffix='hh',
        locations=[somatic_loc])

    cm_param = ephys.parameters.NrnSectionParameter(name='cm',
                                                    param_name='cm',
                                                    value=1.0,
                                                    locations=[somatic_loc],
                                                    frozen=True)

    gnabar_param = ephys.parameters.NrnSectionParameter(
        name='gnabar_hh',
        param_name='gnabar_hh',
        locations=[somatic_loc],
        bounds=[0.05, 0.125],
        frozen=False)
    gkbar_param = ephys.parameters.NrnSectionParameter(
        name='gkbar_hh',
        param_name='gkbar_hh',
        bounds=[0.01, 0.075],
        locations=[somatic_loc],
        frozen=False)

    simple_cell = ephys.models.CellModel(
        name='simple_cell',
        morph=morph,
        mechs=[hh_mech],
        params=[cm_param, gnabar_param, gkbar_param])

    print("#############################")
    print("Simple neuron has been set up")
    print("#############################")

    print(simple_cell)

    print("Setting up stimulation protocols")
    soma_loc = ephys.locations.NrnSeclistCompLocation(name='soma',
                                                      seclist_name='somatic',
                                                      sec_index=0,
                                                      comp_x=0.5)

    sweep_protocols = []

    for protocol_name, amplitude in [('step1', 0.01), ('step2', 0.05)]:
        stim = ephys.stimuli.NrnSquarePulse(
            step_amplitude=amplitude,
            step_delay=100,
            step_duration=50,
            location=soma_loc,
            total_duration=200)
        rec = ephys.recordings.CompRecording(
            name='%s.soma.v' % protocol_name,
            location=soma_loc,
            variable='v')
        protocol = ephys.protocols.SweepProtocol(protocol_name, [stim], [rec])
        sweep_protocols.append(protocol)
    twostep_protocol = ephys.protocols.SequenceProtocol(
        'twostep', protocols=sweep_protocols)

    print("#######################################")
    print("Stimulation protocols have been set up ")
    print("#######################################")

    print(twostep_protocol)

    print('Setting up objectives')
    efel_feature_means = {
        'step1': {
            'Spikecount': 1}, 'step2': {
            'Spikecount': 5}}

    objectives = []

    for protocol in sweep_protocols:
        stim_start = protocol.stimuli[0].step_delay
        stim_end = stim_start + protocol.stimuli[0].step_duration
        for efel_feature_name, mean in efel_feature_means[protocol.name].items(
        ):
            feature_name = '%s.%s' % (protocol.name, efel_feature_name)
            feature = ephys.efeatures.eFELFeature(
                feature_name,
                efel_feature_name=efel_feature_name,
                recording_names={'': '%s.soma.v' % protocol.name},
                stim_start=stim_start,
                stim_end=stim_end,
                exp_mean=mean,
                exp_std=0.05 * mean)
            objective = ephys.objectives.SingletonObjective(
                feature_name,
                feature)
            objectives.append(objective)

    print("############################")
    print("Objectives have been set up ")
    print("############################")

    print('Setting up fitness calculator')

    score_calc = ephys.objectivescalculators.ObjectivesCalculator(objectives)

    nrn = ephys.simulators.NrnSimulator()

    cell_evaluator = ephys.evaluators.CellEvaluator(
        cell_model=simple_cell,
        param_names=['gnabar_hh', 'gkbar_hh'],
        fitness_protocols={twostep_protocol.name: twostep_protocol},
        fitness_calculator=score_calc,
        sim=nrn)

    print("####################################")
    print("Fitness calculator have been set up ")
    print("####################################")

    print('Running test evaluation:')
    default_params = {'gnabar_hh': 0.1, 'gkbar_hh': 0.03}
    print(cell_evaluator.evaluate_with_dicts(default_params))

    print("###############################")
    print("Test evaluation was successful ")
    print("###############################")


if __name__ == '__main__':
    main()
