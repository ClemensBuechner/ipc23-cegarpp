#! /usr/bin/env python3

import os
import sys

from lab.environments import LocalEnvironment, BaselSlurmEnvironment
from lab.reports import Attribute

import common_setup
from common_setup import IssueConfig, IssueExperiment

ARCHIVE_PATH = "buechner/ipc23-cegarpp/post-analysis"
DIR = os.path.dirname(os.path.abspath(__file__))
BENCHMARKS_DIR = os.environ["IPC2023_OPT_BENCHMARKS"]
REVISIONS = [
    ("d7190500a", ""),
]
BUILD = "release"
DRIVER_OPTIONS = [
    "--build", BUILD,
    "--overall-time-limit", "30m",
    "--overall-memory-limit", "8192M",
]

ABSTRACTION_GENERATORS = [
    ("HC", "projections(hillclimbing(max_time=100))"),
    ("sys-2", "projections(systematic(2))"),
    ("cart", "cartesian()"),
    ("cegar-pdb", "projections(multiple_cegar(total_max_time=100, max_pdb_size=10k, max_collection_size=1M, stagnation_limit=20, blacklist_trigger_percentage=0, verbosity=normal))"),
    ("cegar-dom", "domain_abstractions(multiple_domain_abstractions_cegar(flaw_treatment=random_single_atom, max_abstraction_size=10k, max_collection_size=1M, init_split_quantity=single, init_split_candidates=goals, init_split_method=identity, blacklist_trigger_percentage=0, verbosity=normal))"),
]
PREFIX = "astar(scp(["
SUFFIX = "], max_orders=infinity, max_optimization_time=2, diversify=true, max_time=200, orders=greedy_orders(scoring_function=max_heuristic_per_stolen_costs)))"
full_list = ""
for _, generator in ABSTRACTION_GENERATORS:
    full_list += generator + ", "
full_list = full_list[:-2]
CONFIGS = [
    IssueConfig(
        "cegarpp",
        ["--search", PREFIX + full_list + SUFFIX],
        build_options=[BUILD],
        driver_options=DRIVER_OPTIONS,
    ),
] + [
    IssueConfig(
        name,
        ["--search", PREFIX + generator + SUFFIX],
        build_options=[BUILD],
        driver_options=DRIVER_OPTIONS,
    ) for name, generator in ABSTRACTION_GENERATORS
]

SUITE = [
    "folding",
    "labyrinth",
    "quantum-layout",
    "recharging-robots",
    "ricochet-robots",
    "rubiks-cube",
    "slitherlink",
]

ENVIRONMENT = BaselSlurmEnvironment(
    partition="infai_3",
    memory_per_cpu="8500M",
    email="clemens.buechner@unibas.ch",
    export=["PATH", "IPC23_OPT_BENCHMARKS"])

if common_setup.is_test_run():
    SUITE = ["rubiks-cube:p03.pddl"]
    ENVIRONMENT = LocalEnvironment(processes=4)

exp = IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

ATTRIBUTES = IssueExperiment.DEFAULT_TABLE_ATTRIBUTES + [
    Attribute("landmarks", min_wins=False),
    Attribute("landmarks_disjunctive", min_wins=False),
    Attribute("landmarks_conjunctive", min_wins=False),
    Attribute("orderings", min_wins=False),
    Attribute("lmgraph_generation_time", min_wins=True),
    Attribute("initial_h_lm", min_wins=True),
]

exp.add_step('build', exp.build)
exp.add_step('start', exp.start_runs)
exp.add_fetcher(name='fetch', merge=True)

exp.add_absolute_report_step(attributes=ATTRIBUTES)
# exp.add_scatter_plot_step(relative=True, attributes=["search_time", "cost"])
# exp.add_scatter_plot_step(relative=False, attributes=["search_time", "cost"])

exp.add_parse_again_step()

exp.add_archive_step(ARCHIVE_PATH)

exp.run_steps()
