"""
This is the "CEGAR PDBs and Domain Abstractions" sequential portfolio that
participated in the IPC 2023 optimal track.
"""

OPTIMAL = True

CONFIGS = [
    (1799, ["--search", "astar(scp([projections(hillclimbing(max_time=100)), projections(systematic(2)), cartesian(), projections(multiple_cegar(total_max_time=100, max_pdb_size=10k, max_collection_size=1M, stagnation_limit=20, blacklist_trigger_percentage=0, verbosity=normal)), domain_abstractions(multiple_domain_abstractions_cegar(flaw_treatment=random_single_atom, max_abstraction_size=10k, max_collection_size=1M, init_split_quantity=single, init_split_candidates=goals, init_split_method=identity, blacklist_trigger_percentage=0, verbosity=normal))], max_orders=infinity, max_optimization_time=2, diversify=true, max_time=200, orders=greedy_orders(scoring_function=max_heuristic_per_stolen_costs)))"]),
    # TODO: use something which supports conditional effects
    # (1, ["--search", "astar(scp([projections(hillclimbing(max_time=100)), projections(systematic(2)), cartesian(), projections(multiple_cegar(total_max_time=100, max_pdb_size=10k, max_collection_size=1M, stagnation_limit=20, blacklist_trigger_percentage=0, verbosity=normal)), domain_abstractions(multiple_domain_abstractions_cegar(flaw_treatment=random_single_atom, max_abstraction_size=10k, max_collection_size=1M, init_split_quantity=single, init_split_candidates=goals, init_split_method=identity, blacklist_trigger_percentage=0, verbosity=normal))], max_orders=infinity, max_optimization_time=2, diversify=true, max_time=200, orders=greedy_orders(scoring_function=max_heuristic_per_stolen_costs)))"]),
]
