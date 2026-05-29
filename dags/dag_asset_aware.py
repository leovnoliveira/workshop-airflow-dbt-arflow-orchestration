from airflow.sdk import Asset, dag, task 
from dotenv import load_dotenv
from airflow.model import Variable
import os 


load_dotenv() 

dbt_env = Variable.get("dbt_env", default_var="dev").lower()

if dbt_env not in ("dev", "prod"):
    raise ValueError(f"dbt_env inválido: {dbt_env!r}, use  'dev' ou 'prod'")

asset_name_dev = f"postgres://{os.getenv('DOCKER_HOST')}:{os.getenv('DOCKER_PORT')}/postgres/public/stg_cadastros_2"
asset_name_prod = f"postgres://{os.getenv('ASTRO_HOST')}:{os.getenv('ASTRO_PORT')}/railway/public/stg_cadastros_2"

asset_name = asset_name_dev if dbt_env == "dev" else asset_name_prod


asset_tabela = Asset(
    name=asset_name,
    uri=asset_name,
    group='asset'
)

@dag(schedule=[asset_tabela])
def new_asset():
    @task
    def print_asset():
        print("Asset: ", asset_tabela)
        print_asset()

new_asset()


