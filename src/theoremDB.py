from past.formulaDB import *

class tm(Enum):
    is_ordered_set = "is_ordered_set",
    is_least_upper_bound = "is_least_upper_bound",
    is_not_empty = "is_not_empty",
    is_subset_of = "is_subset_of",
    is_bounded_below = "is_bounded_below",
    is_inf_exist = "is_inf_exit"

class tid(Enum):
    n1 = "existence of sup/inf"

theorem_db = set()

theorem_db.add(
    # Bady.Rudin.TM.1.11
    (
        {tm.is_ordered_set, tm.is_least_upper_bound, tm.is_bounded_below},
        tm.is_inf_exist
    )
)