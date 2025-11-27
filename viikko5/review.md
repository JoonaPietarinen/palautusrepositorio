Copilotin PR arvio:

Copilotin sanoin "The refactoring maintains the existing functionality while making the code more maintainable and readable."

Ainoana ehdotuksena Copilot ehdotti, että score_name(): metodin loppuun lisätään raise ValueError, jos metodia yritetään käyttää kolmea suuremmalla luvulla.

Katselmointi oli melko kompakti, mutta sain siitä sellaisen vaikutelman että Copilot oli tyytyväinen työhöni. Copilotin antama ehdotus tuntui hieman turhalta, sillä
score_name() metodia kutsutaan vain ja ainoastaan current_scores() metodin kautta, jota kutsutaan get_score() metodin kautta vain ja ainoastaan luvuilla 0, 1, 2 ja 3.
Lisäsin ehdotuksen koodiin silti, koska liiallisesta varovaisuudesta ei ainakaan tässä kontekstissa ole haittaa.
