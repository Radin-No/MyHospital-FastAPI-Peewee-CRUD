import os
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    FloatField,
    ForeignKeyField
)


db = SqliteDatabase(os.path.join(os.path.dirname(__file__), 'Test_DB.db'), pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Doctor(BaseModel):
    name = CharField()
    specialty = CharField()

    class Meta:
        table_name = "doctors"


class Patient(BaseModel):
    name = CharField()
    illness = CharField()

    class Meta:
        table_name = "patients"


class ContractPharma(BaseModel):
    name = CharField()
    location = CharField()

    class Meta:
        table_name = "contract_pharma"


class Med(BaseModel):
    pharr = ForeignKeyField(ContractPharma, column_name="pharr_id", backref="meds", on_delete="CASCADE")
    name = CharField()
    is_pill = IntegerField()
    stock = IntegerField()
    price = FloatField()

    class Meta:
        table_name = "meds"


class Prescription(BaseModel):
    doc = ForeignKeyField(Doctor, column_name="doc_id", backref="prescriptions", on_delete="CASCADE")
    pat = ForeignKeyField(Patient, column_name="pat_id", backref="prescriptions", on_delete="CASCADE")
    phar = ForeignKeyField(ContractPharma, column_name="phar_id", backref="prescriptions", on_delete="CASCADE")
    date = CharField()
    is_done = IntegerField()

    class Meta:
        table_name = "prescription"


class PrescriptionItem(BaseModel):
    prescr = ForeignKeyField(Prescription, column_name="prescr_id", backref="items", on_delete="CASCADE")
    med = ForeignKeyField(Med, column_name="med_id", backref="prescription_items", on_delete="CASCADE")
    cons_instr = CharField()

    class Meta:
        table_name = "prescription_items"


db.create_tables([
    Doctor,
    Patient,
    ContractPharma,
    Med,
    Prescription,
    PrescriptionItem
], safe=True)


def seed_data():
    if Doctor.select().count() > 0:
        return

    with db.atomic():
        doc1 = Doctor.create(name="Dr. Smith", specialty="Cardiology")
        Doctor.create(name="Dr. Johnson", specialty="Neurology")

        pat1 = Patient.create(name="Alex", illness="Hypertension")
        Patient.create(name="Rico", illness="Migraine")

        pharma1 = ContractPharma.create(name="PharmaPlus", location="3rd Street")

        med1 = Med.create(pharr=pharma1, name="Aspirin", is_pill=1, stock=100, price=5.99)
        Med.create(pharr=pharma1, name="Ibuprofen", is_pill=1, stock=50, price=8.50)

        presc1 = Prescription.create(doc=doc1, pat=pat1, phar=pharma1, date="2026-10-07", is_done=0)

        PrescriptionItem.create(prescr=presc1, med=med1, cons_instr="Once daily with food")


seed_data()