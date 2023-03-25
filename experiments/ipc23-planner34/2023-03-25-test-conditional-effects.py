#! /usr/bin/env python3

import itertools
import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment
from lab.reports import Attribute, geometric_mean

from downward.reports.compare import ComparativeReport

import common_setup
from common_setup import IssueConfig, IssueExperiment

ARCHIVE_PATH = "sieverss/downward/ipc23-planner34"
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REVISIONS = ["59572c5642c46928e3b6643983959c72d021c516"]
BUILDS = ["release"]
CONFIG_NICKS = [
    ('scp-pdbs-cartesian-domain-abstractions', ["--search", "astar(scp([projections(hillclimbing(max_time=10)), projections(systematic(2)), cartesian(max_time=10), projections(multiple_cegar(total_max_time=10, max_pdb_size=10k, max_collection_size=1M, stagnation_limit=2, blacklist_trigger_percentage=0, verbosity=normal)), domain_abstractions(multiple_domain_abstractions_cegar(total_max_time=10,flaw_treatment=random_single_atom, max_abstraction_size=10k, max_collection_size=1M, init_split_quantity=single, init_split_candidates=goals, init_split_method=identity, blacklist_trigger_percentage=0, verbosity=normal))], max_orders=infinity, max_optimization_time=2, diversify=true, max_time=20, orders=greedy_orders(scoring_function=max_heuristic_per_stolen_costs)))"]),
]
CONFIGS = [
    IssueConfig(
        config_nick,
        config,
        build_options=[build],
        driver_options=["--build", build, "--search-time-limit", "5m"])
    for build in BUILDS
    for config_nick, config in CONFIG_NICKS
]

# optimal_adl
SUITE = ["assembly", "caldera-opt18-adl", "caldera-split-opt18-adl",
"cavediving-14-adl", "citycar-opt14-adl", "maintenance-opt14-adl",
"miconic-fulladl", "miconic-simpleadl", "nurikabe-opt18-adl",
"openstacks", "openstacks-opt08-adl", "optical-telegraphs",
"philosophers", "psr-large", "psr-middle", "schedule",
"settlers-opt18-adl", "trucks"]
ENVIRONMENT = BaselSlurmEnvironment(
    partition="infai_2",
    email="silvan.sievers@unibas.ch",
    # paths obtained via:
    # module purge
    # module -q load CMake/3.23.1-GCCcore-11.3.0.lua
    # module -q load GCC/11.3.0.lua
    # echo $PATH
    # echo $LD_LIBRARY_PATH
    setup='export PATH=/scicore/soft/apps/binutils/2.38-GCCcore-11.3.0/bin:/scicore/soft/apps/CMake/3.23.1-GCCcore-11.3.0/bin:/scicore/soft/apps/libarchive/3.6.1-GCCcore-11.3.0/bin:/scicore/soft/apps/XZ/5.2.5-GCCcore-11.3.0/bin:/scicore/soft/apps/cURL/7.83.0-GCCcore-11.3.0/bin:/scicore/soft/apps/OpenSSL/1.1/bin:/scicore/soft/apps/bzip2/1.0.8-GCCcore-11.3.0/bin:/scicore/soft/apps/ncurses/6.3-GCCcore-11.3.0/bin:/scicore/soft/apps/GCCcore/11.3.0/bin:/infai/sieverss/repos/bin:/infai/sieverss/local:/export/soft/lua_lmod/centos7/lmod/lmod/libexec:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$PATH\nexport LD_LIBRARY_PATH=/scicore/soft/apps/binutils/2.38-GCCcore-11.3.0/lib:/scicore/soft/apps/libarchive/3.6.1-GCCcore-11.3.0/lib:/scicore/soft/apps/XZ/5.2.5-GCCcore-11.3.0/lib:/scicore/soft/apps/cURL/7.83.0-GCCcore-11.3.0/lib:/scicore/soft/apps/OpenSSL/1.1/lib:/scicore/soft/apps/bzip2/1.0.8-GCCcore-11.3.0/lib:/scicore/soft/apps/zlib/1.2.12-GCCcore-11.3.0/lib:/scicore/soft/apps/ncurses/6.3-GCCcore-11.3.0/lib:/scicore/soft/apps/GCCcore/11.3.0/lib64')

if common_setup.is_test_run():
    SUITE = ["miconic-simpleadl:s3-0.pddl"]
    ENVIRONMENT = LocalEnvironment(processes=4)

exp = IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp.add_step('build', exp.build)
exp.add_step('start', exp.start_runs)
exp.add_fetcher(name='fetch')

attributes = exp.DEFAULT_TABLE_ATTRIBUTES

exp.add_absolute_report_step(attributes=attributes)

exp.add_archive_step(ARCHIVE_PATH)

exp.run_steps()
