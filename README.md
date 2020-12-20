# ParkingViolations
Analyzing Millions of NYC Parking Violations

In this project, I will apply what I have learned about EC2, the terminal, Docker and Elasticsearch to ingest and analyze a dataset. I will write a python script that runs in docker to consume data from the NYC Open Data project and pushes that information into an Elasticsearch cluster provisioned via AWS. This way, the data is never “saved” into your EC2 instance but instead streamed directly to Elasticsearch.

Once the data is loaded and available on Elasticsearch, I will create a dashboard with a few visualizations to help better explain/understand the data.
