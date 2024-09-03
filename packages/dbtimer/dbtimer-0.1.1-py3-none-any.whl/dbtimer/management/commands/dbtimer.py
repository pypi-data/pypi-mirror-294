import json
import time
import uuid
import io
import requests
from datetime import datetime
import random

import boto3
from tqdm import tqdm
import matplotlib.pyplot as plt

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.db import connections
from django.template import Template, Context, loader

from dbtimer.conf import STORAGE_URL
from dbtimer.models import DBTimerHistory, DBTimerHelper
from dbtimer.utils import QueryLogger


class Command(BaseCommand):
    help = """
     This management command measures the time taken to perform various database operations (read, write, search)
     on different models across multiple database configurations. It is primarily used for performance benchmarking
     of database queries within a Django application.

     The command executes a series of read, write, and search operations on specified models and records the time taken 
     for each operation. It supports running these operations on multiple databases to compare performance metrics.

     Key functionalities of the command include:
     - Configuring the models, fields, and types of operations to benchmark via Django settings.
     - Logging and handling any exceptions that occur during the database operations.
     - Generating performance graphs to visualize query times and uploading them to an S3-compatible storage service.
     - Calculating and displaying a performance comparison between a 'default' database configuration and other databases.
     - Saving detailed results in JSON and HTML formats, which include performance metrics and comparisons.
    
     Command-line arguments:
     --notes : Optional argument to provide additional notes (e.g., current branch, schema changes) for the benchmark session.
    
     This command is useful for developers and database administrators who want to understand and optimize 
     the query performance of their Django applications across different databases or configurations.
     """

    def __init__(self, *args, **kwargs):
        """Initialize the command with default parameters."""
        self.pks = []
        self.cycles = 0
        self.sleep = 0
        self.durations = {}
        self.exceptions = {}

    def add_arguments(self, parser):
        """Define command-line arguments for the management command."""
        parser.add_argument(
            "--notes",
            default="",
            action="store",
            dest="notes",
            help="""Enter notes, for example which branch you are on, 
            if the field names have been changed""",
        )

    def render_html(self, context):
        """Render the HTML template with the provided context."""
        template = loader.get_template("dbtimer/index.html")
        return template.render(context)

    def to_file(self, instance, target_field: str, filename: str, contents: str) -> None:
        """Save the rendered content to a temporary file and associate it with a model instance."""
        with NamedTemporaryFile(mode="w+b") as temp:
            temp.write(contents.encode())
            temp.seek(0)
            setattr(instance, target_field, File(temp, name=filename))
            instance.save()

    def append_exception(self, model, db, pk, e):
        """Log exceptions encountered during database operations."""
        self.exceptions[db].append({"model": str(model), "pk": pk, "error": str(e)})

    def random_searchterm(self) -> str:
        """Generate a random search term composed of 10 random letters."""
        ls = []
        for i in range(10):
            ls.append(random.choice("abcdefghijklmopqrstuvwxyz"))
        return "".join(ls)

    def search(self, model, db: str, pk: int, attr: str, search: dict) -> float:
        """Perform a search query on the model using random search terms."""
        for k, v in search.items():
            search[k] = self.random_searchterm()

        ls = []
        for result in model.objects.using(db).filter(**search):
            ls.append(result)

    def write(self, model, db: str, pk: int, attr: str, search: dict = {}) -> float:
        """Perform a write operation on the model by updating an attribute."""
        obj = model.objects.using(db).get(pk=pk)
        value = getattr(obj, attr)
        setattr(obj, attr, value)
        try:
            obj.save()
        except Exception as e:
            self.append_exception(model=model, db=db, pk=pk, e=e)

    def read(self, model, db: str, pk: int, attr: str = "", search: dict = {}):
        """Perform a read operation to fetch an object by its primary key."""
        try:
            model.objects.using(db).get(pk=pk)
        except Exception as e:
            self.append_exception(model=model, db=db, pk=pk, e=e)

    def time_query(self, model, db: str, pk: int, attr: str, search: dict = {}, operation: str = "read") -> float:
        """Measure the time taken to perform a specified database operation."""
        operations = {
            "read": self.read,
            "write": self.write,
            "search": self.search,
        }
        conn = connections[db]
        query_logger = QueryLogger()
        with conn.execute_wrapper(query_logger):
            operations[operation](model=model, db=db, pk=pk, attr=attr, search=search)
        for query in query_logger.queries:
            duration = query["duration"]
            self.durations[db].append(duration)
            return duration

    def random_pks(self):
        """Select random primary keys for testing purposes."""
        ls = []
        for i in range(0, int(self.cycles)):
            pk = random.choice(self.pks)
            ls.append(pk)
            self.pks.remove(pk)
        return ls

    def measure(self, pks: list, db: str = "default", cycles: int = 100, app: str = "quickscan", model: str = "report", operation: str = "read", attr: str = "mic", search: dict = {}) -> float:
        """Measure the average time taken for multiple database operations."""
        ls = []
        for pk in tqdm(pks):
            duration = self.time_query(model=model, db=db, pk=pk, attr=attr, search=search, operation=operation)
            if type(duration) == float:
                ls.append(duration)
            else:
                ls.append(0.1)
            time.sleep(float(self.sleep))
        return sum(ls) / self.cycles

    def calc(self, default: float, newcomer: float) -> str:
        """Calculate and compare the performance difference between default and newcomer databases."""
        if default > newcomer:
            c = round(((default - newcomer) / newcomer) * 100)
            return f"The Newcomer is faster by {c}%"
        elif newcomer > default:
            c = round(((newcomer - default) / default) * 100)
            return f"The Default is faster by {c}%"
        else:
            return "Default and Newcomer are exactly the same."

    def fget(self, url: str) -> list:
        """Fetch data from a URL and return it as a JSON object if successful."""
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return []

    def handle(self, *args, **options):
        """Main method to execute the management command."""
        notes = options.get("notes", "")

        # Initialize S3 bucket to upload graphs
        s3 = boto3.resource(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        bucket = s3.Bucket(settings.LINODE_BUCKET)

        # Get arguments from settings
        args_dict = settings.DBTIMER_ARGS
        # Set some constants
        self.cycles = args_dict["cycles"]
        self.sleep = args_dict["sleep"]

        # Initialize model instance to hold files
        master = DBTimerHistory.objects.create()
        # Initialize container to hold context
        output_dict = {}
        for operation in args_dict["operations"]:
            for model in args_dict["models"]:
                model_args = model["conf"]
                attr = model["attr"]
                search = model["search"]
                model_name = model["name"]
                chosen_model = apps.get_model(*model_args)
                tqdm.write(f"Processing {self.cycles} pks of model {model_name} with interval {self.sleep}")
                count = chosen_model.objects.count()
                qs = chosen_model.objects.all()
                # Empty the list of pks
                self.pks = []
                # Using tqdm to display progress while resolving queryset
                with tqdm(total=count) as t:
                    for i in qs:
                        self.pks.append(i.pk)
                        time.sleep(0.00001)
                        t.update(1)

                # Select random primary keys for processing
                chosen_pks = self.random_pks()

                tqdm.write("Averages (lower is better):")
                comparisons_dict = {}
                for db in tqdm(args_dict["dbs"]):
                    # Initialize buckets for durations and exceptions
                    output_dict[db] = {}
                    self.durations[db] = []
                    self.exceptions[db] = []

                    engine = settings.DATABASES[db]["ENGINE"].split(".")
                    dbname = engine[len(engine) - 1]

                    tqdm.write(f"Processing {db}, engine: {dbname}, model: {model_name}, op: {operation}")
                    average = self.measure(db=db, model=chosen_model, pks=chosen_pks, operation=operation, attr=attr, search=search)

                    tqdm.write(f"{dbname}: {average}")
                    comparisons_dict[db] = average

                    text = f"{model_name} {self.cycles} {self.sleep} {dbname} {operation} avg:{average}"

                    # Create a filename for the graph
                    now = datetime.now().strftime("%Y%m%d-%H%M")
                    basename = f"{now}-{model_name}-{operation}"
                    uu = str(uuid.uuid4())
                    fn = f"{basename}-{uu}-{dbname}.png"

                    tqdm.write(f"Creating graph with caption {text} and filename {fn}")

                    # Plot graph for durations
                    durations = self.durations[db]
                    graph = [x for x in range(len(durations))]
                    plt.plot(graph, durations)
                    plt.figtext(0.5, 0.01, text, horizontalalignment="center", fontsize=10)

                    # Save graph to buffer
                    img_data = io.BytesIO()
                    plt.savefig(img_data, format="png")
                    img_data.seek(0)

                    # Upload graph to S3 bucket
                    bucket.put_object(
                        Body=img_data,
                        ContentType="image/png",
                        Key=fn,
                        ACL="public-read",
                    )

                    plt.close()

                    # Store data for output formats
                    output_dict[db]["dbname"] = dbname
                    output_dict[db]["average"] = average
                    output_dict[db]["graph"] = fn

                # Compare default and newcomer databases
                for db in args_dict["dbs"]:
                    if db == "default":
                        default = comparisons_dict["default"]
                    else:
                        newcomer = comparisons_dict[db]

                comparison = self.calc(default=default, newcomer=newcomer)
                tqdm.write(f"comparisons_dict: {json.dumps(comparisons_dict)}, comparison: {comparison}")

                # Prepare data for JSON output
                data = {
                    "notes": notes,
                    "operation": operation,
                    "model": model_name,
                    "output": output_dict,
                    "cycles": self.cycles,
                    "interval": self.sleep,
                    "comparison": comparison,
                    "exceptions": self.exceptions,
                    "model": model,
                    "pks": chosen_pks,
                }
                helper = DBTimerHelper.objects.create(master=master)
                self.to_file(
                    instance=helper,
                    target_field="json_file",
                    filename=f"{basename}.json",
                    contents=json.dumps(data),
                )

        # Write HTML file content
        context_dict = {
            "storage_url": STORAGE_URL,
            "data": [self.fget(h.json_file.url) for h in master.dbtimerhelper_set.active()]
        }
        html_uuid = str(uuid.uuid4())
        html_fn = f"{now}-{html_uuid}.html"

        # Save HTML to file field
        self.to_file(
            instance=master,
            target_field="html_file",
            filename=html_fn,
            contents=self.render_html(context=context_dict),
        )

        tqdm.write(f"Wrote output to {STORAGE_URL}/{html_fn}")
