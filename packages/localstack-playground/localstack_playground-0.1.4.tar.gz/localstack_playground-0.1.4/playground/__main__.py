import os
import subprocess
import argparse
import importlib.resources as pkg_resources

# Import your package's resources
from playground import resources


def get_resource_path(resource_name):
    return str(pkg_resources.files(resources) / resource_name)


def run_command(command):
    subprocess.run(command, shell=True, check=True)


def playground_up(init_script_folder=None):
    compose_file = get_resource_path("playground_compose.yaml")
    run_command(f"docker-compose --profile all -f {compose_file} up -d")


def playground_down():
    compose_file = get_resource_path("playground_compose.yaml")
    run_command(f"docker-compose --profile all -f {compose_file} down")


def playground_reset():
    playground_down()
    try:
        run_command(
            "docker volume rm localstack_playground_postgres localstack_playground_oracle localstack_playground_mysql"
        )
    except subprocess.CalledProcessError:
        pass


def playground_localstack():
    compose_file = get_resource_path("playground_compose.yaml")
    run_command(f"docker-compose --profile localstack -f {compose_file} up -d")


def playground_postgres():
    compose_file = get_resource_path("playground_compose.yaml")
    init_script_path = (
        os.getenv("POSTGRES_INIT_PATH")
        or get_resource_path("init_scripts/postgres")
    )
    run_command(
        f"POSTGRES_INIT_FOLDER={init_script_path} docker-compose --profile postgres -f {compose_file} up -d"
    )


def playground_oracle():
    compose_file = get_resource_path("playground_compose.yaml")
    init_script_path = (
        os.getenv("ORACLE_INIT_PATH")
        or get_resource_path("init_scripts/oracle")
    )
    run_command(
        f"docker-compose --profile oracle -f {compose_file} up -d -v {init_script_path}:/docker-entrypoint-initdb.d"
    )


def playground_mysql():
    compose_file = get_resource_path("playground_compose.yaml")
    init_script_path = (
        os.getenv("MYSQL_INIT_PATH")
        or get_resource_path("init_scripts/mysql")
    )
    run_command(
        f"docker-compose --profile mysql -f {compose_file} up -d -v {init_script_path}:/docker-entrypoint-initdb.d"
    )


def main():
    parser = argparse.ArgumentParser(description="Manage the Localstack Playground")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    subparsers.add_parser("up", help="Start Localstack and all databases")
    subparsers.add_parser("down", help="Stop all playground services")
    subparsers.add_parser(
        "reset", help="Reset the playground (stop services and remove volumes)"
    )

    subparsers.add_parser(
        "localstack", help="Start only Localstack"
    )

    subparsers.add_parser(
        "postgres", help="Start Localstack and the PostgreSQL database"
    )

    subparsers.add_parser(
        "oracle", help="Start Localstack and the Oracle database"
    )

    subparsers.add_parser("mysql", help="Start MySQL service only")
    
    args = parser.parse_args()

    if args.command == "up":
        playground_up()
    elif args.command == "down":
        playground_down()
    elif args.command == "reset":
        playground_reset()
    elif args.command == "localstack":
        playground_localstack()
    elif args.command == "postgres":
        playground_postgres()
    elif args.command == "oracle":
        playground_oracle()
    elif args.command == "mysql":
        playground_mysql()
    else:
        parser.print_help()
