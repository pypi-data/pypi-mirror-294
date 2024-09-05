from zipfile import ZipFile
from io import TextIOWrapper
from csv import DictReader
from tqdm import tqdm
from spacy.lang.en import English
from saf import Token
from ..skb import KnowledgeBase, BASE_URL
from ..data_model import Statement

PATH = "eSNLI/eSNLI.zip"
URL = BASE_URL + "eSNLI.zip"


class ESNLIKB(KnowledgeBase):
    """
    Wrapper for the e-SNLI dataset (Camburu et al., 2018): https://github.com/OanaMariaCamburu/e-SNLI
    """
    def __init__(self, path: str = PATH, url: str = URL):
        super().__init__(path, url)
        self.tokenizer = English().tokenizer
        self.id = PATH.split(".")[0]
        self.key_idx: dict[str, list[Statement]] = dict()
        if (not url):
            return

        with ZipFile(self.data_path) as dataset_file:
            self.data = list()

            for split in ["train", "dev", "test"]:
                with TextIOWrapper(dataset_file.open(f"eSNLI/esnli_{split}.tsv"), encoding="utf-8") as data_file:
                    reader = DictReader(data_file, delimiter="\t")
                    for row in tqdm(reader, desc=f"Loading data [{split}]"):
                        sents = list()
                        self.key_idx[row["pairID"]] = list()
                        for sent_key in ["Sentence1", "Sentence2"]:
                            sent = row[sent_key]
                            stt = Statement(sent)
                            stt.annotations["split"] = split
                            stt.annotations["label"] = row["gold_label"]
                            stt.annotations["type"] = "fact"
                            stt.annotations["number"] = int(sent_key[-1])
                            stt.annotations["id"] = row["pairID"]
                            for i in range(1, 4):
                                if (f"{sent_key}_marked_{i}" in row):
                                    stt.annotations[f"{sent_key}_marked_{i}"] = row[f"{sent_key}_marked_{i}"]
                                    stt.annotations[f"{sent_key}_Highlighted_{i}"] = row[f"{sent_key}_Highlighted_{i}"]

                            for tok in self.tokenizer(stt.surface):
                                token = Token()
                                token.surface = tok.text
                                stt.tokens.append(token)

                            self.data.append(stt)
                            self.key_idx[row["pairID"]].append(stt)
                            sents.append(stt)

                        for expl_key in ["Explanation_1", "Explanation_2", "Explanation_3"]:
                            if (expl_key not in row):
                                continue

                            expl = row[expl_key]
                            for expl_sent in expl.split(". "):
                                stt = Statement(expl_sent)
                                stt.annotations["split"] = split
                                stt.annotations["label"] = row["gold_label"]
                                stt.annotations["type"] = "explanation"
                                stt.annotations["number"] = expl_key[-1]
                                stt.annotations["id"] = row["pairID"]

                                for tok in self.tokenizer(stt.surface):
                                    token = Token()
                                    token.surface = tok.text
                                    stt.tokens.append(token)

                                for sent in sents:
                                    sent.premises.append(stt)

                                self.data.append(stt)
                                self.key_idx[row["pairID"]].append(stt)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int | str | slice) -> Statement | list[Statement]:
        """Fetches the ith statement in the KB.

        Args:
            idx (int): index for the ith term in the KB.

        :return: A single term definition (Statement).
        """
        if (isinstance(idx, int) or isinstance(idx, slice)):
            item = self.data[idx]
        else:
            item = self.key_idx[idx]

        return item

    def keys(self):
        return self.key_idx.keys()

