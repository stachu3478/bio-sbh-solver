# Sekwencjonowanie poprzez hybrydyzację - algorytm metaheurystyczny

Program podejmuje próbę rozwiązania problemu złożenia DNA ze spektrum powstałego z sekwencjonowania poprzez hybrydyzację używając algorytmu mrówkowego. 

## Wymagania

- Python 3.9.0 lub nowszy
- Dowolny wiersz poleceń

## Uruchamianie

Program rozwiązuje problemy w oparciu o plik we własnym formacie, który można wygenerować masowo również przy pomocy programu.

### Generowanie instancji problemu

Do wygenerowania folderu z instancjami służy komenda wywowała w folderze projektu:

```Bash
python ./generate.py <folder z instancjami> [baza DNA]
```

Folder z instancjami należy podać obowiązkowo. Nowy folder jest tworzony, gdy takowy nie istnieje. Zachowanie programu jest niedeterministyczne, gdy w folderze znajdują się pliki.

Można wybrać bazę DNA:
- "random" - losowanie nukleotydów z równomiernym rozkładem (domyślnie) lub
- "sars_cov_2" - na podstawie losowego wycinku z kodu koronawirusa

Efekt: wygenerowanie 240 plików z instancjami i zapisania w wybranym folderze pod nazwami `n<długość DNA>k<długość oligonuleotydów>pe<współczynnik błędów negatywnych>ne<współczynnik błędów pozytywnych`, po 1 z każdej permutacji parametrów n (300, 500, 750), k (7, 8, 9, 10) błędów negatywnych i pozytywnych (0%, 4%, 8%, 12%), z wyjątkiem instancji bez żadnych błędów.

W przypadku podania niewłaściwych argumentów wyświetlenie informacji o błędzie.

### Uruchamianie algorytmu na pojedyńczym pliku z instancją

Do uruchomienia algorytmu dla pojedyńczego pliku służy komenda wywowała w folderze projektu:

```Bash
python ./solve.py <ścieżka do pliku z instancją> [algorytm]
```

Ścieżkę do pliku z instancją należy podać obowiązkowo. Zachowanie programu jest niedeterministyczne, gdy plik nie zawiera instancji problemu.

Można wybrać algorytm:
- "Greedy" lub "GreedyLeastWeight (domyślnie) - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w kolejności rosnących odległości od pasujących do siebie oligonukleotydów (malejąco do liczby nakładających się nukleotydów)
- "GreedyRandomWeight - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w losowej kolejności odległości od pasujących do siebie oligonukleotydów
- "GreedyHighestWeight - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w malejącej kolejności odległości od pasujących do siebie oligonukleotydów

Efekt: Podanie wczytanej sekwencji instancji problemu, rozwiązania proponowanego przez algorytm na podstawie spektrum oraz dodatkowych informacjach o jakości i podobieństwie, w zależności od podanego algorytmu.

W przypadku podania niewłaściwych argumentów wyświetlenie informacji o błędzie.

### Uruchamianie algorytmu na folderze z instancjami

Do uruchomienia algorytmu dla folderu z instancjami służy komenda wywowała w folderze projektu:

```Bash
python ./solve_dir.py <ścieżka do folderu z instancjami> [algorytm]
```

Ścieżkę do folderu z instancjami należy podać obowiązkowo. Zachowanie programu jest niedeterministyczne, gdy pliki w folderze nie zawierają instancji problemu lub w folderze są zagnieżdżone foldery.

Można wybrać algorytm:
- "Greedy" lub "GreedyLeastWeight (domyślnie) - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w kolejności rosnących odległości od pasujących do siebie oligonukleotydów (malejąco do liczby nakładających się nukleotydów)
- "GreedyRandomWeight - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w losowej kolejności odległości od pasujących do siebie oligonukleotydów
- "GreedyHighestWeight - przeszukiwanie grafu w celu znalezienia pierwszego rozwiązania problemu w malejącej kolejności odległości od pasujących do siebie oligonukleotydów

Efekt: Podanie informacji o podobieństwach rozwiązań podawanych przez algorytm dodatkowe informacje o jakości (w zależności od algorytmu) oraz informacje podsumowujące: Średnie podobieństwo, najgorszy przypadek podobieństwa oraz liczba idealnie pokrywających się ze sobą sekwencji.

W przypadku podania niewłaściwych argumentów wyświetlenie informacji o błędzie.

### Parametry algorytmu metaheurystycznego

Zmiana parametrów algorytmu wymaga modyfikacji kodu źródłowego.
Parametry są ustawiane w pliku `algorithm/Ant.py` w linijce 13. Obecny ich stan:

```Python
# tuning variables
self.ant_count = 1000
self.feromon_half_vapor_time = 0.375
self.min_feromon = 0.000001 # 0.00001
self.starvation_cycles = 10 # 5

self.vertex_degree_weight = 1.0
self.chain_length_weight = 1.0
self.unique_vertex_weight = 1.0
```
