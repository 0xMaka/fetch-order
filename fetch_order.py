import requests
import json 

LIMIT = 'https://limit-order-ffo5rqmjnq-uc.a.run.app/orders/view'

def _sort(_json):
  items = dict(dict(dict(_json.items()).items()).items())
  data = items['data']
  pending_orders = items['data']['pendingOrders']
  other_orders = items['data']['otherOrders']
  return data, pending_orders, other_orders

def get_value(_orders, _key):
  orders = dict(_orders['orders'][0])
  return orders[_key]

def _store(_json):
  data, pending_orders, other_orders = _sort(_json)
  try:
    maker = get_value(other_orders, 'maker')
  except:
    maker = get_value(pending_orders, 'maker')
  with open(f'logs/{maker}.log', 'w') as f:
    f.write(json.dumps(_json, indent=2))
    f.close
    return 1

def _order(_address, _chainId):
  query = {   
    'address': _address,     
    'chainId': _chainId,     
    'page': 1,     
    'pendingPage': 1 
  }
  r = requests.post(LIMIT, json=query)
  return r.json()

def store_limit_order(_address, _chainId):
  assert _store(_order(_address, _chainId)) == 1, '0'

def fetch_and_index(_address, _chainId):
  j = _order(_address, _chainId)
  data, pending_orders, other_orders = _sort(j)
  total_pending = pending_orders['totalPendingOrders'] 
  total_other = other_orders['totalOrders'] 

  total = total_pending + total_other
  if total == 0:
    return [[0, 0, 0], 0, 0]

  totals = [total, total_pending, total_other]
  pending = []
  other = []

  if total_pending and total_other > 0:
      for i in pending_orders:
        pending.append(pending_orders[i])
      for i in other_orders:
        other.append(other_orders[i])
      return [totals, pending[0], other[0]]
  elif total_other > 0:
    for i in other_orders: other.append(other_orders[i])
    return [totals, 0, other[0]] 
  else:
    for i in pending_orders: pending.append(pending_orders[i])
    return [totals, pending[0], 0] 

def main():
  user0 = '0xB6207FaCFbc0C7373425D9671Ea0Ca23459E9796' 
  user1 = '0x8c14ed4F602ac4d2Be8Ed9c4716307c73e9A83A8'
  chainId = 137
  print(fetch_and_index(user0, chainId))
  store_limit_order(user1, chainId)

if __name__ == '__main__':
  main()

