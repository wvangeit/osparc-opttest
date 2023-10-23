def main():
    print("Starting simplecell")

    import bluepyopt.ephys as ephys

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

    print(simple_cell)


if __name__ == '__main__':
    main()
