from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
import json
from datetime import datetime

from app.database import get_db, engine
from app.dependencies import require_admin

router = APIRouter(
    prefix="/api/backup",
    tags=["Database Backup & Maintenance"],
    dependencies=[Depends(require_admin)] # Wajib Admin
)

@router.get("/export-json", summary="Download seluruh data tabel dalam format JSON")
def export_database_json(db: Session = Depends(get_db)):
    """
    Mengekstrak seluruh isi tabel database ke dalam satu file JSON.
    Sangat cocok untuk migrasi data atau cadangan data berkala.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "tables": {}
    }
    
    for table_name in table_names:
        result = db.execute(text(f'SELECT * FROM "{table_name}"'))
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        
        # Konversi tipe data yang tidak serializable (date/datetime/uuid/decimal) ke string
        for row in rows:
            for k, v in row.items():
                if hasattr(v, 'isoformat'):
                    row[k] = v.isoformat()
                elif isinstance(v, (bytes, bytearray)):
                    row[k] = str(v)
                elif v is not None and not isinstance(v, (int, float, str, bool, list, dict)):
                    row[k] = str(v)
                    
        backup_data["tables"][table_name] = rows

    json_str = json.dumps(backup_data, indent=2, default=str)
    filename = f"backup_school_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
