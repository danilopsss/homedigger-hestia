from hdmdata.types.get_by_type import by_
from hdmdata.schemas.advertisements import RentOfficeSchema, AdvertisementsSchema
from hdmdata.models.advertisements import RentOffice
from sqlalchemy import Result


class RentOfficeProcessor:
    def __init__(self, real_state_agency: list):
        self._real_state_agency = real_state_agency

    @property
    def real_state_agency(self):
        return self._real_state_agency

    def has_rent_office(self, rent_office: RentOfficeSchema) -> Result | RentOfficeSchema:
        by = by_(column="title", value=rent_office.title)
        result = rent_office.get(by)
        if result:
            return result[0][0]

    def add_rent_office_to_advert(self, office: RentOffice, adverts: list) -> None:
        model_adverts_list = []
        for adv in adverts:
            adv_model = adv.to_dbmodel()
            adv_model.rent_office = office
            adv_model.rent_office_id = office.id
            model_adverts_list.append(adv_model)
        return model_adverts_list

    def process(self) -> list:
        advertisings = []
        for _, real_state_agency in self.real_state_agency.items():
            if not (db_rent_office := self.has_rent_office(real_state_agency)):
                real_state_agency.save()
            else:
                advertisings.extend(
                    self.add_rent_office_to_advert(db_rent_office, real_state_agency.advertisements)
                )
        return advertisings
