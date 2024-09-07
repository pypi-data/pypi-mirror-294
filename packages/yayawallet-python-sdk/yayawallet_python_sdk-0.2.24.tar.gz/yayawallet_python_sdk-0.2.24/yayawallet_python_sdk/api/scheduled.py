from ..functions.api_request import api_request

async def create(account_number: str, amount: str, reason: str, recurring: str, start_at: str, meta_data, api_key: str = None):
  api_response = await api_request("POST", "/scheduled-payment/create", "", {"account_number": account_number, "amount": amount, "reason": reason, "recurring": recurring, "start_at": start_at, "meta_data": meta_data}, api_key)
  return api_response

async def get_list(param, api_key = None):
  page_number_param = "?p=1"
  if(param != None):
    page_number_param = param
  api_response = await api_request("GET", "/scheduled-payment/list", page_number_param, None, api_key)
  return api_response

async def archive(id, api_key = None):
  api_response = await api_request("GET", "/scheduled-payment/archive/" + id, "", None, api_key)
  return api_response