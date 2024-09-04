# MultiMolecule
# Copyright (C) 2024-Present  MultiMolecule

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from functools import cached_property
from typing import Any, List

import danling as dl
import datasets
import torch
from chanfig import NestedDict
from danling import NestedTensor
from torch import Tensor
from transformers import AutoTokenizer, PreTrainedTokenizerBase

from multimolecule import defaults
from multimolecule.tasks import Task

from .utils import infer_task


class Dataset(datasets.Dataset):
    r"""
    The base class for all datasets.

    Dataset is a subclass of [`datasets.Dataset`][] that provides additional functionality for handling structured data.
    It has three main features:

    - column identification: identify the special columns (sequence and structure columns) in the dataset.
    - tokenization: tokenize the sequence columns in the dataset using a pretrained tokenizer.
    - task inference: infer the task type and level of each label column in the dataset.

    Attributes:
        tasks: A nested dictionary of the inferred tasks for each label column in the dataset.
        tokenizer: The pretrained tokenizer to use for tokenization.
        truncation: Whether to truncate sequences that exceed the maximum length of the tokenizer.
        max_length: The maximum length of the input sequences.
        data_cols: The names of all columns in the dataset.
        feature_cols: The names of the feature columns in the dataset.
        label_cols: The names of the label columns in the dataset.
        sequence_cols: The names of the sequence columns in the dataset.
        structure_cols: The names of the structure columns in the dataset.
        column_names_map: A mapping of column names to new column names.
        preprocess: Whether to preprocess the dataset.

    Args:
        arrow_table: The arrow table containing the dataset.
        split: The split of the dataset.
        tokenizer: A pretrained tokenizer to use for tokenization.
            Either `tokenizer` or `pretrained` must be specified.
        pretrained: The name of a pretrained tokenizer to use for tokenization.
            Either `tokenizer` or `pretrained` must be specified.
        feature_cols: The names of the feature columns in the dataset.
            Will be inferred automatically if not specified.
        label_cols: The names of the label columns in the dataset.
            Will be inferred automatically if not specified.
        preprocess: Whether to preprocess the dataset.
            Preprocessing involves pre-tokenizing the sequences using the tokenizer.
            Defaults to `True`.
        auto_rename_cols: Whether to automatically rename columns to standard names.
            Only works when there is exactly one feature column / one label column.
            You can control the naming through `multimolecule.defaults.SEQUENCE_COL_NAME` and
            `multimolecule.defaults.LABEL_COL_NAME`.
            For more refined control, use `column_names_map`.
        column_names_map: A mapping of column names to new column names.
            This is useful for renaming columns to inputs that are expected by a model.
            Defaults to `None`.
        truncation: Whether to truncate sequences that exceed the maximum length of the tokenizer.
            Defaults to `False`.
        max_length: The maximum length of the input sequences.
            Defaults to the `model_max_length` of the tokenizer.
        info: The dataset info.
        indices_table: The indices table.
        fingerprint: The fingerprint of the dataset.
    """

    tokenizer: PreTrainedTokenizerBase
    truncation: bool = False
    max_length: int

    feature_cols: List
    label_cols: List

    data_cols: List
    sequence_cols: List
    structure_cols: List

    column_names_map: Mapping[str, str] | None = None
    preprocess: bool = True
    auto_rename_cols: bool = False

    def __init__(
        self,
        arrow_table: datasets.table.Table,
        split: datasets.NamedSplit,
        tokenizer: PreTrainedTokenizerBase | None = None,
        pretrained: str | None = None,
        feature_cols: List | None = None,
        label_cols: List | None = None,
        preprocess: bool | None = None,
        auto_rename_cols: bool | None = None,
        column_names_map: Mapping[str, str] | None = None,
        truncation: bool | None = None,
        max_length: int | None = None,
        info: datasets.DatasetInfo | None = None,
        indices_table: datasets.table.Table | None = None,
        fingerprint: str | None = None,
    ):
        super().__init__(
            arrow_table=arrow_table, split=split, info=info, indices_table=indices_table, fingerprint=fingerprint
        )
        if tokenizer is None:
            if pretrained is None:
                raise ValueError("tokenizer and pretrained can not be both None.")
            tokenizer = AutoTokenizer.from_pretrained(pretrained)
        if max_length is None:
            max_length = tokenizer.model_max_length
        else:
            tokenizer.model_max_length = max_length
        self.max_length = max_length
        if truncation is not None:
            self.truncation = truncation
        if preprocess is not None:
            self.preprocess = preprocess
        self.tokenizer = tokenizer
        self.post(
            feature_cols=feature_cols,
            label_cols=label_cols,
            auto_rename_cols=auto_rename_cols,
            column_names_map=column_names_map,
        )

    def post(
        self,
        feature_cols: List | None = None,
        label_cols: List | None = None,
        auto_rename_cols: bool | None = None,
        column_names_map: Mapping[str, str] | None = None,
    ) -> None:
        r"""
        Perform pre-processing steps after initialization.

        It first identifies the special columns (sequence and structure columns) in the dataset.
        Then it sets the feature and label columns based on the input arguments.
        If `auto_rename_cols` is `True`, it will automatically rename the columns to model inputs.
        Finally, it sets the [`transform`][datasets.Dataset.set_transform] function based on the `preprocess` flag.
        """
        self.identify_special_cols()
        data_cols = list(self._info.features.keys())
        if label_cols is None:
            if feature_cols is None:
                feature_cols = [i for i in data_cols if i in defaults.SEQUENCE_COL_NAMES]
            label_cols = [i for i in data_cols if i not in feature_cols]
        if feature_cols is None:
            feature_cols = [i for i in data_cols if i not in label_cols]
        missing_feature_cols = set(feature_cols).difference(data_cols)
        if missing_feature_cols:
            raise ValueError(f"{missing_feature_cols} are specified in feature_cols, but not found in dataset.")
        missing_label_cols = set(label_cols).difference(data_cols)
        if missing_label_cols:
            raise ValueError(f"{missing_label_cols} are specified in label_cols, but not found in dataset.")
        self.feature_cols = list(feature_cols)
        self.label_cols = list(label_cols)
        self.data_cols = self.feature_cols + self.label_cols

        if auto_rename_cols is not None:
            self.auto_rename_cols = auto_rename_cols
        if self.auto_rename_cols:
            if column_names_map is not None:
                raise ValueError("auto_rename_cols and column_names_map are mutually exclusive.")
            column_names_map = {}
            if len(self.feature_cols) == 1:
                column_names_map[self.feature_cols[0]] = defaults.SEQUENCE_COL_NAME
            if len(self.label_cols) == 1:
                column_names_map[self.label_cols[0]] = defaults.LABEL_COL_NAME
        self.column_names_map = column_names_map
        if self.column_names_map:
            self.rename_columns(self.column_names_map)

        if self.preprocess:
            self.update(self.map(self.tokenization))
            self.set_transform(self.torch_transform)
        else:
            self.set_transform(self.tokenize_transform)

    @cached_property
    def tasks(self) -> NestedDict:
        return self.infer_tasks()

    def torch_transform(self, batch: Mapping) -> Mapping:
        r"""
        Default [`transform`][datasets.Dataset.set_transform] function when `preprocess` is `True`.

        See Also:
            [`collate`](multimolecule.Dataset.collate)
        """
        return {k: self.collate(k, v) for k, v in batch.items()}

    def tokenize_transform(self, batch: Mapping) -> Mapping:
        r"""
        Default [`transform`][datasets.Dataset.set_transform] function when `preprocess` is `False`.

        See Also:
            [`collate`](multimolecule.Dataset.collate)
        """
        return {k: self.collate(k, v, tokenize=True) for k, v in batch.items()}

    def collate(self, col: str, data: Any, tokenize: bool = False) -> Tensor | NestedTensor | None:
        r"""
        Collate the data for a column.

        If the column is a sequence column, it will tokenize the data if `tokenize` is `True`.
        Otherwise, it will return a tensor or nested tensor.
        """
        if col in self.sequence_cols:
            if tokenize:
                data = self.tokenize(data)
            return dl.tensor(data) if len(data) == 1 else NestedTensor(data)
        try:
            return torch.tensor(data)
        except ValueError:
            return NestedTensor(data)

    def infer_tasks(self, sequence_col: str | None = None) -> NestedDict:
        return NestedDict({col: self.infer_task(col, sequence_col) for col in self.label_cols})

    def infer_task(self, label_col: str, sequence_col: str | None = None) -> Task:
        if sequence_col is None:
            if len(self.sequence_cols) != 1:
                raise ValueError("sequence_col must be specified if there are multiple sequence columns.")
            sequence_col = self.sequence_cols[0]
        sequence = self._data.column(sequence_col)
        column = self._data.column(label_col)
        # is_nested = isinstance(column.type, ListType)
        # if is_nested:
        #     column = column.combine_chunks().flatten()
        return infer_task(sequence, column)

    def __getitems__(self, key: int | slice | Iterable[int]) -> Any:
        return self.__getitem__(key)

    def identify_special_cols(self) -> Sequence:
        self.sequence_cols, self.structure_cols = [], []
        string_cols = [k for k, v in self.features.items() if v.dtype == "string"]
        for col in string_cols:
            unique_values = set()
            for chunk in self._data.column(col):
                unique_values.update(chunk.as_py())
            if unique_values == {"(", ".", ")"}:
                self.structure_cols.append(col)
            else:
                self.sequence_cols.append(col)
        return string_cols

    def tokenization(self, data: Mapping[str, str]) -> Mapping[str, Tensor]:
        return {col: self.tokenize(data[col]) for col in self.sequence_cols}

    def tokenize(self, string: str) -> Tensor:
        return self.tokenizer(string, return_attention_mask=False, truncation=self.truncation)["input_ids"]

    def update(self, dataset: datasets.Dataset):
        r"""
        Perform an in-place update of the dataset.

        This method is used to update the dataset after changes have been made to the underlying data.
        It updates the format columns, data, info, and fingerprint of the dataset.
        """
        # pylint: disable=W0212
        # Why datasets won't support in-place changes?
        # It's just impossible to extend.
        self._format_columns = dataset._format_columns
        self._data = dataset._data
        self._info = dataset._info
        self._fingerprint = dataset._fingerprint

    def rename_columns(self, column_mapping: Mapping[str, str], new_fingerprint: str | None = None) -> datasets.Dataset:
        self.update(super().rename_columns(column_mapping, new_fingerprint=new_fingerprint))
        self.feature_cols = [column_mapping.get(i, i) for i in self.feature_cols]
        self.label_cols = [column_mapping.get(i, i) for i in self.label_cols]
        self.sequence_cols = [column_mapping.get(i, i) for i in self.sequence_cols]
        self.structure_cols = [column_mapping.get(i, i) for i in self.structure_cols]
        return self

    def rename_column(
        self, original_column_name: str, new_column_name: str, new_fingerprint: str | None = None
    ) -> datasets.Dataset:
        self.update(super().rename_column(original_column_name, new_column_name, new_fingerprint))
        self.feature_cols = [new_column_name if i == original_column_name else i for i in self.feature_cols]
        self.label_cols = [new_column_name if i == original_column_name else i for i in self.label_cols]
        self.sequence_cols = [new_column_name if i == original_column_name else i for i in self.sequence_cols]
        self.structure_cols = [new_column_name if i == original_column_name else i for i in self.structure_cols]
        return self
