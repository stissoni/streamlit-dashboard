import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv


class DynamoHandler:
    def __init__(self):
        print("Connecting to Dynamo database...")

        # Initialize the DynamoDB resource
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        print("Connected to Dynamo database!")

    def get_table(self, table_name):
        try:
            # Get the table
            table = self.dynamodb.Table(table_name)

            return table
        except Exception as e:
            print(f"Error: {e}")

    def get_distinct_values(self, table, column_name):
        try:
            table = self.get_table(table)
            response = table.scan(ProjectionExpression=column_name)
            items = response["Items"]

            values = set()
            for item in items:
                values.add(item[column_name])

            return values
        except Exception as e:
            print(f"Error: {e}")

    def full_scan(self, table_name):
        try:
            table = self.get_table(table_name)
            items = []
            response = table.scan()

            while "LastEvaluatedKey" in response:
                items.extend(response["Items"])
                response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])

            # Add the last batch of items
            items.extend(response.get("Items", []))

            print("Obtained items:", len(items))
            return items
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_distinct_models_by_manufacturer(self, manufacturer):
        try:
            table = self.get_table("listings")

            values = set()
            last_evaluated_key = None

            while True:
                query_params = {
                    "IndexName": "ManufacturerModelDateIndex",
                    "KeyConditionExpression": Key("manufacturer").eq(manufacturer),
                }

                if last_evaluated_key:
                    query_params["ExclusiveStartKey"] = last_evaluated_key

                response = table.query(**query_params)
                items = response.get("Items", [])

                print(f"Obtained {len(items)} items for {manufacturer}")

                for item in items:
                    values.add(item["model"])

                last_evaluated_key = response.get("LastEvaluatedKey")
                if not last_evaluated_key:
                    break  # No more pages to fetch

            return values
        except Exception as e:
            print(f"Error: {e}")
            return set()

    def create_gsi(self):
        table = self.get_table("listings")
        table.update(
            AttributeDefinitions=[
                {"AttributeName": "manufacturer", "AttributeType": "S"},
                {"AttributeName": "model", "AttributeType": "S"},
                {"AttributeName": "date", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    "Create": {
                        "IndexName": "ManufacturerModelDateIndex",
                        "KeySchema": [
                            {"AttributeName": "manufacturer", "KeyType": "HASH"},
                            {"AttributeName": "model", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                }
            ],
        )

    def select_listings(self, manufacturer=None, model=None, date=None):
        try:
            table = self.get_table("listings")

            if manufacturer is None and model is None and date is None:
                # Make a full scan of the table
                response = table.scan()


            # Query the Global Secondary Index
            response = table.query(
                IndexName="ManufacturerModelDateIndex",
                KeyConditionExpression=Key("manufacturer").eq(manufacturer)
                & Key("model").eq(model),
                FilterExpression=Attr("date").eq(date),
            )

            return response.get("Items", [])
        except Exception as e:
            print(f"Error: {e}")

    def insert_listings_df(self, df):
        try:
            items = []

            for _, row in df.iterrows():
                item = {
                    "publication_id": row["publication_id"],
                    "date": str(row["date"]),
                    "url": row["url"],
                    "title": row["title"],
                    "manufacturer": row["manufacturer"],
                    "model": row["model"],
                    "year": int(row["year"]),
                    "kilometers": int(row["kilometers"]),
                    "currency": row["currency"],
                    "price": int(row["price"]),
                }
                items.append(item)

            # Get the table
            table = self.get_table("listings")

            # Insert data into the table
            with table.batch_writer() as batch:
                for item in items:
                    print(f"Inserting {item}")
                    batch.put_item(Item=item)
        except Exception as err:
            print(f"Error: {err}")
            raise err


if __name__ == "__main__":
    # Get credentials from dotenv file
    load_dotenv(override=True)

    # Create a DBHandler object
    db_handler = DynamoHandler()

    # Get listings
    distinct_manufacturers = db_handler.get_distinct_values("listings", "manufacturer")
    print(f"Distinct manufacturers: {distinct_manufacturers}")

    for manufacturer in distinct_manufacturers:
        distinct_models = db_handler.get_distinct_models_by_manufacturer(manufacturer)
        print(f"Distinct models for {manufacturer}: {distinct_models}")
