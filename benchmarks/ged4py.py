from typing import cast
from time import perf_counter

from fastgedcom.helpers import extract_int_year
from ged4py import GedcomReader  # type: ignore
from ged4py.model import Individual  # type: ignore

from CONFIG import GEDCOM_FILE

start_time = perf_counter()

gedcom = GedcomReader(GEDCOM_FILE)
assert gedcom.xref0

end_time = perf_counter()

print(f"Time to parse: {end_time - start_time}")

##############################################################################

start_time = perf_counter()


def nb_gen(indi: Individual) -> int:
    return max([1+nb_gen(p) for p in (indi.father, indi.mother) if p] + [1])


root = cast(Individual, gedcom.read_record(gedcom.xref0["@I1@"][0]))
number_generations_above_root = nb_gen(root)

end_time = perf_counter()

print(f"Number of generations above root: {number_generations_above_root}")
print(f"Time to traverse parents: {end_time - start_time}")

##############################################################################

start_time = perf_counter()


def nb_descendants_rec(parent: Individual) -> int:
    children = [child for f in parent.sub_tags('FAMS') for child in f.sub_tags('CHIL')]
    return len(children) + sum(nb_descendants_rec(child) for child in children)


assert (gedcom.xref0)
root2 = cast(Individual, gedcom.read_record(gedcom.xref0["@I1692@"][0]))
nb_descendants = nb_descendants_rec(root2)

end_time = perf_counter()

print(f"Number of children: {nb_descendants}")
print(f"Time to traverse children: {end_time - start_time}")


##############################################################################


start_time = perf_counter()

oldest = cast(Individual, next(gedcom.records0("INDI")))
age_oldest = 0.0
for element in gedcom.records0("INDI"):
    if not isinstance(element, Individual):
        continue
    birth_date = element.sub_tag_value("BIRT/DATE")
    death_date = element.sub_tag_value("DEAT/DATE")
    if birth_date is None or death_date is None:
        continue
    birth_year = extract_int_year(str(birth_date)[1:-1])
    death_year = extract_int_year(str(death_date)[1:-1])
    if birth_year is None or death_year is None:
        continue
    age = death_year - birth_year
    if age > age_oldest:
        oldest = element
        age_oldest = age

end_time = perf_counter()
assert (oldest)
print(f"Oldest person: {oldest.name.format()}    Age: {age_oldest}")
print(f"Time to traverse ages: {end_time - start_time}")
