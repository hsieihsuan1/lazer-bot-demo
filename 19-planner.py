"""Offline synthetic planning workflow adapted from the original scenario/filter design."""
from datetime import date
from math import hypot,isfinite
from .scenario import _rain_scenario

# Coordinates are a made-up kilometer grid, NOT GPS or São Paulo locations.
PLACES=[
 {"name":"Parque Exemplo Verde","x":2,"y":1,"indoor":False,"price":0,"family":True},
 {"name":"Museu Exemplo Azul","x":3,"y":2,"indoor":True,"price":20,"family":True},
 {"name":"Oficina Exemplo Criativa","x":4,"y":1,"indoor":True,"price":35,"family":True},
 {"name":"Trilha Exemplo Longa","x":9,"y":8,"indoor":False,"price":0,"family":False},
 {"name":"Teatro Exemplo Noturno","x":5,"y":3,"indoor":True,"price":80,"family":False},
]
def plan(payload):
 if not isinstance(payload,dict):raise ValueError("Esperado objeto.")
 target=date.fromisoformat(payload.get('date',''))
 group=payload.get('group');preference=payload.get('preference')
 if group not in ('familia','casal','amigos','solo') or preference not in ('misto','indoor','outdoor'):raise ValueError("Perfil inválido.")
 numbers=[]
 for key,lower,upper in [('radius',1,20),('budget',0,500),('rain',0,100)]:
  value=payload.get(key)
  if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or not lower<=value<=upper:raise ValueError("Limite inválido.")
  numbers.append(value)
 radius,budget,rain=numbers
 candidates=[]
 for place in PLACES:
  distance=hypot(place['x'],place['y'])
  if distance<=radius and place['price']<=budget and (group!='familia' or place['family']):
   candidates.append({**place,'distance':round(distance,2)})
 candidates.sort(key=lambda p:p['distance'])
 scenario=_rain_scenario(rain)
 # Rain takes precedence over an outdoor preference. A fallback is always explicit.
 primary=[p for p in candidates if (p['indoor'] if scenario=='chuva' or preference=='indoor' else not p['indoor'] if preference=='outdoor' or scenario=='sol' else True)]
 fallback=[p for p in candidates if p['indoor']]
 return {'date':target.isoformat(),'scenario':scenario,'primary':primary[:2],'fallback':fallback[:2],'note':'Catálogo, preços, distância e chuva fictícios. Não são disponibilidade ou previsão real. O orçamento é por atividade/pessoa, não total do passeio.'}
