import csv
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
                with open("diploma.csv", "r", encoding="utf-8", newline="") as file:
                    reader = csv.reader(file)

                    for values in reader:
                        diploma_data = values[:8]

                        if len(values) > 8:
                            university_data = values[8:]
                        else:
                            university_data = []

                        existing_diploma = (
                            session.query(AbschlussModel)
                            .filter_by(DiplomaName=diploma_data[0])
                            .first()
                        )

                        if existing_diploma:
                            continue

                        diploma_instance = AbschlussModel(
                            DiplomaName=diploma_data[0],
                            DiplomaType=diploma_data[1],
                            MinDuration=diploma_data[2],
                            MaxDuration=diploma_data[3],
                            Class=diploma_data[4],
                            Field=diploma_data[5],
                            Country=diploma_data[6],
                            GermanDegreeEquivalent=diploma_data[7],
                        )

                        if university_data:
                            universities = []
                            for university_name in university_data:
                                existing_university = (
                                    session.query(InstitutionModel)
                                    .filter_by(UniversityName=university_name)
                                    .first()
                                )
                                if existing_university:
                                    universities.append(existing_university)
                                else:
                                    new_university = InstitutionModel(
                                        UniversityName=university_name
                                    )
                                    universities.append(new_university)
                                    session.add(new_university)

                            diploma_instance.universities = universities

                        session.add(diploma_instance)

                session.commit()
            except FileNotFoundError as e:
                logging.error(f"Error Storing diploma data: {str(e)}")
            except SQLAlchemyError as e:
                logging.error(f"Error interacting with the database: {str(e)}")
