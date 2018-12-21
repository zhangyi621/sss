from apps import create_api_add
from apps.settings import APIConfig

api_app = create_api_add(APIConfig)

if __name__ == '__main__':
    print(api_app.url_map)
    api_app.run(port=9101)
