Method Ideas
- create race
- calculate total
- show scores for person
- show scores for race
- edit scores for race
- edit scores for person
- get scores given a specific fleet, sorted (overall, race, intro)
- export to spreadsheet?

Have to figure out how to store everything.

Each race is a dictionary. The keys to the dictionary are the names. The value for each key is their score for the race.

Totals are a dictionary. Each key is a person and each value is the total.

or...

Whole thing is dictionary. Keys are people. Key is assigned to an object with array (race results) and a number (total points)

We only keep track of overall results. When we need a specific fleet, we just go through sorted and only display those people.

Todo
- tie breakers
- inputting of race results
- hook up json file
- fleet specific results