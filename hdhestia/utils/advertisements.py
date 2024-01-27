from hdmdata.types.get_by_type import by_
from hdmdata.schemas.advertisements import RentOfficeSchema
from hdmdata.models.advertisements import RentOffice
from sqlalchemy import Result


class RentOfficeProcessor:
    def __init__(self, rent_office_list: list):
        self._rent_office_list = iter(rent_office_list)
        self._test = rent_office_list
        self._current_rent_office = None
        self._bulk_ready = []

    @property
    def rent_office(self):
        return self._current_rent_office

    @property
    def ready(self):
        return self._bulk_ready

    def next_rent_office(self) -> RentOfficeSchema | None:
        if rent_office := next(self._rent_office_list, None):
            self._current_rent_office = RentOfficeSchema(**rent_office)
            return self._current_rent_office

    def has_rent_office(self, rent_office: RentOfficeSchema) -> Result | RentOfficeSchema:
        by = by_(column="title", value=rent_office.title)
        result = rent_office.get(by)
        if result:
            return result[0][0]

    def add_rent_office_to_advert(self, office: RentOffice) -> None:
        advertisements = []
        for adverisement in office.advertisements:
            adverisement.rent_office = office
            adverisement.rent_office_id = office.id
            advertisements.append(adverisement)
        self._bulk_ready.extend(advertisements)

    def process(self) -> list:
        while rent_office := self.next_rent_office():
            if db_rent_office := self.has_rent_office(rent_office):
                self.add_rent_office_to_advert(db_rent_office)
                continue
            rent_office.save()
        return self.ready
