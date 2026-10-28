"""Data model for a layered, provenance-backed government process map.

Layers (each node/edge/rule can be read at any of them):
  - Service   : CPSV-AP-aligned description of the public service (what, for whom, by whom, legal basis)
  - Process   : BPMN-aligned control flow — nodes are steps/decisions/events, edges are sequence flows
  - Rules     : DMN / rules-as-code-aligned decision logic, each rule tied to its legal basis
  - Data      : data objects (inputs the citizen supplies) and the registers/systems they come from
  - Provenance: every claim above carries verbatim quotes with a locator into a named source

The agent-operable spec is not a separate artefact: it is the `automation_class` / `agent_mode`
annotation on every node, plus the rules and data sources it references.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

Layer = Literal["catalogue", "legislation", "guidance", "forms", "internal", "statistics", "appeals"]
SourceKind = Literal["ptv_api", "akn_xml", "html", "pdf"]
Grounding = Literal["documented", "inferred", "unknown"]


# --------------------------------------------------------------------------------------
# Sources and evidence
# --------------------------------------------------------------------------------------

class Source(BaseModel):
    id: str
    title: str
    url: str
    kind: SourceKind
    layer: Layer
    publisher: str
    language: str
    fetched_at: str = ""
    chars: int = 0
    sha256: str = ""


class Passage(BaseModel):
    source_id: str
    locator: str = Field(description="Where in the source: '§ 7', 'p. 3', '#anchor', 'H2: heading'")
    quote: str = Field(description="Verbatim passage from the source, in the source language")
    support: Literal["supports", "partial", "contradicts"] = "supports"
    verified: Optional[bool] = Field(default=None, description="True if quote exact-matches the source text")


# --------------------------------------------------------------------------------------
# Pass A output: atomic facts per source
# --------------------------------------------------------------------------------------

FactKind = Literal[
    "step", "actor", "eligibility", "calculation", "procedural_rule", "deadline",
    "input", "data_source", "channel", "output", "exception", "appeal", "volume",
]


class Fact(BaseModel):
    id: str = Field(description="Short unique id within this source, e.g. 'F12'")
    kind: FactKind
    statement: str = Field(description="One atomic claim in English about how the process works")
    quote: str = Field(description="Verbatim passage from the source that supports the statement (source language, no paraphrase)")
    locator: str = Field(description="The bracketed marker nearest above the quote, e.g. '§ 7' or 'p. 3' or 'H2: How to apply'")


class FactSheet(BaseModel):
    source_id: str
    facts: list[Fact]


# --------------------------------------------------------------------------------------
# Pass B output: the map (evidence given as fact ids; expanded into Evidence in code)
# --------------------------------------------------------------------------------------

class Actor(BaseModel):
    id: str
    name: str
    kind: Literal["citizen", "caseworker", "system", "third_party", "other_authority"]
    description: str = ""


class DataSource(BaseModel):
    id: str
    name: str
    owner: str = Field(description="Organisation that owns the register/system")
    access: Literal["api", "manual_lookup", "citizen_supplied", "unknown"]
    description: str = ""
    provenance_fact_ids: list[str] = []
    provenance: list[Passage] = []
    grounding: Grounding = "unknown"


class DataObject(BaseModel):
    id: str
    name: str
    description: str = ""
    provided_by: str = Field(description="Actor id or data source id that supplies it")


class RuleParameter(BaseModel):
    name: str
    value: str


class Rule(BaseModel):
    id: str
    name: str
    kind: Literal["eligibility", "calculation", "procedural", "deadline", "sanction"]
    logic: str = Field(description="Plain-language, testable statement of the rule (if/then, formula, threshold)")
    parameters: list[RuleParameter] = []
    provenance_fact_ids: list[str] = []
    provenance: list[Passage] = []
    grounding: Grounding = "unknown"
    validated: bool = False


NodeType = Literal[
    "start_event", "end_event", "citizen_task", "caseworker_task", "system_task",
    "third_party_task", "decision", "wait", "timer",
]
AutomationClass = Literal[
    "citizen_action",       # the citizen does something (fill form, upload document)
    "deterministic_rule",   # fully specified by a rule: compute, compare, route
    "register_lookup",      # fetch data from a register/system
    "document_check",       # read an unstructured document and extract/verify facts
    "judgment",             # discretionary assessment not fully specified by rules
    "human_signoff",        # a human must formally take the decision / sign
    "notification",         # inform a party (decision letter, request for info)
]
AgentMode = Literal["agent_can_execute", "agent_prepares_human_decides", "human_only"]


class Node(BaseModel):
    id: str
    name: str
    description: str = ""
    type: NodeType
    actor_id: str
    inputs: list[str] = Field(default=[], description="DataObject ids consumed")
    outputs: list[str] = Field(default=[], description="DataObject ids produced")
    data_source_ids: list[str] = []
    rule_ids: list[str] = []
    channel: Optional[str] = Field(default=None, description="e.g. OmaKela, paper form, service point, phone")
    time_limit: Optional[str] = Field(default=None, description="Statutory or administrative deadline that applies to this step")
    exceptions: list[str] = []
    visibility: Literal["external", "internal"] = Field(
        description="external: the citizen sees or does this step (apply, receive decision, report change). "
                    "internal: happens inside the authority (check, compute, decide, register)")
    automation_class: AutomationClass
    agent_mode: AgentMode
    agent_mode_reason: str = Field(default="", description="Why this agent mode: which rule makes it deterministic, or what requires human judgment")
    provenance_fact_ids: list[str] = []
    provenance: list[Passage] = []
    grounding: Grounding = "unknown"
    inferred_reason: str = Field(default="", description="If no provenance: why this step was added (e.g. needed to connect the flow)")
    confidence: float = Field(ge=0, le=1, description="Expected probability that this step matches how the process actually runs; see rubric in synthesis prompt")
    validated: bool = Field(default=False, description="Set to true by a responsible human after checking the step; validated steps run at 100%")


class Edge(BaseModel):
    id: str
    source: str
    target: str
    condition: Optional[str] = Field(default=None, description="Condition on this path, for edges leaving a decision")
    rule_id: Optional[str] = None
    provenance_fact_ids: list[str] = []
    provenance: list[Passage] = []
    grounding: Grounding = "unknown"


class ServiceInfo(BaseModel):
    id: str
    name_fi: str
    name_en: str
    competent_authority: str
    legal_basis: list[str] = Field(description="Acts and sections, e.g. 'Laki yleisestä asumistuesta 938/2014'")
    life_events: list[str] = []
    channels: list[str] = []
    outputs: list[str] = Field(default=[], description="What the citizen gets: decision, payment, ...")
    eligibility_summary: str = ""
    processing_time: Optional[str] = None


class OpenQuestion(BaseModel):
    question: str
    why_it_matters: str
    likely_source: str = Field(description="Where the answer probably lives: internal guideline, case system, appeals board, ...")


class ProcessMap(BaseModel):
    service: ServiceInfo
    actors: list[Actor]
    data_sources: list[DataSource]
    data_objects: list[DataObject]
    rules: list[Rule]
    nodes: list[Node]
    edges: list[Edge]
    open_questions: list[OpenQuestion] = Field(description="What the public record does not tell us about this process")
    sources: list[Source] = []
