import pandas as pd
import glob
import xml.etree.ElementTree as ET
from datetime import datetime

log_file = "log_file.txt"
output = "transformed_data.csv"


def extract_from_csv(myfile):
    dataframe = pd.read_csv(myfile)
    return dataframe


def extract_from_json(myfile):
    dataframe = pd.read_json(myfile, lines=True)
    return dataframe


def extract_from_xml(myfile):
    dataframe = pd.DataFrame(
        columns=["car_model", "year_of_manufacture", "price", "fuel"])
    tree = ET.parse(myfile)
    root = tree.getroot()
    for car in root:
        model = car.find("car_model").text
        year = int(car.find("year_of_manufacture").text)
        price = float(car.find("price").text)
        fuel = car.find("fuel").text
        dataframe = pd.concat([dataframe, pd.DataFrame(
            [{"car_model": model, "year_of_manufacture": year, "price": price, "fuel": fuel}])], ignore_index=True)

    return dataframe


def extract():
    extracted = pd.DataFrame(
        columns=["car_model", "year_of_manufacture", "price", "fuel"])

    for file in glob.glob("*.csv"):
        if file != output:
            extracted = pd.concat([extracted, pd.DataFrame(
                extract_from_csv(file))], ignore_index=True)

    for file in glob.glob("*.json"):
        extracted = pd.concat([extracted, pd.DataFrame(
            extract_from_json(file))], ignore_index=True)

    for file in glob.glob("*.xml"):
        extracted = pd.concat([extracted, pd.DataFrame(
            extract_from_xml(file))], ignore_index=True)

    return extracted


def transform(data):
    # 1USD is 9.09 MAD
    data["price"] = round(data.price*9.09, 3)
    return data


def load(target, transformed):
    transformed.to_csv(target)


def log_progress(message):
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    now = datetime.now()
    timestring = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestring + "," + message + "\n")


# Log the initialization of the ETL process
log_progress("ETL Job Started")
# Log the beginning of the Extraction process
log_progress("Extract phase Started")
extracted_data = extract()
# Log the completion of the Extraction process
log_progress("Extract phase Ended")
# Log the beginning of the Transformation process
log_progress("Transform phase Started")
transformed_data = transform(extracted_data)
print("Transformed Data")
print(transformed_data)
# Log the completion of the Transformation process
log_progress("Transform phase Ended")
# Log the beginning of the Loading process
log_progress("Load phase Started")
load(output, transformed_data)
# Log the completion of the Loading process
log_progress("Load phase Ended")
# Log the completion of the ETL process
log_progress("ETL Job Ended")
