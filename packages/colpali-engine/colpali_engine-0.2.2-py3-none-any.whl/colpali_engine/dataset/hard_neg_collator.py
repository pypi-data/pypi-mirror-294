from random import randint

from datasets import Dataset, DatasetDict
from transformers import PreTrainedTokenizer, ProcessorMixin

from .custom_collator import CustomCollator


class HardNegCollator(CustomCollator):
    def __init__(
        self,
        processor: ProcessorMixin = None,
        tokenizer: PreTrainedTokenizer = None,
        max_length: int = 2048,
        add_suffix: bool = True,
        image_dataset: Dataset = None,
    ):
        super().__init__(processor, tokenizer, max_length, add_suffix)
        self.image_dataset = image_dataset
        assert self.image_dataset is not None, "image_dataset must be provided"

    def get_image_from_image_dataset(self, image_idx):
        return self.image_dataset[int(image_idx)]["image"]

    def __call__(self, examples):
        # assert len(examples) == 1, "HardNegCollator only supports a single example at at time"

        tmp_examples = examples
        examples = []
        for example in tmp_examples:
            pos_image = self.get_image_from_image_dataset(example["gold_index"])
            pos_query = example["query"]
            # randomly sample a negative image amongst the top 10
            neg_image = self.get_image_from_image_dataset(example["negs"][randint(0, 9)])
            examples += [{"image": pos_image, "query": pos_query, "neg_image": neg_image}]

        # reorder examples
        if self.processor is None:
            return self.forward_text(examples)
        if self.processor.__class__.__name__ == "Idefics2Processor":
            return self.forward_vision_idefics(examples)
        if self.processor.__class__.__name__ == "PaliGemmaProcessor":
            return self.forward_vision_pali(examples)
        if self.processor.__class__.__name__ == "SiglipProcessor":
            return self.forward_vision_siglip(examples)
        raise ValueError("Processor not supported")
