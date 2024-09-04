# scorep-db
Minimal tooling to keep track of Score-P Profiles + Traces.
It relies on Score-P's metadata collection abilities.

<img src="figures/scorep-db-overview.png" alt="alt text" width="400"/>

__Until__ version 1.0 is reached, this is a proof of concept.
Metadata schema structure may change without notice before version 1.0.

It currently relies on [feature branches of Score-P](https://perftools.pages.jsc.fz-juelich.de/cicd/scorep/branches/MR300/latest.tar.gz) and [master branch of cubelib](https://perftools.pages.jsc.fz-juelich.de/cicd/cubelib/branches/master/latest.tar.gz).

---
## Install
Either install via `pip`
```
pip install scorep-db
```
or from source (git).

## scorep-db commands
```
scorep-db add          <config> [offline|online] <path/to/experiment>
scorep-db query        <config> [offline|online] <path/to/query.sparql>
scorep-db download     <config> [offline|online] <path/to/download_query.sparql> <target/path>
scorep-db health-check <config> [offline|online]
scorep-db merge        <config>
scorep-db get-id                                 <path/to/experiment>
scorep-db clear        <config> [offline|online]
```
Brief explanation:
- __add__: Adds an experiment to the database
- __query__: Query the database with a sparql query file
- __download__: Download test cases according to a certain query the the target_path. The query must follow some structure (see below)
- __health-check__: Test, if the databases are available
- __merge__: Merges an offline database into a online database
- __get-id__: Get the Score-P Experiment ID (same as `scorep-info show-metatadata --experiment-id`)
- __clear__: Delete everything within the selected database.
## Query
See directory `example/query/` for some queries.


## Download Query
The download capability currently relies on a query with a special format.
The query __must__ be based on the following minimal example.
It is critical, that the results `?Experiment` and `?storePath` are in the result.
It does not matter, if they are upper or lower or mixed case.
```
PREFIX scorep: <http://scorep-fair.github.io/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?Experiment ?storePath
WHERE {
  ?Experiment rdf:type scorep:Experiment ;
              scorep:storePath ?storePath .
}
```
The query above will download all experiments into to specified target path.
The name will be (some random) `uuid` name, so no renaming takes place.

The download name can be modified by providing additional search terms.
```
PREFIX scorep: <http://scorep-fair.github.io/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?Experiment ?storePath ?program
WHERE {
  ?Experiment rdf:type scorep:Experiment  ;
              scorep:storePath ?storePath ;
              scorep:program   ?program   .
}
```
The query above leads to the name
`program_<program_name>.<experiment-id>` (e.g. `program_sp-mz.A.x.709330_1725173478_308410`).
This name is created by concatinating any search key words and its values.
Each `?Experiment` is unique - if it appears multiple times in a search results, the folder name
will be created by merging the key,value pairs together.

E.g. the following query
```
PREFIX scorep: <http://scorep-fair.github.io/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?experiment ?storePath ?program ?n ?c ?toolchain
WHERE {
  ?experiment rdf:type scorep:Experiment    ;
              scorep:storePath   ?storePath ;
              scorep:program     ?program   ;
              scorep:environment ?envVar    .

  ?envVar scorep:envName  ?envName  ;
          scorep:envState ?envState ;
          scorep:envValue ?envValue .

  FILTER(?envName IN ("SLURM_NTASKS", "SLURM_CPUS_PER_TASK", "TC_NAME"))
  FILTER(?envState = "set")
  FILTER(?program = "sp-mz.A.x")

  BIND(IF(?envName = "SLURM_NTASKS", ?envValue, "") AS ?n)
  BIND(IF(?envName = "SLURM_CPUS_PER_TASK", ?envValue, "") AS ?c)
  BIND(IF(?envName = "TC_NAME", ?envValue, "") AS ?toolchain)
}
```
will create a download pattern of e.g
```
n_2.c_2.toolchain_foss2022a.program_sp.mz.A.x.709330_1725173478_308410/
```

which allows the user to associate some case setup with the folder name.
Not that this naming scheme is _close_ to the
[one needed for Extra-P](https://github.com/extra-p/extrap/blob/master/docs/file-formats.md#cube-file-format).
This does not work yet, but might be addressed in the future.


## Inclusion of 'external' data.
Other JSON-LD files may be merged and linked into the metadata.

The User has to link its JSON-LD the Score-P Run to its metadata.
The runtime id of the Score-P Run can be extracted with

```
SCOREP_RUN_ID=`scorep-db get-id <path/to/experiment_directory>`
echo $SCOREP_RUN_ID
```
or
```
SCOREP_RUN_ID=`scorep-info show-metadata --experiment-id <path/to/experiment_directory>`
echo $SCOREP_RUN_ID
```

which can then be used to link the external JSON-LD to this Score-P Experiment.

See scripts in `cube_x_to_jsonld/*` on how this might exemplarily be done.


## Performance
The query via RDFlib is quite slow, and, depeding on the query, can be _very, very_ slow.
This issue can be solved by using a different, more performance "Triple Store" backend.

## Config File Layout
Almost all `scorep-db` command need a config file (except `get-id`).
The config file configures some paths and credentials of the following type.
```
# Offline - Data Store
SCOREP_DB_OFFLINE_DIRECTORY=${HOME}/repos/scorep-db/example/showcase_NAS-NPB/showcase_database/

# Offline - Metadata Store
SCOREP_DB_OFFLINE_PATH=${HOME}/repos/scorep-db/example/showcase_NAS-NPB/showcase_database/
SCOREP_DB_OFFLINE_NAME=scorep-experiments.db

# ----------------------------------------- #

# Online - Data Store
SCOREP_DB_ONLINE_OBJ_HOSTNAME=localhost
SCOREP_DB_ONLINE_OBJ_PORT=9000
SCOREP_DB_ONLINE_OBJ_USER=minioadmin
SCOREP_DB_ONLINE_OBJ_PASSWORD=minioadmin
SCOREP_DB_ONLINE_OBJ_BUCKET_NAME=scorep-experiments

# Online - Metadata Store
SCOREP_DB_ONLINE_RDF_HOSTNAME=localhost
SCOREP_DB_ONLINE_RDF_PORT=5432
SCOREP_DB_ONLINE_RDF_USER=postgres
SCOREP_DB_ONLINE_RDF_PASSWORD=mysecretpassword
SCOREP_DB_ONLINE_RDF_DB_NAME=postgres

```

##


It dependes on the metadata emitted by Score-P

The env may contain further data, which means
that this must be attributed as well.

I this case it will be attributed to the run.
The envVariable_name is the property, its is the value

## Example usage

View the showcase in `example/showcase_NAS-NPB/03_run_testcases.sh`

# Setup 'Online' Infrastructure
You can use docker to host the _online_ infrastructure.
Make sure to match these with the `<config_files>`.
__Postgres__
```bash
$ docker pull postgres
$ docker run --name my_postgres \
             -e POSTGRES_PASSWORD=mysecretpassword \
             -p 5432:5432 \
             -d \
             postgres
```
__Minio__
```bash
$ docker pull minio/minio
$ docker run --name minio \
    -v $HOME/.minio-data:/data \
    -v $HOME/.minio:/root/.minio \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    -p 9000:9000 \
    -p 9001:9001 \
    -d \
    minio/minio server /data --console-address ":9001"

```
