# trailblaze-pathsense

See [trailblaze-flutter](https://github.com/andreytakhtamirov/trailblaze-flutter) to read about the project.

This module creates routes which are optimized for the chosen transportation mode. It is designed to be accessed from the trailblaze-flutter application. Uses omsnx with data tiles from OpenSteetMap to find routes between 2 given points.

## How Does it Work?
- Supporting a wide region poses the challenge of maintaining low route calculation time.
- My solution involves utilizing small data tiles, each covering an area of 20 $km^2$, which can be dynamically loaded as required.
- By analyzing the origin and destination points of a given query, data tiles can be loaded as needed to process the request.
- This streamlined approach ensures optimal resource utilization even when facing concurrent requests from different regions.

## Implemented Modes
- Gravel cycling ✅
- Road cycling
- Running
- Hiking


## Supported Regions
The area shown below:
![range](https://github.com/andreytakhtamirov/trailblaze-pathsense/assets/70922688/65dd12a0-01c7-4700-8bed-875eba092375)

