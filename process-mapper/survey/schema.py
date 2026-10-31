"""Data model for the public-record survey.

Three passes, each producing one JSON document per unit:

  country    survey/countries/<iso2>.json          what a country publishes, and the authorities to survey
  authority  survey/authorities/<iso2>/<id>.json   what one national authority publishes, and its services
  service    survey/services/<service_id>.json     candidate sources for one service (exported to services/<id>/sources.yaml)

Every pass scores the same seven layers the mapper uses for sources (catalogue, legislation,
guidance, forms, internal, statistics, appeals) on a 0-3 scale, with URLs as evidence:

  0  nothing found
  1  exists for some services or is hard to reach (scattered PDFs, no index, paywalled or stale)
  2  systematic for the main authorities or services, reachable by browsing
  3  systematic AND enumerable or machine-readable (API, sitemap, open-data dump, structured register)

The tier is computed in code from the layer scores (see `tier_for`), never by the model.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

Layer = Literal["catalogue", "legislation", "guidance", "forms", "internal", "statistics", "appeals"]
LAYERS: tuple[str, ...] = ("catalogue", "legislation", "guidance", "forms", "internal", "statistics", "appeals")
Score = int  # 0-3


class Evidence(BaseModel):
    claim: str = Field(description="One checkable statement, e.g. 'Finlex serves consolidated acts as Akoma Ntoso XML'")
    url: str
    layer: Optional[Layer] = None
    note: str = ""


class LayerScore(BaseModel):
    layer: Layer
    score: int = Field(ge=0, le=3)
    reason: str = Field(description="Why this score, naming the systems or document types found")
    evidence_urls: list[str] = []


class NamedSystem(BaseModel):
    """A website, register or portal that matters for one layer."""
    name: str
    url: str
    publisher: str = ""
    machine_readable: bool = Field(default=False, description="API, bulk download or structured XML/JSON")
    api_url: str = ""
    languages: list[str] = []
    note: str = ""


# --------------------------------------------------------------------------------------
# Country pass
# --------------------------------------------------------------------------------------

class LegalInformationSystem(NamedSystem):
    consolidated_texts: bool = Field(default=False, description="In-force consolidated versions, not only the original acts")
    consolidation_lag: str = Field(default="", description="How current the consolidation is, if known")
    covers_regulations: bool = Field(default=False, description="Secondary legislation / decrees / ministerial regulations included")
    format: Literal["akn_xml", "xml", "html", "pdf", "mixed", "unknown"] = "unknown"


class ServiceCatalogue(NamedSystem):
    scope: Literal["national", "national_and_subnational", "unknown"] = "unknown"
    record_count_estimate: Optional[int] = None
    fields_per_record: list[str] = Field(default=[], description="What a record holds: steps, forms, deadlines, legal basis, fees, responsible unit, channels ...")


class FoiRegime(BaseModel):
    law_exists: bool = False
    law_name: str = ""
    law_url: str = ""
    proactive_publication_duties: list[str] = Field(default=[], description="What bodies must publish without being asked, e.g. 'procedure descriptions with deadlines and forms' (Italy d.lgs 33/2013 art. 35)")
    procedure_publication_duty: bool = Field(default=False, description="True if the law obliges bodies to publish descriptions of their administrative procedures")
    disclosure_platforms: list[NamedSystem] = Field(default=[], description="Request platforms with public logs (Alaveteli instances, government disclosure logs)")


class AuthorityStub(BaseModel):
    """A national authority worth surveying in the authority pass."""
    id: str = Field(description="Short slug, ascii, e.g. 'kela', 'dwp', 'ssa'")
    name: str
    name_en: str = ""
    url: str
    domains: list[str] = Field(default=[], description="Policy domains: social_security, tax, pensions, health, immigration, business_registry, civil_registry, customs, employment, education, licences, housing, justice, other")
    delivers_services_to_public: bool = True
    note: str = ""


class CountryProfile(BaseModel):
    country_id: str = Field(description="ISO 3166-1 alpha-2, lower case")
    country_name: str
    surveyed_at: str = ""
    model: str = ""

    government_structure: str = Field(description="Unitary or federal; which tier delivers the main citizen services (benefits, permits, registrations)")
    official_languages: list[str] = []
    web_languages: list[str] = Field(default=[], description="Languages in which government sites publish")

    legal_information: list[LegalInformationSystem] = Field(default=[], description="Official legal databases and gazettes")
    catalogues: list[ServiceCatalogue] = Field(default=[], description="Service catalogues, procedure registers, single digital gateways")
    foi: FoiRegime = FoiRegime()
    internal_guidance_practice: str = Field(default="", description="Do major agencies publish staff instructions, decision-maker guides, procedure manuals? Name examples")
    internal_guidance_examples: list[NamedSystem] = []
    appeals_sources: list[NamedSystem] = Field(default=[], description="Court, tribunal and ombudsman decision databases that cover administrative decisions")
    audit_office: list[NamedSystem] = Field(default=[], description="Supreme audit institution and its report archive")
    statistics_sources: list[NamedSystem] = Field(default=[], description="Where administrative statistics on services live (volumes, processing times)")
    procurement_portals: list[NamedSystem] = Field(default=[], description="Public procurement portals where tender documents for case systems can be read")
    rules_as_code: list[NamedSystem] = Field(default=[], description="OpenFisca packages, published calculators, rule repositories")
    open_data_portals: list[NamedSystem] = []

    authorities: list[AuthorityStub] = Field(description="Every national authority that delivers services to people or firms; be exhaustive, this list drives the next pass")

    layer_scores: list[LayerScore] = Field(description="One entry per layer, all seven")
    evidence: list[Evidence] = Field(default=[], description="Claims with URLs that back the scores")
    best_documented_domains: list[str] = Field(default=[], description="Policy domains where the public record is richest")
    notes: str = ""
    open_questions: list[str] = Field(default=[], description="What this pass could not determine and where to look")


# --------------------------------------------------------------------------------------
# Authority pass
# --------------------------------------------------------------------------------------

class DocumentRepository(BaseModel):
    url: str
    enumerable: bool = Field(description="Listing, sitemap, search with pagination, or predictable ids")
    formats: list[str] = []
    approx_documents: Optional[int] = None
    note: str = ""


class PublishedDocument(BaseModel):
    title: str
    url: str
    kind: str = Field(description="staff_manual, procedure_note, decision_maker_guide, system_description, audit_report, ombudsman_decision, tribunal_decision, annual_report, statistics, tender_spec, foi_release, other")
    layer: Layer
    language: str = ""
    note: str = ""


class ServiceStub(BaseModel):
    id: str = Field(description="Slug: <iso2>-<authority>-<service>, ascii, e.g. 'fi-kela-general-housing-allowance'")
    name: str
    name_en: str = ""
    url: str = Field(description="The main guidance page for the service")
    legal_basis: list[str] = []
    domain: str = ""
    note: str = ""


class AuthorityProfile(BaseModel):
    country_id: str
    authority_id: str
    name: str
    name_en: str = ""
    url: str
    surveyed_at: str = ""
    model: str = ""

    domains: list[str] = []
    document_repositories: list[DocumentRepository] = []
    internal_documents: list[PublishedDocument] = Field(default=[], description="Staff instructions, procedure notes, decision-maker guides, system descriptions found")
    forms_library: list[NamedSystem] = []
    statistics: list[PublishedDocument] = []
    appeals: list[NamedSystem] = Field(default=[], description="Where decisions about this authority's cases are published")
    audit_and_oversight: list[PublishedDocument] = []
    foi_releases: list[PublishedDocument] = []
    procurement_documents: list[PublishedDocument] = []

    services: list[ServiceStub] = Field(description="Every service this authority delivers to people or firms; exhaustive")
    services_count_estimate: Optional[int] = Field(default=None, description="If the list is cut short, the estimated total")

    layer_scores: list[LayerScore]
    evidence: list[Evidence] = []
    notes: str = ""
    open_questions: list[str] = []


# --------------------------------------------------------------------------------------
# Service pass: candidate sources, exported to services/<id>/sources.yaml
# --------------------------------------------------------------------------------------

FetchKind = Literal["html", "pdf", "akn_xml", "ptv_api", "api_json", "xml", "docx", "other"]


class CandidateSource(BaseModel):
    id: str = Field(description="Short slug unique within the service, e.g. 'law-938-2014', 'kela-form-AT1e'")
    title: str
    url: str
    kind: FetchKind
    layer: Layer
    publisher: str
    language: str
    why: str = Field(default="", description="What this source is expected to contribute: steps, parameters, inputs, internal automation, deadlines ...")
    currency: str = Field(default="", description="Date or version if visible; note if stale")


class ServiceSourceSet(BaseModel):
    service_id: str
    service_name: str
    service_name_en: str = ""
    country_id: str
    authority_id: str
    authority_name: str
    surveyed_at: str = ""
    model: str = ""

    sources: list[CandidateSource] = Field(description="Every public document that describes how the service runs; exhaustive, all languages")
    layer_scores: list[LayerScore]
    missing: list[str] = Field(default=[], description="Document types that should exist but were not found, and where they might be")
    notes: str = ""


# --------------------------------------------------------------------------------------
# Tiering (deterministic)
# --------------------------------------------------------------------------------------

def scores_dict(layer_scores: list[LayerScore]) -> dict[str, int]:
    d = {l: 0 for l in LAYERS}
    for ls in layer_scores:
        d[ls.layer] = max(d[ls.layer], ls.score)
    return d


def tier_for(scores: dict[str, int]) -> int:
    """Map layer scores to the expected map quality.

    0  no map: law or guidance missing
    1  external skeleton: law and guidance; internal steps inferred
    2  full external process: plus forms and (appeals or catalogue)
    3  internal steps documented: plus internal >= 2 and (statistics or appeals >= 2)
    4  refreshable: tier 3 plus machine-readable law and catalogue
    """
    s = scores
    if s["legislation"] < 1 or s["guidance"] < 1:
        return 0
    if s["forms"] < 1 or max(s["appeals"], s["catalogue"]) < 1:
        return 1
    if s["internal"] < 2 or max(s["statistics"], s["appeals"] - 1) < 1:
        return 2
    if s["legislation"] >= 3 and s["catalogue"] >= 3:
        return 4
    return 3


TIER_LABELS = {
    0: "no map",
    1: "external skeleton",
    2: "full external process",
    3: "internal steps documented",
    4: "refreshable",
}
