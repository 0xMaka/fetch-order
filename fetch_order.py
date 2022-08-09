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
  maker = get_value(other_orders, 'maker')
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
  
  pending = []
  other = []

  total = other_orders['totalOrders']
  total_pending = len(pending_orders['orders']) 
  total_other = total - total_pending 

  if total == 0:
    print('No orders found')
  elif total_pending and total_other > 0:
      for i in pending_orders:
        pending.append(pending_orders[i])
      for i in other_orders:
        other.append(other_orders[i])
  else:
    print('No pending orders found')
    for i in other_orders: other.append(other_orders[i])
  
  return [[total, total_pending, total_other], pending[0], other[0]]

def main():
  user = '0xB6207FaCFbc0C7373425D9671Ea0Ca23459E9796'
  chainId = 137
  fetch_and_index(user, chainId)

if __name__ == '__main__':
  main()

