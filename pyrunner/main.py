def main():
    print("Starting simplecell")

    import bluepyopt.ephys as ephys

    print("Setting up simple cell model")

    morph = ephys.morphologies.NrnFileMorphology('simple.swc')

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

    print("Setting up stimulation protocols"
    soma_loc=ephys.locations.NrnSeclistCompLocation(
        name='soma',
        seclist_name='somatic',
        sec_index=0,
        comp_x=0.5)

    sweep_protocols=[]

    for protocol_name, amplitude in [('step1', 0.01), ('step2', 0.05)]:
        stim=ephys.stimuli.NrnSquarePulse(
            step_amplitude=amplitude,
            step_delay=100,
            step_duration=50,
            location=soma_loc,
            total_duration=200)
        rec=ephys.recordings.CompRecording(
            name='%s.soma.v' % protocol_name,
            location=soma_loc,
            variable='v')
        protocol=ephys.protocols.SweepProtocol(protocol_name, [stim], [rec])
        sweep_protocols.append(protocol)
    twostep_protocol=ephys.protocols.SequenceProtocol(
        'twostep', protocols=sweep_protocols)

    print("#######################################")
    print("Stimulation protocols have been set up ")
    print("#######################################")

    print(twostep_protocol)


    nrn=ephys.simulators.NrnSimulator()



if __name__ == '__main__':
    main()
