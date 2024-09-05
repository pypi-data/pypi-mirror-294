import json
from zipfile import ZipFile
from io import TextIOWrapper
from tqdm import tqdm
from spacy.lang.en import English
from saf import Token
from ..skb import KnowledgeBase
from ..data_model import Statement

PATH = "NLI4CT/Complete_dataset.zip"
URL = "https://github.com/ai-systems/nli4ct/raw/main/Complete_dataset.zip"


class NLI4CTKB(KnowledgeBase):
    """
    Wrapper for the NLI4CT dataset (Julien et al., 2018): https://github.com/ai-systems/nli4ct
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

            ct_fpaths = [path for path in dataset_file.namelist()
                         if (path.startswith("Complete_dataset/CT json") and path.endswith(".json"))]
            for fpath in tqdm(ct_fpaths, desc="Loading CT data"):
                with TextIOWrapper(dataset_file.open(fpath), encoding="utf-8") as ct_file:
                    ct_data = json.load(ct_file)
                    ct_id = ct_data["Clinical Trial ID"]
                    self.key_idx[ct_id] = list()
                    del ct_data["Clinical Trial ID"]
                    for section in ct_data:
                        idx = 0
                        for line in ct_data[section]:
                            stt = Statement(line.strip())
                            stt.annotations["id"] = ct_id
                            stt.annotations["section"] = section
                            stt.annotations["index"] = idx

                            for tok in self.tokenizer(stt.surface):
                                token = Token()
                                token.surface = tok.text
                                stt.tokens.append(token)

                            self.data.append(stt)
                            self.key_idx[ct_id].append(stt)
                            idx += 1

            for split in ["train", "dev", "Gold_test"]:
                with TextIOWrapper(dataset_file.open(f"Complete_dataset/{split}.json"), encoding="utf-8") as data_file:
                    data = json.load(data_file)
                    for uuid in tqdm(data, desc=f"Loading data [{split}]"):
                        self.key_idx[uuid] = list()
                        stt = Statement(data[uuid]["Statement"])
                        stt.annotations["id"] = uuid
                        stt.annotations["split"] = split
                        stt.annotations["type"] = data[uuid]["Type"]
                        stt.annotations["section_id"] = data[uuid]["Section_id"]
                        stt.annotations["primary_id"] = data[uuid]["Primary_id"]
                        if ("Label" in data[uuid]):
                            stt.annotations["label"] = data[uuid]["Label"]

                        for tok in self.tokenizer(stt.surface):
                            token = Token()
                            token.surface = tok.text
                            stt.tokens.append(token)

                        for prem_idx in data[uuid]["Primary_evidence_index"]:
                            prem = [
                                p for p in self.key_idx[data[uuid]["Primary_id"]]
                                if (p.annotations["section"] == data[uuid]["Section_id"] and
                                    p.annotations["index"] == prem_idx)
                            ]
                            stt.premises.append(prem[0])

                        if ("Secondary_id" in data[uuid]):
                            stt.annotations["secondary_id"] = data[uuid]["Secondary_id"]
                            for prem_idx in data[uuid]["Secondary_evidence_index"]:
                                prem = [
                                    p for p in self.key_idx[data[uuid]["Secondary_id"]]
                                    if (p.annotations["section"] == data[uuid]["Section_id"] and
                                        p.annotations["index"] == prem_idx)
                                ][0]
                                stt.premises.append(prem)

                        self.data.append(stt)
                        self.key_idx[uuid].append(stt)

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
        if (isinstance(idx, slice) or isinstance(idx, int)):
            item = self.data[idx]
        else:
            item = self.key_idx[idx]

        return item

    def keys(self):
        return self.key_idx.keys()



