import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    page = 1
    headers = {'x-api-key': api_key}
    all_assets = []
    
    while True:
        url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}&page={page}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            
            # Append the list of assets to the all_assets list
            all_assets.extend(data)
            
            # Check if there's another page
            if len(data) < PAGE_SIZE:  # PAGE_SIZE should be set to the number of items per page
                break
            
            page += 1
        
        except requests.exceptions.RequestException as e:
            return {"assets": []}, f"Error fetching assets: {e}"
    
    return {"assets": all_assets}, None
