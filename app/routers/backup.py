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
    tags=["Database Backup and Maintenance"],
    dependencies=[Depends(require_admin)]
)

@router.get("/stats", summary="Statistik Data Tabel Database")
def get_database_stats(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    tables_stats = []
    total_records = 0
    
    for table_name in sorted(table_names):
        try:
            res = db.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
            count = int(res) if res is not None else 0
        except Exception:
            count = 0
        total_records += count
        tables_stats.append({
            "table_name": table_name,
            "row_count": count
        })
        
    return {
        "total_tables": len(table_names),
        "total_records": total_records,
        "generated_at": datetime.now().isoformat(),
        "tables": tables_stats
    }

@router.get("/export-json", summary="Download seluruh data tabel dalam format JSON")
def export_database_json(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tables": len(table_names),
        "tables": {}
    }
    
    for table_name in sorted(table_names):
        try:
            result = db.execute(text(f'SELECT * FROM "{table_name}"'))
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            
            for row in rows:
                for k, v in row.items():
                    if hasattr(v, 'isoformat'):
                        row[k] = v.isoformat()
                    elif isinstance(v, (bytes, bytearray)):
                        row[k] = str(v)
                    elif v is not None and not isinstance(v, (int, float, str, bool, list, dict)):
                        row[k] = str(v)
                        
            backup_data["tables"][table_name] = rows
        except Exception as e:
            backup_data["tables"][table_name] = {"error": str(e)}

    json_str = json.dumps(backup_data, indent=2, default=str)
    filename = f"backup_school_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    return Response(
        content=json_str,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.get("/export-sql", summary="Download seluruh data database dalam format SQL Dump")
def export_database_sql(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    sql_lines = []
    sql_lines.append("-- =====================================================")
    sql_lines.append("-- Database Backup (SQL Export)")
    sql_lines.append(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sql_lines.append(f"-- Total Tables: {len(table_names)}")
    sql_lines.append("-- =====================================================\n")
    sql_lines.append("BEGIN TRANSACTION;\n")
    
    for table_name in sorted(table_names):
        try:
            result = db.execute(text(f'SELECT * FROM "{table_name}"'))
            columns = list(result.keys())
            rows = result.fetchall()
            
            sql_lines.append(f"-- Table: {table_name} ({len(rows)} records)")
            if not rows:
                sql_lines.append(f"-- (No records in {table_name})\n")
                continue
                
            cols_str = ', '.join([f'"{c}"' for c in columns])
            
            for row in rows:
                vals = []
                for val in row:
                    if val is None:
                        vals.append("NULL")
                    elif isinstance(val, (int, float)):
                        vals.append(str(val))
                    elif isinstance(val, bool):
                        vals.append("TRUE" if val else "FALSE")
                    else:
                        val_str = str(val).replace("'", "''")
                        vals.append(f"'{val_str}'")
                vals_str = ', '.join(vals)
                sql_lines.append(f'INSERT INTO "{table_name}" ({cols_str}) VALUES ({vals_str});')
            sql_lines.append("")
        except Exception as e:
            sql_lines.append(f"-- Error exporting {table_name}: {str(e)}\n")
            
    sql_lines.append("COMMIT;\n")
    
    sql_content = "\n".join(sql_lines)
    filename = f"backup_school_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    return Response(
        content=sql_content,
        media_type="application/sql",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )
