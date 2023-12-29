from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("postgresql://postgres:1598753@localhost/me")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

association_table = Table(
    "abschluss_institution_association",
    Base.metadata,
    Column("Abschluss", String, ForeignKey("abschluss.Abschluss")),
    Column("Institution", String, ForeignKey("institution.Institution")),
)


class InstitutionModel(Base):
    __tablename__ = "institution"

    institution_id = Column(Integer, primary_key=True, autoincrement=True)
    Institution = Column(String, unique=True)
    Ort = Column(String)
    Institutiontyp = Column(String)
    Status = Column(String)
    Land = Column(String)
    Gehort_zur_Institution = Column(String, nullable=True)

    abschlussu = relationship(
        "AbschlussModel", secondary=association_table, back_populates="institutions"
    )
    pdf_institution = relationship("PDFInstitutionModel", back_populates="Institution")


class PDFInstitutionModel(Base):
    __tablename__ = "pdfinstitutionmodel"

    pdf_id = Column(Integer, primary_key=True, autoincrement=True)
    Land = Column(String, nullable=True)
    Bildungsinstitution = Column(String, nullable=True)
    Langname = Column(String, nullable=True)
    Abkurzung = Column(String, nullable=True)
    Anschrift = Column(String, nullable=True)
    Telefon = Column(String, nullable=True)
    Fax = Column(String, nullable=True)
    Email = Column(String, nullable=True)
    Homepage = Column(String, nullable=True)
    Kommentar = Column(String, nullable=True)
    Aliasname = Column(String, nullable=True)
    Aliasname2 = Column(String, nullable=True)
    Englisch = Column(String, nullable=True)
    Arabisch = Column(String, nullable=True)
    status_Kommentar = Column(String, nullable=True)

    Institution = Column(Integer, ForeignKey("institution.Institution"))
    Institution = relationship("InstitutionModel", back_populates="pdf_institution")


class AbschlussModel(Base):
    __tablename__ = "abschluss"

    abschluss_id = Column(Integer, primary_key=True, autoincrement=True)
    Abschluss = Column(String, unique=True)
    Abschlusstyp = Column(String, nullable=True)
    Dauer_min = Column(String, nullable=True)
    Dauer_max = Column(String, nullable=True)
    Klasse = Column(String, nullable=True)
    Studienrichtung = Column(String, nullable=True)
    Land = Column(String, nullable=True)

    institutions = relationship(
        "InstitutionModel", secondary=association_table, back_populates="abschlussu"
    )
    pdf_diplomas = relationship("PDFDiplomaModel", back_populates="Abschluss")


class PDFDiplomaModel(Base):
    __tablename__ = "pdfdiplomamodel"

    pdf_id = Column(Integer, primary_key=True, autoincrement=True)
    Abschluss_deutsche_Ubersetzung = Column(String, nullable=True)
    Abkurzung = Column(String, nullable=True)
    Kommentar = Column(String, nullable=True)
    Andere_Bezeichnung_für_diesen_Abschluss = Column(String, nullable=True)
    Sprache = Column(String, nullable=True)
    Aquivalenzklasse = Column(String, nullable=True)
    Entsprechender_dt_Abschlusstyp = Column(String, nullable=True)
    Kommentar1 = Column(String, nullable=True)

    Abschluss = Column(Integer, ForeignKey("abschluss.Abschluss"))
    Abschluss = relationship("DiplomaModel", back_populates="pdf_diplomas")


def create_session():
    return Session()


try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating tables: {str(e)}")
