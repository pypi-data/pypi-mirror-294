# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum


class ComparisonOperationType(Enum):
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_EQUAL = "greater_than_or_equal_to"
    LESS_EQUAL = "less_than_or_equal_to"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"


ITERABLE_COMPARISON_OPERATION_TYPES = [
    ComparisonOperationType.IN,
    ComparisonOperationType.NOT_IN,
]

LIST_TYPE_COMPATIBLE_TYPES = ITERABLE_COMPARISON_OPERATION_TYPES + [
    ComparisonOperationType.CONTAINS,
    ComparisonOperationType.NOT_CONTAINS,
]
