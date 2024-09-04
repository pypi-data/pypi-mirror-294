import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    page = 1
    page_size = 25
    headers = {'x-api-key': api_key}
    all_assets = []
    
    while True:
        url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}&page={page}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            
            all_assets.extend(data)
            
            if len(data) < page_size:
                break
            
            page += 1
        
        except requests.exceptions.RequestException as e:
            return {"assets": []}, f"Error fetching assets: {e}"
    
    return {"assets": all_assets}, None
