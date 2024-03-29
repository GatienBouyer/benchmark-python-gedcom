from time import perf_counter

from fastgedcom.helpers import extract_int_year
from gedcom.element.individual import IndividualElement  # type: ignore
from gedcom.parser import Parser  # type: ignore

from CONFIG import GEDCOM_FILE

start_time = perf_counter()

gedcom = Parser()
gedcom.parse_file(GEDCOM_FILE)

end_time = perf_counter()

print(f"Time to parse: {end_time - start_time}")

##############################################################################

start_time = perf_counter()


def nb_gen(indi: IndividualElement) -> int:
    return max([1+nb_gen(p) for p in gedcom.get_parents(indi)] + [1])


root = gedcom.get_element_dictionary()["@I1@"]
number_generations_above_root = nb_gen(root)

end_time = perf_counter()

print(f"Number of generations above root: {number_generations_above_root}")
print(f"Time to traverse parents: {end_time - start_time}")

##############################################################################

start_time = perf_counter()


def nb_descendants_rec(parent: IndividualElement) -> int:
    children = [c for f in gedcom.get_families(parent)
                for c in gedcom.get_family_members(f, "CHIL")]
    return len(children) + sum(nb_descendants_rec(child) for child in children)


root2 = gedcom.get_element_dictionary()["@I1692@"]
nb_descendants = nb_descendants_rec(root2)

end_time = perf_counter()

print(f"Number of children: {nb_descendants}")
print(f"Time to traverse children: {end_time - start_time}")


##############################################################################


start_time = perf_counter()

oldest: IndividualElement | None = None
age_oldest = 0.0
for element in gedcom.get_root_child_elements():
    if not isinstance(element, IndividualElement):
        continue
    birth_year = element.get_birth_year()
    death_year = element.get_death_year()
    if birth_year == -1 or death_year == -1:
        continue
    age = death_year - birth_year
    if age > age_oldest:
        oldest = element
        age_oldest = age

end_time = perf_counter()
assert (oldest)
print(f"Oldest person: {oldest.get_name()}    Age: {age_oldest} (note: BC doesn't work)")
print(f"Time to traverse ages: {end_time - start_time}")
