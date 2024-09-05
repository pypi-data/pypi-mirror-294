from zipfile import ZipFile
from io import TextIOWrapper
from csv import DictReader
from tqdm import tqdm
from spacy.lang.en import English
from saf import Token, Term
from ..skb import KnowledgeBase
from ..data_model import Statement, Entity

PATH = "WorldTree/tg2020task-dataset.zip"
URL = "https://cognitiveai.org/dist/tg2020task-dataset.zip"


class WorldTreeKB(KnowledgeBase):
    """
    Wrapper for the WorldTree dataset (Jansen et al., 2020): https://github.com/cognitiveailab/tg2020task
    """
    def __init__(self, path: str = PATH, url: str = URL):
        super().__init__(path, url)
        self.tokenizer = English().tokenizer
        self.id = PATH.split(".")[0]
        self.key_idx: dict[str, list[Statement]] = dict()
        if (not url):
            return

        ent_nameset = set()
        num_facts = 0
        with ZipFile(self.data_path) as dataset_file:
            self.data = list()
            tbl_paths = [fpath for fpath in dataset_file.namelist() if fpath.startswith("tables/")]
            for tbl_path in tqdm(tbl_paths, desc="Loading fact tables"):
                table_name = tbl_path.split("/")[-1].split(".")[0]
                with TextIOWrapper(dataset_file.open(tbl_path, "r"), encoding="utf-8") as tbl_file:
                    reader = DictReader(tbl_file, delimiter="\t")
                    for row in reader:
                        uid = row["[SKIP] UID"].strip()
                        self.key_idx[uid] = list()
                        terms = [(row[field], field) for field in row if "SKIP" not in field]
                        surface = " ".join([t[0] for t in terms if t[0].strip()])
                        stt = Statement(surface)
                        stt.annotations["UID"] = uid
                        stt.annotations["type"] = "fact"
                        stt.annotations["table"] = table_name
                        if ("[SKIP] DEP" in row and row["[SKIP] DEP"].startswith("SW")):
                            stt.annotations["dep"] = row["[SKIP] DEP"].strip().split()[1:]

                        for t in terms:
                            term = Term()
                            term.surface = t[0]
                            for tok in self.tokenizer(t[0]):
                                token = Token()
                                token.surface = tok.text
                                term.tokens.append(token)

                            term.annotations["role"] = t[1]
                            stt.terms.append(term)
                            stt.tokens.extend(term.tokens)

                            if ("OBJECT" in t[1]):
                                ent_names = [e.strip() for e in t[0].split(";")]
                                for name in ent_names:
                                    if (name not in ent_nameset):
                                        ent = Entity(name, self.id)
                                        ent.metadata["table"] = {table_name}
                                        self.entities.append(ent)
                                        stt.entities.append(ent)
                                        ent_nameset.add(name)
                                    else:
                                        ent = [e for e in self.entities if e.surface == name][0]
                                        ent.metadata["table"].add(table_name)

                        if (stt.surface.strip()):
                            self.data.append(stt)
                            self.key_idx[uid].append(stt)
                            num_facts += 1

            for split in ["train", "dev", "test"]:
                with TextIOWrapper(dataset_file.open(f"questions.{split}.tsv"), encoding="utf-8") as q_file:
                    reader = DictReader(q_file, delimiter="\t")
                    for row in tqdm(reader, desc=f"Loading questions [{split}]"):
                        stt = Statement(row["question"])
                        for field in row:
                            stt.annotations[field] = row[field]
                        del stt.annotations["question"]
                        stt.annotations["type"] = "question"
                        stt.annotations["split"] = split
                        stt.annotations["explanation"] = [
                            tuple(exp.split("|"))
                            for exp in stt.annotations["explanation"].split()
                        ]
                        for expl in stt.annotations["explanation"]:
                            prem = [p for p in self.data[:num_facts] if (p.annotations["UID"] == expl[0])]
                            if (prem):
                                stt.premises.append(prem[0])
                                self.key_idx[expl[0]].append(stt)

                        for tok in self.tokenizer(stt.surface):
                            token = Token()
                            token.surface = tok.text
                            stt.tokens.append(token)

                        if (stt.surface.strip()):
                            self.data.append(stt)

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

