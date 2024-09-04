import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    page = 1
    per_page = 25
    headers = {'x-api-key': api_key}
    all_assets = []

    while True:
        url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}&page={page}&per_page={per_page}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error if the request failed
            data = response.json()

            if 'assets' in data:
                assets = data['assets']
                all_assets.extend(assets)
                
                # If the number of assets returned is less than `per_page`, it's likely the last page
                if len(assets) < per_page:
                    break
            else:
                break  # No assets key in the response, end the loop

            page += 1

        except requests.exceptions.RequestException as e:
            return None, f"Error fetching assets: {e}"
    
    return all_assets, None
