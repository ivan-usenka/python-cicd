import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import parse_table_schema_from_json

BQ_DATASET = 'lake'
BQ_TABLE = 'whatever'

SCHEMA_OBJ = [
    {"name": "id", "type": "STRING", "description": ""},
    {"name": "value", "type": "STRING", "description": ""}
]


class ContactUploadOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--infile',
            type=str,
            help='path of input file',
            default='gs://%s/data_files/test.csv' )

def run(argv=None):
    print('running')
    p = beam.Pipeline(options=PipelineOptions())
    lines = (p
             | beam.Create([
                {"id": "some random name", "value": "i dont know"},
                {"id": "id2", "value": "whatever man"}]))

    schema_str = '{"fields": ' + json.dumps(SCHEMA_OBJ) + '}'
    schema = parse_table_schema_from_json(schema_str)
    output_destination = '%s.%s' % (BQ_DATASET, BQ_TABLE)
    (lines
     | 'Write lines to BigQuery' >> beam.io.WriteToBigQuery(
                output_destination,
                schema=schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

    p.run().wait_until_finish()


if __name__ == '__main__':
    run()