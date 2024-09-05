# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EvaluationCreateParams",
    "EvaluationBuilderRequest",
    "EvaluationBuilderRequestAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest",
    "DefaultEvaluationRequest",
    "DefaultEvaluationRequestAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest",
]


class EvaluationBuilderRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    application_variant_id: Required[str]

    description: Required[str]

    evaluation_dataset_id: Required[str]

    name: Required[str]

    annotation_config: EvaluationBuilderRequestAnnotationConfig
    """Annotation configuration for tasking"""

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_dataset_version: int

    tags: object

    type: Literal["builder"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent(TypedDict, total=False):
    item: Required[EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem]

    comparison: EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison


class EvaluationBuilderRequestAnnotationConfigAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest(TypedDict, total=False):
    messages_loc: Required[List[str]]


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest(TypedDict, total=False):
    document_loc: Required[List[str]]

    summary_loc: Required[List[str]]

    expected_summary_loc: List[str]


EvaluationBuilderRequestAnnotationConfig: TypeAlias = Union[
    EvaluationBuilderRequestAnnotationConfigAnnotationConfig,
    EvaluationBuilderRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest,
    EvaluationBuilderRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest,
]


class DefaultEvaluationRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    description: Required[str]

    name: Required[str]

    annotation_config: DefaultEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_variant_id: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    tags: object

    type: Literal["default"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent(TypedDict, total=False):
    item: Required[DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem]

    comparison: DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison


class DefaultEvaluationRequestAnnotationConfigAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest(TypedDict, total=False):
    messages_loc: Required[List[str]]


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest(TypedDict, total=False):
    document_loc: Required[List[str]]

    summary_loc: Required[List[str]]

    expected_summary_loc: List[str]


DefaultEvaluationRequestAnnotationConfig: TypeAlias = Union[
    DefaultEvaluationRequestAnnotationConfigAnnotationConfig,
    DefaultEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest,
    DefaultEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest,
]

EvaluationCreateParams: TypeAlias = Union[EvaluationBuilderRequest, DefaultEvaluationRequest]
