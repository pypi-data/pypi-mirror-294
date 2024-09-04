from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt


class DefaultDates(BaseModel):
    ActivationDate: date
    DeactivationDate: date


class PostalAddress(BaseModel):
    StandardAddressIdentifier: Optional[str]
    PostalCode: Optional[PositiveInt]
    DistrictName: Optional[str]
    MunicipalityCode: Optional[PositiveInt]
    CountryIdentificationCode: Optional[str]


class ContactInformation(BaseModel):
    TelephoneNumberIdentifier: Optional[List[str]]
    EmailAddressIdentifier: Optional[List[str]]


class Department(DefaultDates):
    DepartmentIdentifier: str
    DepartmentLevelIdentifier: str
    DepartmentName: Optional[str]
    DepartmentUUIDIdentifier: Optional[UUID]
    PostalAddress: Optional[PostalAddress]
    ProductionUnitIdentifier: Optional[int]


class EmploymentStatus(DefaultDates):
    # TODO: add constraint
    EmploymentStatusCode: str


class EmploymentDepartment(DefaultDates):
    DepartmentIdentifier: str
    DepartmentUUIDIdentifier: Optional[UUID]


class Profession(DefaultDates):
    JobPositionIdentifier: int
    EmploymentName: Optional[str]
    AppointmentCode: Optional[str]


class Employment(BaseModel):
    # TODO: add missing fields
    EmploymentIdentifier: str
    EmploymentDate: date
    AnniversaryDate: date
    EmploymentStatus: EmploymentStatus
    EmploymentDepartment: Optional[EmploymentDepartment]
    Profession: Optional[Profession]


class EmploymentWithLists(BaseModel):
    # TODO: add missing fields
    EmploymentIdentifier: str
    EmploymentDate: Optional[date]
    AnniversaryDate: Optional[date]
    EmploymentStatus: Optional[List[EmploymentStatus]]
    EmploymentDepartment: Optional[List[EmploymentDepartment]]
    Profession: Optional[List[Profession]]


class EmploymentPerson(BaseModel):
    """
    An SD (GetEmployment) person... can maybe be generalized
    """

    # TODO: add constraint
    PersonCivilRegistrationIdentifier: str
    Employment: List[Employment]


class PersonEmployment(BaseModel):
    EmploymentIdentifier: Optional[str]
    ContactInformation: Optional[ContactInformation]


class Person(BaseModel):
    """
    An SD (GetPerson, GetPersonChangedAtDate) person.
    """

    PersonCivilRegistrationIdentifier: str
    PersonGivenName: Optional[str]
    PersonSurnameName: Optional[str]

    PostalAddress: Optional[PostalAddress]
    ContactInformation: Optional[ContactInformation]

    Employment: List[PersonEmployment]


class EmploymentPersonWithLists(BaseModel):
    """
    An SD (GetEmployment) person... can maybe be generalized
    """

    # TODO: add constraint
    PersonCivilRegistrationIdentifier: str
    Employment: List[EmploymentWithLists]


class GetDepartmentResponse(BaseModel):
    """
    Response model for SDs GetDepartment20111201
    """

    # TODO: add missing fields
    RegionIdentifier: str
    RegionUUIDIdentifier: Optional[UUID]
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: Optional[UUID]
    Department: List[Department]


class GetEmploymentResponse(BaseModel):
    """
    Response model for SDs GetEmployment20111201
    """

    Person: List[EmploymentPerson] = []


class GetEmploymentChangedResponse(BaseModel):
    """
    Response model for SDs GetEmploymentChanged20111201
    """

    Person: List[EmploymentPersonWithLists] = []


class GetEmploymentChangedAtDateResponse(GetEmploymentChangedResponse):
    """
    Response model for SDs GetEmploymentChangedAtDate20111201
    """

    pass


class GetPersonChangedAtDateResponse(BaseModel):
    """
    Response model for SDs GetPersonChangedAtDate20111201
    """

    Person: List[Person] = []


class DepartmentLevelReference(BaseModel):
    DepartmentLevelIdentifier: str | None = None
    DepartmentLevelReference: DepartmentLevelReference | None = None
    # TODO: add validator?


class DepartmentReference(BaseModel):
    DepartmentIdentifier: str
    DepartmentUUIDIdentifier: UUID | None = None
    DepartmentLevelIdentifier: str
    DepartmentReference: list[DepartmentReference] = []


class OrganizationModel(DefaultDates):
    DepartmentReference: list[DepartmentReference] = []


class GetOrganizationResponse(BaseModel):
    """
    Response model for SDs GetOrganisation20111201
    """

    RegionIdentifier: str
    RegionUUIDIdentifier: UUID | None = None
    InstitutionIdentifier: str
    InstitutionUUIDIdentifier: UUID | None = None
    DepartmentStructureName: str

    OrganizationStructure: DepartmentLevelReference
    Organization: list[OrganizationModel] = []


class DepartmentParent(BaseModel):
    DepartmentUUIDIdentifier: UUID


class GetDepartmentParentResponse(BaseModel):
    """
    Response model for SDs GetDepartmentParent20190701
    """

    DepartmentParent: DepartmentParent
