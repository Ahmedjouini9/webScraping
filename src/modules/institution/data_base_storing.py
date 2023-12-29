import logging
from MyProject.src.core.data_base import (
    AbschlussModel,
    InstitutionModel,
    create_session,
)
from sqlalchemy.exc import SQLAlchemyError


class Storing:
    def store_data(self):
        with create_session() as session:
            try:
                with open("Institution.txt", "r", encoding="utf-8") as file:
                    data = file.readlines()

                for line in data:
                    values = line.strip().split("|")
                    institution_data = values[:8]

                    if len(values) > 8:
                        diploma_data = values[8:]
                    else:
                        diploma_data = []

                    existing_institution = (
                        session.query(InstitutionModel)
                        .filter_by(DiplomaName=institution_data[0])
                        .first()
                    )

                    if existing_institution:
                        continue

                    institution_instance = InstitutionModel(
                        University=institution_data[0],
                        DiplomaType=institution_data[1],
                        MinDuration=institution_data[2],
                        MaxDuration=institution_data[3],
                        Class=institution_data[4],
                        Field=institution_data[5],
                        Country=institution_data[6],
                        GermanDegreeEquivalent=institution_data[7],
                    )

                    if diploma_data:
                        diploma_list = []
                        for diploma_name in diploma_data:
                            existing_university = (
                                session.query(InstitutionModel)
                                .filter_by(UniversityName=diploma_name)
                                .first()
                            )
                            if existing_university:
                                diploma_list.append(existing_university)
                            else:
                                new_university = AbschlussModel(
                                    UniversityName=diploma_name
                                )
                                diploma_list.append(new_university)
                                session.add(new_university)

                        institution_instance.universities = diploma_list

                    session.add(institution_instance)

                session.commit()
            except FileNotFoundError as e:
                logging.error(f"Error reading file: {str(e)}")
            except SQLAlchemyError as e:
                logging.error(f"Error interacting with the database: {str(e)}")
