from app.database import SessionLocal
from app import models
import json

names = [
    'lalith_sai-123','superadmin','pro_mentor','star_student',
    'lalith_sai','sai','Sitigx','lalith_sai21','lalith_sai-12','qwe'
]

db = SessionLocal()
try:
    users = db.query(models.User).filter(models.User.username.in_(names)).all()
    out = []
    for u in users:
        out.append({
            'username': u.username,
            'id': u.id,
            'xp': getattr(u, 'xp', None),
            'streak': getattr(u, 'streak', None)
        })
    print(json.dumps(out, indent=2))
finally:
    db.close()
