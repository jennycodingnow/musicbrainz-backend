# MusicBrainz ETL (Extract Transform Load)

The goal of this project is to become familiar with loading data into a database from an external source.

In this project, you will use the MusicBrainz API to store both artist and release data in mongoDB. We will use this data in subsequent projects to create an API and an frontend to consume the API.

API Details: https://musicbrainz.org/doc/MusicBrainz_API

## Running mongo DB using Docker

For an intro to Docker, check out: https://docker-curriculum.com/ 

* Download and install Docker Desktop: https://www.docker.com/products/docker-desktop/
* A Docker compose file has already been provided for running mongodb
* Run the following command to run a container with mongodb: `docker-compose up -d` Specifying -d will run the image in detached mode
* To check the status of your docker images: `docker ps`
* To stop a docker image: `docker stop <container-name>` in this project, that would be `docker stop code_tl_musicbrainz`
* To start the image: `docker start <container-name>`. `docker start code_tl_musicbrainz`
* See Docker documentation for more information on building/running containers

## Project objectives

1. Write a script or application that will allow you to search MusicBrainz for artists and load both their artist data and release data into mongoDB.
2. Add a database to mongodb that you will use for your project. Use this database to add the collections described below.
3. For the `Artist` collection, store the following fields:
    * MBID - this is the artist ID from MusicBrainz
    * Name
    * Country
    * Type
4. For the `Release` collection, store the following fields:
    * MBID - this is the release ID from MusicBrainz
    * Artist
    * ArtistId - this would be the mongo Object ID that corresponds to the Artist
    * Country
    * Title
    * Date
    * Status
    * CoverArtUrl - Cover art must be retrieved using a separate API, see API Examples Below

## MusicBrainz API Examples

* Searching for an artist to retrieve their artist ID: https://musicbrainz.org/ws/2/artist?query=name:radiohead&fmt=json
* Retrieving a list of releases by a specific artist: https://musicbrainz.org/ws/2/release?artist=a74b1b7f-71a5-4011-9441-d0b5e4122711&fmt=json 
* Retrieving cover art:
    * https://coverartarchive.org/release/<musicbrainz-release-id>
    * https://coverartarchive.org/release/07aab296-9a40-42a9-8d1f-6b06aa032e8a/

## Notes

Knowing how to query monogDB directly will be a useful skill. I would recommend using both the native mongoDB SDKs and an ORM for interacting with MongoDB: https://www.mongodb.com/developer/products/mongodb/mongodb-orms-odms-libraries/

## Bonus

Try using another database like PostgresQL or MySQL. ChatGPT is a good resource for generating Dockerfiles for services like this.
