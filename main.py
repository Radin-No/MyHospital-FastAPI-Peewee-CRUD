from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from peewee import IntegrityError
from models import Doctor, Patient, ContractPharma, Med, Prescription, PrescriptionItem

app = FastAPI(title="Hospital Management Test System")

class DoctorData(BaseModel):
    name: str
    specialty: str

class PatientData(BaseModel):
    name: str
    illness: str

class PharmaData(BaseModel):
    name: str
    location: str

class MedData(BaseModel):
    pharr_id: int
    name: str
    is_pill: int
    stock: int
    price: float

class PrescriptionData(BaseModel):
    doc_id: int
    pat_id: int
    phar_id: int
    date: str
    is_done: int

class ItemData(BaseModel):
    prescr_id: int
    med_id: int
    cons_instr: str

MODEL_MAP = {
    "doctors": (Doctor, DoctorData), "patients": (Patient, PatientData),
    "contract_pharma": (ContractPharma, PharmaData), "meds": (Med, MedData),
    "prescription": (Prescription, PrescriptionData),
    "prescription_items": (PrescriptionItem, ItemData),
}

def table_info(table):
    if table not in MODEL_MAP:
        raise HTTPException(status_code=404, detail="Table not found")
    return MODEL_MAP[table]

def values(table, data):
    try:
        return table_info(table)[1](**data).model_dump()
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors(include_url=False, include_context=False))

def record_data(record):
    return {field.column_name: record.__data__[field.name] for field in record._meta.sorted_fields}

def get_record(model, id):
    record = model.get_or_none(model.id == id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.get("/")
def home():
    return {"tables": list(MODEL_MAP)}

@app.get("/{table}")
def index(table: str):
    model, _ = table_info(table)
    return [record_data(r) for r in model.select().order_by(model.id.desc())]

@app.get("/{table}/{id}")
def details(table: str, id: int):
    model, _ = table_info(table)
    return record_data(get_record(model, id))

@app.post("/{table}", status_code=201)
def create(table: str, data: dict):
    model, _ = table_info(table)
    try:
        return record_data(model.create(**values(table, data)))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid related record")

@app.put("/{table}/{id}")
def update(table: str, id: int, data: dict):
    model, _ = table_info(table)
    record = get_record(model, id)
    for key, value in values(table, data).items():
        setattr(record, key, value)
    try:
        record.save()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid related record")
    return record_data(record)

@app.delete("/{table}/{id}")
def delete(table: str, id: int):
    model, _ = table_info(table)
    record = get_record(model, id)
    record.delete_instance()
    return {"deleted": id}
