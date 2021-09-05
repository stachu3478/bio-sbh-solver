from pathlib import Path
import random


def random_sequence(length):
    return ''.join(random.choices(['G', 'T', 'A', 'C'], k=length))


class SbhInstance:
    def create_series_into_folder(self, base_path):
        if base_path != "":
            self._create_dir_if_not_exists(base_path)
        for n in [300, 500, 750, 1000]:
            for k in [7, 8, 9, 10]:
                for pe in [0, 0.04, 0.08, 0.12]:
                    for ne in [0, 0.04, 0.08, 0.12]:
                        if pe == 0 and ne == 0:
                            continue
                        instance = SbhInstance(n, k)
                        instance.introduce_negative_repeat_errors()
                        if pe > 0:
                            instance.introduce_positive_errors(pe)
                        if ne > 0:
                            instance.introduce_negative_leak_errors(ne)
                        instance.save(base_path + '/n' + str(n) +
                                      'k' + str(k) + 'pe' + str(pe) + 'ne' + str(ne) + '.txt')

    def read(self, file):
        """
        Wczytuje plik z instancją sbh

        Parameters
        ----------
        file : string
        Ścieżka do pliku z instancją

        Returns
        -------
        SbhInstance
            Klasa instancji Sbh z wczytanymi danymi
        """
        f = open(file, 'r')
        instance = SbhInstance(
            int(f.readline()), int(f.readline()), build=False)
        spectrum_length = int(f.readline())
        instance.positive_errors = f.readline().strip() == "True"
        instance.negative_errors = f.readline().strip() == "True"
        instance.sequence = f.readline().strip()
        instance.initial_oligo = f.readline().strip()
        instance.spectrum = list(map(lambda o: o.strip(), f.readlines()))
        return instance

    def __init__(self, length, oligo_length, build=True):
        self.length = int(length)
        self.oligo_length = int(oligo_length)
        if build:
            self.build()

    def build(self):
        self.positive_errors = False
        self.negative_errors = False
        self.sequence = random_sequence(self.length)
        self.initial_oligo = self.sequence[:self.oligo_length]
        self.spectrum = [self.sequence[i:i+self.oligo_length]
                         for i in range(self.length - self.oligo_length + 1)]
        random.shuffle(self.spectrum)

    def introduce_positive_errors(self, rate):
        self.positive_errors = True
        for _ in range(int(self.length * rate)):
            self.spectrum.append(random_sequence(self.oligo_length))
        random.shuffle(self.spectrum)

    def introduce_negative_leak_errors(self, rate):
        self.negative_errors = True
        self.spectrum = self.spectrum[int(len(self.spectrum) * rate):]

    def introduce_negative_repeat_errors(self):
        """
        Just based on duplicate removal
        """
        self.spectrum = list(set(self.spectrum))

    def save(self, path):
        f = open(path, "w")
        f.write(str(self.length) + '\n')
        f.write(str(self.oligo_length) + '\n')
        f.write(str(len(self.spectrum)) + '\n')
        f.write(str(self.positive_errors) + '\n')
        f.write(str(self.negative_errors) + '\n')
        f.write(self.sequence + '\n')
        f.write(self.initial_oligo + '\n')
        f.write('\n'.join(self.spectrum))
        f.close()

    def _create_dir_if_not_exists(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)


SbhInstance.create_series_into_folder = classmethod(
    SbhInstance.create_series_into_folder)
SbhInstance.read = classmethod(
    SbhInstance.read)
SbhInstance._create_dir_if_not_exists = classmethod(
    SbhInstance._create_dir_if_not_exists)