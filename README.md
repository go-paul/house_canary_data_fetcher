# Run project

```shell
$ docker-compose -f docker/docker-compose.dev.yml up
```

This will start a server listening on [http://localhost:5555](http://localhost:5555).

To test the endpoint use a link that looks like this
http://localhost:5555/realty?street_address=123+Main+St&city=Cityville&state=OK&zip=11111&details=[sewer,year_built]

Currently supported details: `sewer`, `pool`, `year_built`.

# Run tests

```shell
docker-compose -f docker/docker-compose.dev.yml run house_canary_data_fetcher_server python -m unittest
```