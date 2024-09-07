import os

os.environ['NEO4J_SCHEMA'] = 'croma'

from semantic_main.autotwin_mapper import write_semantic_links
from sha_learning.autotwin_learn import learn_automaton
from skg_main.autotwin_connector import store_automaton, delete_automaton

SAVE_PATH = os.path.dirname(os.path.abspath(__file__)).split('autotwin_autlib')[0] + 'autotwin_autlib'


def start_automata_learning(pov, start, end):
    # 1: Automata Learning experiment.
    try:
        start = int(start)
        learned_sha = learn_automaton(pov, start_ts=int(start), end_ts=int(end), save_path=SAVE_PATH)
    except ValueError:
        learned_sha = learn_automaton(pov, start_dt=start, end_dt=end, save_path=SAVE_PATH)

    # 2: Delete learned automaton from the SKG, if there already exists one with the same name.
    delete_automaton(learned_sha, pov, start, end)

    # 3: Store the learned automaton into the SKG.
    store_automaton(learned_sha, pov, start, end, SAVE_PATH)

    # 4: Create semantic links between learned model and existing SKG nodes.
    write_semantic_links(learned_sha, pov, start, end, SAVE_PATH)

    return learned_sha
