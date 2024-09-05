# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EvaluationUpdateParams",
    "PartialPatchEvaluationRequest",
    "PartialPatchEvaluationRequestAnnotationConfig",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfig",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponent",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentItem",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest",
    "RestoreRequest",
]


class PartialPatchEvaluationRequest(TypedDict, total=False):
    annotation_config: PartialPatchEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_spec_id: str

    application_variant_id: str

    description: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_type: Literal["llm_benchmark"]
    """
    If llm_benchmark is provided, the evaluation will be updated to a hybrid
    evaluation. No-op on existing hybrid evaluations, and not available for studio
    evaluations.
    """

    name: str

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    tags: object


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponent(TypedDict, total=False):
    item: Required[PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentItem]

    comparison: PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest(TypedDict, total=False):
    messages_loc: Required[List[str]]


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest(TypedDict, total=False):
    document_loc: Required[List[str]]

    summary_loc: Required[List[str]]

    expected_summary_loc: List[str]


PartialPatchEvaluationRequestAnnotationConfig: TypeAlias = Union[
    PartialPatchEvaluationRequestAnnotationConfigAnnotationConfig,
    PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigMultiturnUseCaseRequest,
    PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigSummarizationUseCaseRequest,
]


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


EvaluationUpdateParams: TypeAlias = Union[PartialPatchEvaluationRequest, RestoreRequest]
