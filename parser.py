with open(r'school_work\cs121_databases\final_project\facts.txt', 'r') as f:
    facts = f.read()
    facts = facts.split('\n')
    facts = [fact for fact in facts if fact != '']

    good_facts = []    
    for fact in facts:
        # get the fact number from the first few characters in the fact
        f = fact[fact.find('.')+2:]
        good_facts.append(f)
with open(r'school_work\cs121_databases\final_project\parsed_facts.txt', 'w') as facts_file:
    facts_file.write("fact_id,fact\n")
    for fact_num, fact in enumerate(good_facts):
        facts_file.write(f'{fact_num+1}|{fact}\n')

