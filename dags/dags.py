from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from airflow.models import Variable
import pendulum
import os

profile_config_dev = ProfileConfig(
    profile_name = "jornada_dw",
    target_name = "dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="docker_postgres_db",
        profile_args={"schema": "public"},
    )
)
profile_config_prod = ProfileConfig(
    profile_name = "jornada_dw",
    target_name = "prod",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="railway_postgres_db",
        profile_args={"schema": "public"}
    ),
)

dbt_env = Variable.get("dbt_env", default_var="dev").lower()
if dbt_env not in ("dev", "prod"):
    raise ValueError(f"dbt_env inválido: {dbt_env!r}, use 'dev'ou 'prod'")

profile_config = profile_config_dev if dbt_env == "dev" else profile_config_prod

my_cosmos_dag = DbtDag(
    project_config = ProjectConfig(
        "/usr/local/airflow/dbt/jornada_dw",

    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ["AIRFLOW_HOME"]}/dbt_venv/bin/dbt",
    ),
    operator_args={
        "install_deps": True
    },
    schedule="@daily",
    start_date=pendulum.datetime(2026, 5, 26),
    catchup=False,
    dag_id=f"dag_jornada_dw_{dbt_env}",
    default_args={"retries": 2},
    # atualizando
)