import json
import pickle
import gzip
from zipfile import ZipFile
from io import TextIOWrapper
from tqdm import tqdm
from spacy.lang.en import English
from saf import Token
from ..skb import KnowledgeBase, BASE_URL
from ..data_model import Statement, Entity

PATH = "ProofWiki/proofwiki.zip"
URL = BASE_URL + "proofwiki.zip"

ANNOT_RESOURCES = {
    "proofwiki[entities]": {
        "path": "ProofWiki/proofwiki[entities].pickle.gz",
        "url": BASE_URL + "proofwiki[entities].pickle.gz"
    }
}


class ProofWikiKB(KnowledgeBase):
    """
    Wrapper for the ProofWiki dataset (Ferreira et al., 2018): https://github.com/ai-systems/tg2022task_premise_retrieval
    """
    def __init__(self, path: str = PATH, url: str = URL):
        super().__init__(path, url)
        self.tokenizer = English().tokenizer
        self.id = PATH.split(".")[0]
        self.key_idx: dict[int, list[Statement]] = dict()
        if (not url):
            return

        with ZipFile(self.data_path) as dataset_file:
            self.data = list()

            with TextIOWrapper(dataset_file.open("ProofWiki/def_titles.txt"), encoding="utf-8") as ent_file:
                for line in ent_file:
                    ent = Entity(line.strip(), self.id)
                    self.entities.append(ent)

            with TextIOWrapper(dataset_file.open("ProofWiki/knowledge_base.json"), encoding="utf-8") as data_file:
                data = json.load(data_file)
                for key in tqdm(data, desc=f"Loading data [Knowledge Base]"):
                    self.key_idx[int(key)] = list()
                    stt = Statement(data[key].strip())
                    stt.annotations["split"] = "KB"
                    stt.annotations["type"] = "fact"
                    stt.annotations["id"] = int(key)

                    for tok in self.tokenizer(stt.surface):
                        token = Token()
                        token.surface = tok.text
                        stt.tokens.append(token)

                    self.data.append(stt)
                    self.key_idx[int(key)].append(stt)

            for split in ["train", "dev", "test"]:
                with TextIOWrapper(dataset_file.open(f"ProofWiki/{split}_set.json"), encoding="utf-8") as data_file:
                    data = json.load(data_file)
                    for key in tqdm(data, desc=f"Loading data [{split}]"):
                        self.key_idx[int(key)] = list()
                        stt = Statement(data[key]["text"].strip())
                        stt.annotations["split"] = split
                        stt.annotations["type"] = "proposition"
                        stt.annotations["id"] = int(key)
                        for prem_id in data[key]["premises"]:
                            if (prem_id in self.key_idx):
                                stt.premises.extend(self.key_idx[prem_id])

                        for tok in self.tokenizer(stt.surface):
                            token = Token()
                            token.surface = tok.text
                            stt.tokens.append(token)

                        self.data.append(stt)
                        self.key_idx[int(key)].append(stt)

        stt_text_l = [stt.surface.lower() for stt in self.data]
        for ent in tqdm(self.entities, desc="Searching entities"):
            ent_name = ent.surface.lower()
            stt_matches = [stt_idx for stt_idx, stt_txt in enumerate(stt_text_l)
                           if (ProofWikiKB.entity_name_search(ent_name,stt_txt))]
            for stt_idx in stt_matches:
                self.data[stt_idx].entities.append(ent)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int | slice) -> Statement | list[Statement]:
        """Fetches the ith statement in the KB.

        Args:
            idx (int): index for the ith term in the KB.

        :return: A single term definition (Statement).
        """
        if (isinstance(idx, slice)):
            item = self.data[idx]
        else:
            item = self.data[idx] if (idx < len(self)) else self.key_idx[idx]

        return item

    def keys(self):
        return self.key_idx.keys()

    @staticmethod
    def entity_name_search(ent_name: str, text: str) -> bool:
        if (ent_name in text):
            match = f" {ent_name} " in text or f"'{ent_name}'" in text or f'"{ent_name}"' in text
        else:
            match = False

        return match

    @staticmethod
    def from_resource(locator: str):
        """
        Downloads a pre-annotated resource available at the specified locator

        Example:
            >>> kb = ProofWikiKB.from_resource("proofwiki[entities]")
        """
        kb = None
        if (locator in ANNOT_RESOURCES):
            path = ANNOT_RESOURCES[locator]["path"]
            url = ANNOT_RESOURCES[locator]["url"]
            data_path = KnowledgeBase.download_resource(path, url)
            with gzip.open(data_path, "rb") as resource_file:
                kb = pickle.load(resource_file)
        else:
            print(f"No resource found at locator: {locator}")

        return kb


